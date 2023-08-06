# Copyright (c) OpenMMLab. All rights reserved.
import pdb

import torch
import torch.nn as nn
import torch.utils.checkpoint as cp
from mmcv.cnn import (ConvModule, build_activation_layer, constant_init,
                      normal_init)
from mmcv.runner import BaseModule
from torch.nn.modules.batchnorm import _BatchNorm
from psvis.utils import get_root_logger
# from mmcls.models.utils import channel_shuffle, make_divisible
from ..builder import BACKBONES
from mmcv.runner import load_checkpoint
# from ..utils import res_layer
from ..utils import ShuffleLayer, channel_shuffle, make_divisible
from .utils import load_state_dict_from_google_drive
try:
    from torch.hub import load_state_dict_from_url
except ImportError:
    from torch.utils.model_zoo import load_url as load_state_dict_from_url

__all__ = ['shufflenetv1',
           ]

model_url_params = {
    'shufflenetv1': ('',''),
}
model_urls = {
    'shufflenetv1': 'https://huggingface.co/Alice10/psvision/resolve/main/shufflenetv1-ps19.pth',
}
def shufflenetv1(pretrained=False, progress=True, **kwargs):
    return _shufflenet('shufflenetv1', pretrained, progress,
                   **kwargs)

def _shufflenet(arch, pretrained, progress, **kwargs):
    model = ShuffleNetV1(**kwargs)
    if pretrained:
        state_dict = load_state_dict_from_url(model_urls[arch],
                                              progress=progress)
        model.load_state_dict(state_dict)
    # if pretrained:
    #     url_params=model_url_params[arch]
    #     state_dict = load_state_dict_from_google_drive(url_params[0],url_params[1],
    #                                           progress=progress)
    #     model.load_state_dict(state_dict)
    return model

class ShuffleUnit(BaseModule):
    """ShuffleUnit block.

    ShuffleNet unit with pointwise group convolution (GConv) and channel
    shuffle.

    Args:
        in_channels (int): The input channels of the ShuffleUnit.
        out_channels (int): The output channels of the ShuffleUnit.
        groups (int): The number of groups to be used in grouped 1x1
            convolutions in each ShuffleUnit. Default: 3
        first_block (bool): Whether it is the first ShuffleUnit of a
            sequential ShuffleUnits. Default: True, which means not using the
            grouped 1x1 convolution.
        combine (str): The ways to combine the input and output
            branches. Default: 'add'.
        conv_cfg (dict, optional): Config dict for convolution layer.
            Default: None, which means using conv2d.
        norm_cfg (dict): Config dict for normalization layer.
            Default: dict(type='BN').
        act_cfg (dict): Config dict for activation layer.
            Default: dict(type='ReLU').
        with_cp (bool): Use checkpoint or not. Using checkpoint
            will save some memory while slowing down the training speed.
            Default: False.

    Returns:
        Tensor: The output tensor.
    """

    def __init__(self,
                 in_channels,
                 out_channels,
                 groups=3,
                 num_stages=3,
                 out_indices=(0,1,2),
                 first_block=True,
                 combine='add',
                 conv_cfg=None,
                 norm_cfg=dict(type='BN'),
                 act_cfg=dict(type='ReLU'),
                 with_cp=False):
        super(ShuffleUnit, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.first_block = first_block
        self.combine = combine
        self.groups = groups
        self.bottleneck_channels = self.out_channels // 4
        self.with_cp = with_cp


        if self.combine == 'add':
            self.depthwise_stride = 1
            self._combine_func = self._add
            assert in_channels == out_channels, (
                'in_channels must be equal to out_channels when combine '
                'is add')
        elif self.combine == 'concat':
            self.depthwise_stride = 2
            self._combine_func = self._concat
            self.out_channels -= self.in_channels
            self.avgpool = nn.AvgPool2d(kernel_size=3, stride=2, padding=1)
        else:
            raise ValueError(f'Cannot combine tensors with {self.combine}. '
                             'Only "add" and "concat" are supported')

        self.first_1x1_groups = 1 if first_block else self.groups
        self.g_conv_1x1_compress = ConvModule(
            in_channels=self.in_channels,
            out_channels=self.bottleneck_channels,
            kernel_size=1,
            groups=self.first_1x1_groups,
            conv_cfg=conv_cfg,
            norm_cfg=norm_cfg,
            act_cfg=act_cfg)
        # self.g_conv_1x1_compress = nn.Sequential(
        #
        # )

        self.depthwise_conv3x3_bn = ConvModule(
            in_channels=self.bottleneck_channels,
            out_channels=self.bottleneck_channels,
            kernel_size=3,
            stride=self.depthwise_stride,
            padding=1,
            groups=self.bottleneck_channels,
            conv_cfg=conv_cfg,
            norm_cfg=norm_cfg,
            act_cfg=None)

        self.g_conv_1x1_expand = ConvModule(
            in_channels=self.bottleneck_channels,
            out_channels=self.out_channels,
            kernel_size=1,
            groups=self.groups,
            conv_cfg=conv_cfg,
            norm_cfg=norm_cfg,
            act_cfg=None)

        self.act = build_activation_layer(act_cfg)

    @staticmethod
    def _add(x, out):
        # residual connection
        return x + out

    @staticmethod
    def _concat(x, out):
        # concatenate along channel axis
        return torch.cat((x, out), 1)

    def forward(self, x):

        def _inner_forward(x):
            residual = x

            out = self.g_conv_1x1_compress(x)
            out = self.depthwise_conv3x3_bn(out)

            if self.groups > 1:
                out = channel_shuffle(out, self.groups)

            out = self.g_conv_1x1_expand(out)

            if self.combine == 'concat':
                residual = self.avgpool(residual)
                out = self.act(out)
                out = self._combine_func(residual, out)
            else:
                out = self._combine_func(residual, out)
                out = self.act(out)
            return out

        if self.with_cp and x.requires_grad:
            out = cp.checkpoint(_inner_forward, x)
        else:
            out = _inner_forward(x)

        return out


@BACKBONES.register_module()
class ShuffleNetV1(nn.Module):
    """ShuffleNetV1 backbone.

    Args:
        groups (int): The number of groups to be used in grouped 1x1
            convolutions in each ShuffleUnit. Default: 3.
        widen_factor (float): Width multiplier - adjusts the number
            of channels in each layer by this amount. Default: 1.0.
        out_indices (Sequence[int]): Output from which stages.
            Default: (2, )
        frozen_stages (int): Stages to be frozen (all param fixed).
            Default: -1, which means not freezing any parameters.
        conv_cfg (dict, optional): Config dict for convolution layer.
            Default: None, which means using conv2d.
        norm_cfg (dict): Config dict for normalization layer.
            Default: dict(type='BN').
        act_cfg (dict): Config dict for activation layer.
            Default: dict(type='ReLU').
        norm_eval (bool): Whether to set norm layers to eval mode, namely,
            freeze running stats (mean and var). Note: Effect on Batch Norm
            and its variants only. Default: False.
        with_cp (bool): Use checkpoint or not. Using checkpoint will save some
            memory while slowing down the training speed. Default: False.
    """

    stage_blocks = [4, 8, 4]
    arch_settings = {
        1: (ShuffleUnit, (144, 288, 576)),
        2: (ShuffleUnit, (200, 400, 800)),
        3: (ShuffleUnit, (240, 480, 960)),
        4: (ShuffleUnit, (272, 544, 1088)),
        8: (ShuffleUnit, (384, 768, 1536))
    }

    def __init__(self,
                 groups=3,
                 widen_factor=1.0,
                 out_indices=(2, ),
                 frozen_stages=-1,
                 num_stages=3,
                 conv_cfg=None,
                 norm_cfg=dict(type='BN'),
                 act_cfg=dict(type='ReLU'),
                 norm_eval=False,
                 with_cp=False):
        super(ShuffleNetV1, self).__init__()
        # self.stage_blocks = [4, 8, 4]
        self.groups = groups

        for index in out_indices:
            if index not in range(0, 3):
                raise ValueError('the item in out_indices must in '
                                 f'range(0, 3). But received {index}')

        if frozen_stages not in range(-1, 3):
            raise ValueError('frozen_stages must be in range(-1, 3). '
                             f'But received {frozen_stages}')
        self.out_indices = out_indices
        self.frozen_stages = frozen_stages
        self.conv_cfg = conv_cfg
        self.norm_cfg = norm_cfg
        self.act_cfg = act_cfg
        self.norm_eval = norm_eval
        self.with_cp = with_cp
        self.num_stages = num_stages
        assert num_stages >= 1 and num_stages <= 3
        self.out_indices = out_indices
        assert max(out_indices) < num_stages

        # if groups == 1:
        #     channels = (144, 288, 576)
        # elif groups == 2:
        #     channels = (200, 400, 800)
        # elif groups == 3:
        #     channels = (240, 480, 960)
        # elif groups == 4:
        #     channels = (272, 544, 1088)
        # elif groups == 8:
        #     channels = (384, 768, 1536)
        # else:
        #     raise ValueError(f'{groups} groups is not supported for 1x1 '
        #                      'Grouped Convolutions')
        if groups not in ShuffleNetV1.arch_settings.keys():
            raise ValueError(f'{groups} groups is not supported for 1x1 '
                             'Grouped Convolutions')
        self.block,channels=ShuffleNetV1.arch_settings[groups]
        channels=channels[:num_stages]
        channels = [make_divisible(ch * widen_factor, 8) for ch in channels]

        self.in_channels = int(24 * widen_factor)

        self.conv1 = ConvModule(
            in_channels=3,
            out_channels=self.in_channels,
            kernel_size=3,
            stride=2,
            padding=1,
            conv_cfg=conv_cfg,
            norm_cfg=norm_cfg,
            act_cfg=act_cfg)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.layers = nn.ModuleList()
        for i, num_blocks in enumerate(self.stage_blocks[:num_stages]):
            first_block = True if i == 0 else False
            # layer = self.make_layer(channels[i], num_blocks, first_block)
            in_channel_= self.in_channels if i==0 else channels[i-1]
            layer = self.make_shuffle_layer(
                block=self.block,
                in_channels=in_channel_,
                out_channels=channels[i],
                num_blocks=num_blocks,
                first_block=first_block,
                groups=self.groups,
                conv_cfg=self.conv_cfg,
                norm_cfg=self.norm_cfg,
                act_cfg=self.act_cfg,
                with_cp=self.with_cp
            )
            self.layers.append(layer)

    def _freeze_stages(self):
        if self.frozen_stages >= 0:
            for param in self.conv1.parameters():
                param.requires_grad = False
        for i in range(self.frozen_stages):
            layer = self.layers[i]
            layer.eval()
            for param in layer.parameters():
                param.requires_grad = False

    def make_shuffle_layer(self,
                           **kwargs):
        return ShuffleLayer(**kwargs)

    def init_weights(self,pretrained=None):
        # super(ShuffleNetV1, self).init_weights()

        if isinstance(pretrained, str):
            logger = get_root_logger()
            load_checkpoint(self, pretrained, strict=False, logger=logger)
        elif pretrained is None:

            for name, m in self.named_modules():
                if isinstance(m, nn.Conv2d):
                    if 'conv1' in name:
                        normal_init(m, mean=0, std=0.01)
                    else:
                        normal_init(m, mean=0, std=1.0 / m.weight.shape[1])
                elif isinstance(m, (_BatchNorm, nn.GroupNorm)):
                    constant_init(m, val=1, bias=0.0001)
                    if isinstance(m, _BatchNorm):
                        if m.running_mean is not None:
                            nn.init.constant_(m.running_mean, 0)
        else:
            raise TypeError('pretrained must be a str or None')

    # def make_layer(self, out_channels, num_blocks, first_block=False):
    #     """Stack ShuffleUnit blocks to make a layer.
    #
    #     Args:
    #         out_channels (int): out_channels of the block.
    #         num_blocks (int): Number of blocks.
    #         first_block (bool): Whether is the first ShuffleUnit of a
    #             sequential ShuffleUnits. Default: False, which means using
    #             the grouped 1x1 convolution.
    #     """
    #     layers = []
    #     for i in range(num_blocks):
    #         first_block = first_block if i == 0 else False
    #         combine_mode = 'concat' if i == 0 else 'add'
    #         layers.append(
    #             ShuffleUnit(
    #                 self.in_channels,
    #                 out_channels,
    #                 groups=self.groups,
    #                 first_block=first_block,
    #                 combine=combine_mode,
    #                 conv_cfg=self.conv_cfg,
    #                 norm_cfg=self.norm_cfg,
    #                 act_cfg=self.act_cfg,
    #                 with_cp=self.with_cp))
    #         self.in_channels = out_channels
    #
    #     return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.maxpool(x)

        outs = []
        for i, layer in enumerate(self.layers):
            x = layer(x)
            if i in self.out_indices:
                outs.append(x)

        return tuple(outs)

    def train(self, mode=True):
        super(ShuffleNetV1, self).train(mode)
        self._freeze_stages()
        if mode and self.norm_eval:
            for m in self.modules():
                if isinstance(m, _BatchNorm):
                    m.eval()
