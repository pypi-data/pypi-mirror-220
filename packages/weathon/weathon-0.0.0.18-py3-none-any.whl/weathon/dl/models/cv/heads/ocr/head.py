import torch
from functools import partial
from torch import nn
import torch.nn.functional as F

from weathon.dl.registry import MODELS
from weathon.dl.utils.constants import Tasks
from weathon.dl.utils.cv.ocr.common_modules import ConvBNACT


class Head(nn.Module):
    def __init__(self, in_channels):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=in_channels, out_channels=in_channels // 4, kernel_size=3, padding=1,
                               bias=False)
        # self.conv1 = nn.Conv2d(in_channels=in_channels, out_channels=in_channels // 4, kernel_size=5, padding=2,
        #                        bias=False)
        self.conv_bn1 = nn.BatchNorm2d(in_channels // 4)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.ConvTranspose2d(in_channels=in_channels // 4, out_channels=in_channels // 4, kernel_size=2,
                                        stride=2)
        self.conv_bn2 = nn.BatchNorm2d(in_channels // 4)
        self.conv3 = nn.ConvTranspose2d(in_channels=in_channels // 4, out_channels=1, kernel_size=2, stride=2)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv_bn1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.conv_bn2(x)
        x = self.relu(x)
        x = self.conv3(x)
        x = torch.sigmoid(x)
        return x


def weights_init(m):
    import torch.nn.init as init
    if isinstance(m, nn.Conv2d):
        init.kaiming_normal_(m.weight.data)
        if m.bias is not None:
            init.normal_(m.bias.data)
    elif isinstance(m, nn.ConvTranspose2d):
        init.kaiming_normal_(m.weight.data)
        if m.bias is not None:
            init.normal_(m.bias.data)
    elif isinstance(m, nn.BatchNorm2d):
        init.normal_(m.weight.data, mean=1, std=0.02)
        init.constant_(m.bias.data, 0)

@MODELS.register_module(Tasks.ocr_detection, module_name="DBHead")
class DBHead(nn.Module):
    """
    Differentiable Binarization (DB) for text detection:
        see https://arxiv.org/abs/1911.08947
    args:
        params(dict): super parameters for build DB network
    """

    def __init__(self, in_channels, k=50):
        super().__init__()
        self.k = k
        self.binarize = Head(in_channels)
        self.thresh = Head(in_channels)
        self.binarize.apply(weights_init)
        self.thresh.apply(weights_init)

    def step_function(self, x, y):
        return torch.reciprocal(1 + torch.exp(-self.k * (x - y)))

    def forward(self, x):
        shrink_maps = self.binarize(x)
        if not self.training:
            return shrink_maps
        threshold_maps = self.thresh(x)
        binary_maps = self.step_function(shrink_maps, threshold_maps)
        y = torch.cat((shrink_maps, threshold_maps, binary_maps), dim=1)
        return y


def multi_apply(func, *args, **kwargs):
    pfunc = partial(func, **kwargs) if kwargs else func
    map_results = map(pfunc, *args)
    return tuple(map(list, zip(*map_results)))

@MODELS.register_module(Tasks.ocr_detection, module_name="FCEHead")
class FCEHead(nn.Module):
    """The class for implementing FCENet head.
    FCENet(CVPR2021): Fourier Contour Embedding for Arbitrary-shaped Text
    Detection.

    [https://arxiv.org/abs/2104.10442]

    Args:
        in_channels (int): The number of input channels.
        scales (list[int]) : The scale of each layer.
        fourier_degree (int) : The maximum Fourier transform degree k.
    """

    def __init__(self, in_channels, fourier_degree=5):
        super().__init__()
        assert isinstance(in_channels, int)

        self.downsample_ratio = 1.0
        self.in_channels = in_channels
        self.fourier_degree = fourier_degree
        self.out_channels_cls = 4
        self.out_channels_reg = (2 * self.fourier_degree + 1) * 2

        self.out_conv_cls = nn.Conv2d(
            in_channels=self.in_channels,
            out_channels=self.out_channels_cls,
            kernel_size=3,
            stride=1,
            padding=1,
            groups=1,
            bias=True)
        self.out_conv_reg = nn.Conv2d(
            in_channels=self.in_channels,
            out_channels=self.out_channels_reg,
            kernel_size=3,
            stride=1,
            padding=1,
            groups=1,
            bias=True)

    def forward(self, feats, targets=None):
        cls_res, reg_res = multi_apply(self.forward_single, feats)
        level_num = len(cls_res)
        outs = {}
        if not self.training:
            for i in range(level_num):
                tr_pred = F.softmax(cls_res[i][:, 0:2, :, :], dim=1)
                tcl_pred = F.softmax(cls_res[i][:, 2:, :, :], dim=1)
                outs['level_{}'.format(i)] = torch.cat(
                    [tr_pred, tcl_pred, reg_res[i]], dim=1)
        else:
            preds = [[cls_res[i], reg_res[i]] for i in range(level_num)]
            outs['levels'] = preds
        return outs

    def forward_single(self, x):
        cls_predict = self.out_conv_cls(x)
        reg_predict = self.out_conv_reg(x)
        return cls_predict, reg_predict

@MODELS.register_module(Tasks.ocr_detection, module_name="PseHead")
class PseHead(nn.Module):
    def __init__(self, in_channels, result_num=6, **kwargs):
        super(PseHead, self).__init__()
        self.H = kwargs.get('H', 640)
        self.W = kwargs.get('W', 640)
        self.scale = kwargs.get('scale', 1)
        self.conv = ConvBNACT(in_channels, in_channels // 4, kernel_size=3, padding=1, stride=1, act='relu')
        self.out_conv = nn.Conv2d(in_channels // 4, result_num, kernel_size=1, stride=1)

    def forward(self, x):
        x = self.conv(x)
        x = self.out_conv(x)
        if self.train:
            x = F.interpolate(x, size=(self.H, self.W), mode='bilinear', align_corners=True)
        else:
            x = F.interpolate(x, size=(self.H // self.scale, self.W // self.scale), mode='bilinear', align_corners=True)
        return x


class CTC(nn.Module):
    def __init__(self, in_channels, n_class, **kwargs):
        super().__init__()
        self.fc = nn.Linear(in_channels, n_class)
        self.n_class = n_class

    def forward(self, x):
        return self.fc(x)
