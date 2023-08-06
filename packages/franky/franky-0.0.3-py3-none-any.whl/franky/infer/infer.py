import copy
import os.path as osp
import warnings
from abc import ABCMeta, abstractmethod
from typing import (Any, Callable, Dict, Iterable, List, Optional, Sequence,
                    Tuple, Union)

import numpy as np
import torch
import torch.nn as nn
from rich.progress import track

from franky.config import Config, ConfigDict
from franky.dataset import Compose
from franky.dataset import PseudoCollate
from franky.device import get_device
from franky.registry import MODELS, DefaultScope, COLLATE, TRANSFORMS
from franky.runner.checkpoint import _load_checkpoint, _load_checkpoint_to_model
from franky.utils import dict_del_key_contain

InputType = Union[str, np.ndarray, torch.Tensor]
InputsType = Union[InputType, Sequence[InputType]]
ConfigType = Union[Config, ConfigDict]
ModelType = Union[dict, ConfigType, str]


class InferencerMeta(ABCMeta):
    """Check the legality of the inferencer.

    All Inferencers should not define duplicated keys for
    ``preprocess_kwargs``, ``forward_kwargs``, and
    ``postprocess_kwargs``.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert isinstance(self.preprocess_kwargs, set)
        assert isinstance(self.forward_kwargs, set)
        assert isinstance(self.postprocess_kwargs, set)

        all_kwargs = (
                self.preprocess_kwargs | self.forward_kwargs | self.postprocess_kwargs
        )

        assert len(all_kwargs) == (
                len(self.preprocess_kwargs) + len(self.forward_kwargs) +
                len(self.postprocess_kwargs)), (
            f'Class define error! {self.__name__} should not '
            'define duplicated keys for `preprocess_kwargs`, '
            '`forward_kwargs`, `visualize_kwargs` and '
            '`postprocess_kwargs` are not allowed.')


class BaseInferencer(metaclass=InferencerMeta):
    """Base inferencer for downstream tasks.

    The BaseInferencer provides the standard workflow for inference as follows:

    1. Preprocess the input data by :meth:`preprocess`.
    2. Forward the data to the model by :meth:`forward`. ``BaseInferencer``
       assumes the model inherits from :class:`mmengine.models.BaseModel` and
       will call `model.test_step` in :meth:`forward` by default.
    3. Postprocess and return the results by :meth:`postprocess`.

    When we call the subclasses inherited from BaseInferencer (not overriding
    ``__call__``), the workflow will be executed in order.

    All subclasses of BaseInferencer could define the following class
    attributes for customization:

    - ``preprocess_kwargs``: The keys of the kwargs that will be passed to
      :meth:`preprocess`.
    - ``forward_kwargs``: The keys of the kwargs that will be passed to
      :meth:`forward`
    - ``postprocess_kwargs``: The keys of the kwargs that will be passed to
      :meth:`postprocess`

    All attributes mentioned above should be a ``set`` of keys (strings),
    and each key should not be duplicated. Actually, :meth:`__call__` will
    dispatch all the arguments to the corresponding methods according to the
    ``xxx_kwargs`` mentioned above, therefore, the key in sets should
    be unique to avoid ambiguous dispatching.

    Warning:
        If subclasses defined the class attributes mentioned above with
        duplicated keys, an ``AssertionError`` will be raised during import
        process.

    Subclasses inherited from ``BaseInferencer`` should implement
    :meth:`_init_pipeline` and :meth:`postprocess`:

    - _init_pipeline: Return a callable object to preprocess the input data.
    - postprocess: Postprocess the results returned by :meth:`forward` and
      :meth:`visualize`.

    Args:
        model (str, optional): Path to the config file.
             If model is not specified, user must provide the
            `weights` saved by Franky which contains the config string.
            Defaults to None.
        weights (str, optional): Path to the checkpoint, Defaults to None.
        device (str, optional): Device to run inference. If None, the available
            device will be automatically used. Defaults to None.
        scope (str, optional): The scope of the model. Defaults to None.

    Note:
        Since ``Inferencer`` could be used to infer batch data,
        `collate` should be defined. If `collate` is not defined in config
        file, the `collate` will be `PseudoCollate` by default.
    """  # noqa: E501

    preprocess_kwargs: set = set()
    forward_kwargs: set = set()
    postprocess_kwargs: set = set()

    def __init__(self,
                 model: Union[ModelType, str, None] = None,
                 weights: Optional[str] = None,
                 device: Optional[str] = None,
                 scope: Optional[str] = None) -> None:
        if scope is None:
            default_scope = DefaultScope.get_current_instance()
            if default_scope is not None:
                scope = default_scope.scope_name
        self.scope = scope
        # Load config to cfg
        cfg: ConfigType
        if isinstance(model, str) and osp.isfile(model):
            cfg = Config.fromfile(model)
        elif isinstance(model, (Config, ConfigDict)):
            cfg = copy.deepcopy(model)
        elif isinstance(model, dict):
            cfg = copy.deepcopy(ConfigDict(model))
        elif model is None:
            if weights is None:
                raise ValueError(
                    'If model is None, the weights must be specified since '
                    'the config needs to be loaded from the weights')
            cfg = ConfigDict()
        else:
            raise TypeError('model must be a filepath or any ConfigType'
                            f'object, but got {type(model)}')
        if self.scope is None:
            self.scope = cfg.get('default_scope', None)

        if device is None:
            device = get_device()

        self.model = self._init_model(cfg, weights, device)  # type: ignore
        self.pipeline = self._init_pipeline(cfg)
        self.collate_fn = self._init_collate(cfg)
        self.cfg = cfg

    def __call__(
            self,
            inputs: InputsType,
            return_datasamples: bool = False,
            batch_size: int = 1,
            **kwargs,
    ) -> dict:
        """Call the inferencer.

        Args:
            inputs (InputsType): Inputs for the inferencer.
            return_datasamples (bool): Whether to return results as
                :obj:`BaseDataElement`. Defaults to False.
            batch_size (int): Batch size. Defaults to 1.
            **kwargs: Key words arguments passed to :meth:`preprocess`,
                :meth:`forward` and :meth:`postprocess`.
                Each key in kwargs should be in the corresponding set of
                ``preprocess_kwargs``, ``forward_kwargs``
                and ``postprocess_kwargs``.

        Returns:
            dict: Inference and visualization results.
        """
        (
            preprocess_kwargs,
            forward_kwargs,
            postprocess_kwargs,
        ) = self._dispatch_kwargs(**kwargs)

        ori_inputs = self._inputs_to_list(inputs)
        inputs = self.preprocess(
            ori_inputs, batch_size=batch_size, **preprocess_kwargs)
        preds = []
        for data in track(inputs, description='Inference'):
            preds.extend(self.forward(data, **forward_kwargs))
        results = self.postprocess(preds, return_datasamples,
                                   **postprocess_kwargs)
        return results

    def _inputs_to_list(self, inputs: InputsType) -> list:
        """Preprocess the inputs to a list.

        Preprocess inputs to a list according to its type:

        - list or tuple: return inputs
        - str:
            - Directory path: return all files in the directory
            - other cases: return a list containing the string. The string
              could be a path to file, a url or other types of string according
              to the task.

        Args:
            inputs (InputsType): Inputs for the inferencer.

        Returns:
            list: List of input for the :meth:`preprocess`.
        """
        if not isinstance(inputs, (list, tuple)):
            inputs = [inputs]

        return list(inputs)

    def preprocess(self, inputs: InputsType, batch_size: int = 1, **kwargs):
        """Process the inputs into a model-feedable format.

        Customize your preprocess by overriding this method. Preprocess should
        return an iterable object, of which each item will be used as the
        input of ``model.test_step``.

        ``BaseInferencer.preprocess`` will return an iterable chunked data,
        which will be used in __call__ like this:

        .. code-block:: python

            def __call__(self, inputs, batch_size=1, **kwargs):
                chunked_data = self.preprocess(inputs, batch_size, **kwargs)
                for batch in chunked_data:
                    preds = self.forward(batch, **kwargs)

        Args:
            inputs (InputsType): Inputs given by user.
            batch_size (int): batch size. Defaults to 1.

        Yields:
            Any: Data processed by the ``pipeline`` and ``collate_fn``.
        """
        chunked_data = self._get_chunk_data(
            map(self.pipeline, inputs), batch_size)
        yield from map(self.collate_fn, chunked_data)

    @torch.no_grad()
    def forward(self, inputs: Union[dict, tuple], **kwargs) -> Any:
        """Feed the inputs to the model."""
        return self.model.test_step(inputs)

    @abstractmethod
    def postprocess(
            self,
            preds: Any,
            return_datasample=False,
            **kwargs,
    ) -> dict:
        """Process the predictions and visualization results from ``forward``
        and ``visualize``.

        This method should be responsible for the following tasks:

        1. Convert datasamples into a json-serializable dict if needed.
        2. Pack the predictions and visualization results and return them.
        3. Dump or log the predictions.

        Customize your postprocess by overriding this method. Make sure
        ``postprocess`` will return a dict with visualization results and
        inference results.

        Args:
            preds (List[Dict]): Predictions of the model.
            return_datasample (bool): Whether to return results as datasamples.
                Defaults to False.

        Returns:
            dict: Inference and visualization results with key ``predictions``
            and ``visualization``

            - ``predictions`` (dict or DataSample): Returned by
              :meth:`forward` and processed in :meth:`postprocess`.
              If ``return_datasample=False``, it usually should be a
              json-serializable dict containing only basic data elements such
              as strings and numbers.
        """

    def _init_model(
            self,
            cfg: ConfigType,
            weights: Optional[str],
            device: str = 'cpu',
    ) -> nn.Module:
        """Initialize the model with the given config and checkpoint on the
        specific device.

        Args:
            cfg (ConfigType): Config containing the model information.
            weights (str, optional): Path to the checkpoint.
            device (str, optional): Device to run inference. Defaults to 'cpu'.

        Returns:
            nn.Module: Model loaded with checkpoint.
        """
        checkpoint: Optional[dict] = None
        if weights is not None:
            checkpoint = _load_checkpoint(weights, map_location='cpu')

        if not cfg:
            assert checkpoint is not None
            try:
                # Prefer to get config from `message_hub` since `message_hub`
                # is a more stable module to store all runtime information.
                cfg_string = checkpoint['message_hub']['runtime_info']['cfg']
            except KeyError:
                assert 'meta' in checkpoint, (
                    'If model(config) is not provided, the checkpoint must'
                    'contain the config string in `meta` or `message_hub`, '
                    'but both `meta` and `message_hub` are not found in the '
                    'checkpoint.')
                meta = checkpoint['meta']
                if 'cfg' in meta:
                    cfg_string = meta['cfg']
                else:
                    raise ValueError(
                        'Cannot find the config in the checkpoint.')
            cfg.update(Config.fromstring(cfg_string, file_format='.py')._cfg_dict)

        # Delete the `pretrained` field to prevent model from loading the
        # the pretrained weights unnecessarily.
        dict_del_key_contain(cfg.model, 'pretrained')

        model = self._build_model_from_config(cfg)
        model.cfg = cfg
        self._load_weights_to_model(model, checkpoint, cfg)
        model.to(device)
        model.eval()
        return model

    def _build_model_from_config(self, cfg):
        with MODELS.switch_scope_and_registry(
                self.scope) as registry:
            model = MODELS.build(cfg.model)

        return model

    def _build_collate_from_config(self, cfg):
        with COLLATE.switch_scope_and_registry(
                self.scope) as registry:
            collate_fn = COLLATE.build(cfg.collate)

        return collate_fn

    def _load_weights_to_model(self, model: nn.Module,
                               checkpoint: Optional[dict],
                               cfg: Optional[ConfigType]) -> None:
        """Loading model weights and meta information from cfg and checkpoint.

        Subclasses could override this method to load extra meta information
        from ``checkpoint`` and ``cfg`` to model.

        Args:
            model (nn.Module): Model to load weights and meta information.
            checkpoint (dict, optional): The loaded checkpoint.
            cfg (Config or ConfigDict, optional): The loaded config.
        """
        if checkpoint is not None:
            _load_checkpoint_to_model(model, checkpoint)
        else:
            warnings.warn('Checkpoint is not loaded, and the inference '
                          'result is calculated by the randomly initialized '
                          'model!')

    def _init_collate(self, cfg: ConfigType) -> Callable:
        """Initialize the ``collate_fn`` with the given config.

        The returned ``collate_fn`` will be used to collate the batch data.
        If will be used in :meth:`preprocess` like this

        .. code-block:: python
            def preprocess(self, inputs, batch_size, **kwargs):
                ...
                dataloader = map(self.collate_fn, dataloader)
                yield from dataloader

        Args:
            cfg (ConfigType): Config which could contained the `collate_fn`
                information. If `collate_fn` is not defined in config, it will
                be :func:`pseudo_collate`.

        Returns:
            Callable: Collate function.
        """
        try:
            collate_fn = self._build_collate_from_config(cfg)
        except AttributeError:
            collate_fn = PseudoCollate()
        return collate_fn  # type: ignore

    # @abstractmethod
    def _init_pipeline(self, cfg: ConfigType) -> Callable:
        """Initialize the test pipeline.

        Return a pipeline to handle various input data, such as ``str``,
        ``np.ndarray``. It is an abstract method in BaseInferencer, and should
        be implemented in subclasses.

        The returned pipeline will be used to process a single data.
        It will be used in :meth:`preprocess` like this:

        .. code-block:: python
            def preprocess(self, inputs, batch_size, **kwargs):
                ...
                dataset = map(self.pipeline, dataset)
                ...
        """
        test_pipeline_cfg = cfg.test_dataloader.dataset.pipeline
        test_pipeline = Compose(
            [TRANSFORMS.build(t) for t in test_pipeline_cfg])
        return test_pipeline

    def _get_chunk_data(self, inputs: Iterable, chunk_size: int):
        """Get batch data from dataset.

        Args:
            inputs (Iterable): An iterable dataset.
            chunk_size (int): Equivalent to batch size.

        Yields:
            list: batch data.
        """
        inputs_iter = iter(inputs)
        while True:
            try:
                chunk_data = []
                for _ in range(chunk_size):
                    processed_data = next(inputs_iter)
                    chunk_data.append(processed_data)
                yield chunk_data
            except StopIteration:
                if chunk_data:
                    yield chunk_data
                break

    def _dispatch_kwargs(self, **kwargs) -> Tuple[Dict, Dict, Dict]:
        """Dispatch kwargs to preprocess(), forward(), visualize() and
        postprocess() according to the actual demands.

        Returns:
            Tuple[Dict, Dict, Dict]: kwargs passed to preprocess,
            forward, visualize and postprocess respectively.
        """
        # Ensure each argument only matches one function
        method_kwargs = self.preprocess_kwargs | self.forward_kwargs | \
                        self.postprocess_kwargs

        union_kwargs = method_kwargs | set(kwargs.keys())
        if union_kwargs != method_kwargs:
            unknown_kwargs = union_kwargs - method_kwargs
            raise ValueError(
                f'unknown argument {unknown_kwargs} for `preprocess`, '
                '`forward`, `visualize` and `postprocess`')

        preprocess_kwargs = {}
        forward_kwargs = {}
        postprocess_kwargs = {}

        for key, value in kwargs.items():
            if key in self.preprocess_kwargs:
                preprocess_kwargs[key] = value
            elif key in self.forward_kwargs:
                forward_kwargs[key] = value
            else:
                postprocess_kwargs[key] = value

        return (
            preprocess_kwargs,
            forward_kwargs,
            postprocess_kwargs,
        )
