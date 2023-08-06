from abc import abstractmethod
from collections import OrderedDict
from typing import Dict, Mapping, Optional, Sequence, Union, Tuple

import torch
import torch.nn as nn

from franky.optim import OptimWrapper
from franky.registry import MODELS
from franky.structures import BaseDataElement
from franky.utils import is_list_of
from ..base_module import BaseModule

CastData = Union[tuple, dict, BaseDataElement, torch.Tensor, list, bytes, str, None]


class BaseModel(BaseModule):
    """Base class for all algorithmic models.

    BaseModel implements the basic functions of the algorithmic model, such as
    weights initialize, parse losses, and update model parameters.

    Subclasses inherit from BaseModel only need to implement the forward
    method, which implements the logic to calculate loss and predictions,
    then can be trained in the runner.

    Examples:
        >>> @MODELS.register_module()
        >>> class ToyModel(BaseModel):
        >>>
        >>>     def __init__(self):
        >>>         super().__init__()
        >>>         self.backbone = nn.Sequential()
        >>>         self.backbone.add_module('conv1', nn.Conv2d(3, 6, 5))
        >>>         self.backbone.add_module('pool', nn.MaxPool2d(2, 2))
        >>>         self.backbone.add_module('conv2', nn.Conv2d(6, 16, 5))
        >>>         self.backbone.add_module('fc1', nn.Linear(16 * 5 * 5, 120))
        >>>         self.backbone.add_module('fc2', nn.Linear(120, 84))
        >>>         self.backbone.add_module('fc3', nn.Linear(84, 10))
        >>>
        >>>         self.criterion = nn.CrossEntropyLoss()
        >>>
        >>>     def forward(self, batch_inputs, data_samples, mode='pred'):
        >>>         data_samples = torch.stack(data_samples)
        >>>         if mode == 'pred':
        >>>             return self.backbone(batch_inputs)
        >>>         elif mode == 'eval':
        >>>             feats = self.backbone(batch_inputs)
        >>>             predictions = torch.argmax(feats, 1)
        >>>             return predictions
        >>>         elif mode == 'train':
        >>>             feats = self.backbone(batch_inputs)
        >>>             loss = self.criterion(feats, data_samples)
        >>>             return dict(loss=loss)

    Args:
        init_cfg (dict, optional): The weight initialized config for
            :class:`BaseModule`.

    Attributes:
        init_cfg (dict, optional): Initialization config dict.
    """

    def __init__(self,
                 init_cfg: Optional[dict] = None):
        super().__init__(init_cfg)
        self._device = torch.device('cpu')

    @property
    def device(self):
        return self._device

    def train_step(self, data: Union[dict, tuple, list],
                   optim_wrapper: OptimWrapper) -> Dict[str, torch.Tensor]:
        """Implements the default model training process including
        preprocessing, model forward propagation, loss calculation,
        optimization, and back-propagation.

        During non-distributed training. If subclasses do not override the
        :meth:`train_step`, :class:`EpochBasedTrainLoop` or
        :class:`IterBasedTrainLoop` will call this method to update model
        parameters. The default parameter update process is as follows:

        1. Calls ``self(batch_inputs, data_samples, mode='train')`` to get raw
           loss
        2. Calls ``self.parse_losses`` to get ``parsed_losses`` tensor used to
           backward and dict of loss tensor used to log messages.
        3. Calls ``optim_wrapper.update_params(loss)`` to update model.

        Args:
            data (dict or tuple or list): Data sampled from dataset.
            optim_wrapper (OptimWrapper): OptimWrapper instance
                used to update model parameters.

        Returns:
            Dict[str, torch.Tensor]: A ``dict`` of tensor for logging.
        """
        # Enable automatic mixed precision training context.
        with optim_wrapper.optim_context(self):
            losses = self._run_forward(data, mode='train')  # type: ignore
        parsed_losses, log_vars = self.parse_losses(losses)  # type: ignore
        optim_wrapper.update_params(parsed_losses)
        return log_vars

    def val_step(self, data: Union[tuple, dict, list]) -> list:
        """Gets the predictions of given data.

        Calls ``self(inputs, data_sample, mode='eval')``. Return the
        predictions which will be passed to evaluator.

        Args:
            data (dict or tuple or list): Data sampled from dataset.

        Returns:
            list: The predictions of given data.
        """
        return self._run_forward(data, mode='eval')  # type: ignore

    def test_step(self, data: Union[dict, tuple, list]) -> list:
        """``BaseModel`` implements ``test_step`` the same as ``val_step``.

        Args:
            data (dict or tuple or list): Data sampled from dataset.

        Returns:
            list: The predictions of given data.
        """
        return self._run_forward(data, mode='pred')  # type: ignore

    def parse_losses(
            self, losses: Dict[str, torch.Tensor]
    ) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        """Parses the raw outputs (losses) of the network.

        Args:
            losses (dict): Raw output of the network, which usually contain
                losses and other necessary information.

        Returns:
            tuple[Tensor, dict]: There are two elements. The first is the
            loss tensor passed to optim_wrapper which may be a weighted sum
            of all losses, and the second is log_vars which will be sent to
            the logger.
        """
        log_vars = []
        for loss_name, loss_value in losses.items():
            if isinstance(loss_value, torch.Tensor):
                log_vars.append([loss_name, loss_value.mean()])
            elif is_list_of(loss_value, torch.Tensor):
                log_vars.append(
                    [loss_name,
                     sum(_loss.mean() for _loss in loss_value)])
            else:
                raise TypeError(
                    f'{loss_name} is not a tensor or list of tensors')

        loss = sum(value for key, value in log_vars if 'loss' in key)
        log_vars.insert(0, ['loss', loss])
        log_vars = OrderedDict(log_vars)  # type: ignore

        return loss, log_vars  # type: ignore

    def to(self, *args, **kwargs) -> nn.Module:
        # Since Torch has not officially merged
        # the npu-related fields, using the _parse_to function
        # directly will cause the NPU to not be found.
        # Here, the input parameters are processed to avoid errors.
        if args and isinstance(args[0], str) and 'npu' in args[0]:
            args = tuple(
                [list(args)[0].replace('npu', torch.npu.native_device)])
        if kwargs and 'npu' in str(kwargs.get('device', '')):
            kwargs['device'] = kwargs['device'].replace(
                'npu', torch.npu.native_device)

        self._device = torch._C._nn._parse_to(*args, **kwargs)[0]
        return super().to(*args, **kwargs)

    def cuda(
            self,
            device: Optional[Union[int, str, torch.device]] = None,
    ) -> nn.Module:
        if device is None or isinstance(device, int):
            self._device = torch.device('cuda', index=device)
        return super().cuda(device)

    def npu(
            self,
            device: Union[int, str, torch.device, None] = None,
    ) -> nn.Module:
        """
        Returns:
            nn.Module: The model itself.

        Note:
            This generation of NPU(Ascend910) does not support
            the use of multiple cards in a single process,
            so the index here needs to be consistent with the default device
        """
        self._device = torch.npu.current_device()
        return super().npu()

    def cpu(self, *args, **kwargs) -> nn.Module:
        return super().cpu()

    @abstractmethod
    def forward(self,
                inputs: torch.Tensor,
                data_samples: Optional[list] = None,
                mode: str = 'pred') -> Union[Dict[str, torch.Tensor], list]:
        """Returns losses or predictions of training, validation, testing, and
        simple inference process.

        ``forward`` method of BaseModel is an abstract method, its subclasses
        must implement this method.

        Accepts ``batch_inputs`` and ``data_sample`` processed by
        :attr:`data_preprocessor`, and returns results according to mode
        arguments.

        During non-distributed training, validation, and testing process,
        ``forward`` will be called by ``BaseModel.train_step``,
        ``BaseModel.val_step`` and ``BaseModel.val_step`` directly.

        During distributed data parallel training process,
        ``OPSeparateDistributedDataParallel.train_step`` will first call
        ``DistributedDataParallel.forward`` to enable automatic
        gradient synchronization, and then call ``forward`` to get training
        loss.

        Args:
            inputs (torch.Tensor): batch input tensor collated by
                :attr:`data_preprocessor`.
            mode (str): mode should be one of ``train``, ``eval`` and
                ``pred``

                - ``train``: Called by ``train_step`` and return loss ``dict``
                  used for logging
                - ``eval``: Called by ``val_step`` and ``test_step``
                  and return list of results used for computing metric.
                - ``pred``: Called by custom use to get ``Tensor`` type
                  results.

        Returns:
            dict or list:
                - If ``mode == train``, return a ``dict`` of loss tensor used
                  for backward and logging.
                - If ``mode == eval``, return a ``list`` of inference
                  results.
                - If ``mode == pred``, return a tensor or ``tuple`` of tensor
                  or ``dict`` of tensor for custom use.
        """

    def _run_forward(self, data: Union[dict, tuple, list],
                     mode: str) -> Union[Dict[str, torch.Tensor], list]:
        """Unpacks data for :meth:`forward`

        Args:
            data (dict or tuple or list): Data sampled from dataset.
            mode (str): Mode of forward.

        Returns:
            dict or list: Results of training or testing mode.
        """
        data = self.cast_data(data)
        if isinstance(data, dict):
            results = self(**data, mode=mode)
        elif isinstance(data, (list, tuple)):
            results = self(*data, mode=mode)
        else:
            raise TypeError('Output of `data_preprocessor` should be '
                            f'list, tuple or dict, but got {type(data)}')
        return results

    def cast_data(self, data: CastData) -> CastData:
        """Copying data to the target device.

        Args:
            data (dict): Data returned by ``DataLoader``.

        Returns:
            CollatedResult: Inputs and data sample at target device.
        """
        if isinstance(data, Mapping):
            return {key: self.cast_data(data[key]) for key in data}
        elif isinstance(data, (str, bytes)) or data is None:
            return data
        elif isinstance(data, tuple) and hasattr(data, '_fields'):
            # namedtuple
            return type(data)(
                *(self.cast_data(sample) for sample in data))  # type: ignore  # noqa: E501  # yapf:disable
        elif isinstance(data, Sequence):
            return type(data)(self.cast_data(sample) for sample in data)  # type: ignore  # noqa: E501  # yapf:disable
        elif isinstance(data, (torch.Tensor, BaseDataElement)):
            return data.to(self.device, non_blocking=False)
        else:
            return data
