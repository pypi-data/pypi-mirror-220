import torch.nn.init as init
import torch
from torch import nn
import torch.nn.functional as F
from weathon.dl.registry import MODELS
from weathon.dl.utils.constants import Tasks
from weathon.dl.utils.cv.ocr.common_modules import ConvBNACT, SEBlock, ScaleFeatureSelection


class Im2Seq(nn.Module):
    def __init__(self, in_channels, **kwargs):
        super().__init__()
        self.out_channels = in_channels

    def forward(self, x):
        B, C, H, W = x.shape
        assert H == 1
        x = x.reshape(B, C, H * W)
        x = x.permute((0, 2, 1))
        return x


class EncoderWithRNN(nn.Module):
    def __init__(self, in_channels, **kwargs):
        super(EncoderWithRNN, self).__init__()
        hidden_size = kwargs.get('hidden_size', 256)
        self.out_channels = hidden_size * 2
        self.lstm = nn.LSTM(in_channels, hidden_size, bidirectional=True, num_layers=2, batch_first=True)

    def forward(self, x):
        self.lstm.flatten_parameters()
        x, _ = self.lstm(x)
        return x


class SequenceEncoder(nn.Module):
    def __init__(self, in_channels, encoder_type='rnn', **kwargs):
        super(SequenceEncoder, self).__init__()
        self.encoder_reshape = Im2Seq(in_channels)
        self.out_channels = self.encoder_reshape.out_channels
        if encoder_type == 'reshape':
            self.only_reshape = True
        else:
            support_encoder_dict = {
                'reshape': Im2Seq,
                'rnn': EncoderWithRNN
            }
            assert encoder_type in support_encoder_dict, '{} must in {}'.format(
                encoder_type, support_encoder_dict.keys())

            self.encoder = support_encoder_dict[encoder_type](
                self.encoder_reshape.out_channels, **kwargs)
            self.out_channels = self.encoder.out_channels
            self.only_reshape = False

    def forward(self, x):
        x = self.encoder_reshape(x)
        if not self.only_reshape:
            x = self.encoder(x)

        return x


class DecoderWithRNN(nn.Module):
    def __init__(self, in_channels, **kwargs):
        super().__init__()
        rnn_hidden_size = kwargs.get('hidden_size', 96)
        self.out_channels = rnn_hidden_size * 2
        self.layers = 2
        self.lstm = nn.LSTM(in_channels, rnn_hidden_size, bidirectional=True, batch_first=True, num_layers=self.layers)

    def forward(self, x):
        x = self.lstm(x)[0]
        return x


class Reshape(nn.Module):
    def __init__(self, in_channels, **kwargs):
        super().__init__()
        self.out_channels = in_channels

    def forward(self, x):
        B, C, H, W = x.shape
        x = x.reshape(B, C, H * W)
        x = x.permute((0, 2, 1))  # (NTC)(batch, width, channel)s
        return x


class SequenceDecoder(nn.Module):
    def __init__(self, in_channels, **kwargs):
        super().__init__()
        self.reshape = Reshape(in_channels)
        self.decoder = DecoderWithRNN(in_channels, **kwargs)
        self.out_channels = self.decoder.out_channels

    def forward(self, x):
        x = self.reshape(x)
        x = self.decoder(x)
        return x


@MODELS.register_module(Tasks.ocr_detection, module_name="PSEFPN")
class PSEFPN(nn.Module):
    def __init__(self, in_channels, out_channels=256, inplace=True, **kwargs):
        super().__init__()
        self.out_channels = out_channels * 4
        self.toplayer = ConvBNACT(in_channels=in_channels[3], out_channels=out_channels, kernel_size=1, stride=1,
                                  padding=0, act='relu')
        self.latlayer1 = ConvBNACT(in_channels=in_channels[2], out_channels=out_channels, kernel_size=1, stride=1,
                                   padding=0, act='relu')
        self.latlayer2 = ConvBNACT(in_channels=in_channels[1], out_channels=out_channels, kernel_size=1, stride=1,
                                   padding=0, act='relu')
        self.latlayer3 = ConvBNACT(in_channels=in_channels[0], out_channels=out_channels, kernel_size=1, stride=1,
                                   padding=0, act='relu')
        # Smooth layers
        self.smooth1 = ConvBNACT(in_channels=out_channels, out_channels=out_channels, kernel_size=3, stride=1,
                                 padding=1, act='relu')
        self.smooth2 = ConvBNACT(in_channels=out_channels, out_channels=out_channels, kernel_size=3, stride=1,
                                 padding=1, act='relu')
        self.smooth3 = ConvBNACT(in_channels=out_channels, out_channels=out_channels, kernel_size=3, stride=1,
                                 padding=1, act='relu')

    def forward(self, x):
        c2, c3, c4, c5 = x
        p5 = self.toplayer(c5)
        p4 = self._upsample_add(p5, self.latlayer1(c4))
        p4 = self.smooth1(p4)
        p3 = self._upsample_add(p4, self.latlayer2(c3))
        p3 = self.smooth2(p3)
        p2 = self._upsample_add(p3, self.latlayer3(c2))
        p2 = self.smooth3(p2)
        x = self._upsample_cat(p2, p3, p4, p5)
        return x

    def _upsample_add(self, x, y):
        return F.interpolate(x, size=y.size()[2:], mode='bilinear', align_corners=False) + y

    def _upsample_cat(self, p2, p3, p4, p5):
        h, w = p2.size()[2:]
        p3 = F.interpolate(p3, size=(h, w), mode='bilinear', align_corners=False)
        p4 = F.interpolate(p4, size=(h, w), mode='bilinear', align_corners=False)
        p5 = F.interpolate(p5, size=(h, w), mode='bilinear', align_corners=False)
        return torch.cat([p2, p3, p4, p5], dim=1)


class ConvBnRelu(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True,
                 padding_mode='zeros', inplace=True):
        super().__init__()
        self.conv = nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size,
                              stride=stride, padding=padding, dilation=dilation,
                              groups=groups, bias=bias, padding_mode=padding_mode)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=inplace)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        return x


class FPN(nn.Module):
    def __init__(self, in_channels, out_channels=256, **kwargs):
        """
        :param in_channels: 基础网络输出的维度
        :param kwargs:
        """
        super().__init__()
        inplace = True
        self.conv_out = out_channels
        out_channels = out_channels // 4
        # reduce layers
        self.reduce_conv_c2 = ConvBnRelu(in_channels[0], out_channels, kernel_size=1, inplace=inplace)
        self.reduce_conv_c3 = ConvBnRelu(in_channels[1], out_channels, kernel_size=1, inplace=inplace)
        self.reduce_conv_c4 = ConvBnRelu(in_channels[2], out_channels, kernel_size=1, inplace=inplace)
        self.reduce_conv_c5 = ConvBnRelu(in_channels[3], out_channels, kernel_size=1, inplace=inplace)
        # Smooth layers
        self.smooth_p4 = ConvBnRelu(out_channels, out_channels, kernel_size=3, padding=1, inplace=inplace)
        self.smooth_p3 = ConvBnRelu(out_channels, out_channels, kernel_size=3, padding=1, inplace=inplace)
        self.smooth_p2 = ConvBnRelu(out_channels, out_channels, kernel_size=3, padding=1, inplace=inplace)

        self.conv = nn.Sequential(
            nn.Conv2d(self.conv_out, self.conv_out, kernel_size=3, padding=1, stride=1),
            nn.BatchNorm2d(self.conv_out),
            nn.ReLU(inplace=inplace)
        )
        self.out_channels = self.conv_out

    def forward(self, x):
        c2, c3, c4, c5 = x
        # Top-down
        p5 = self.reduce_conv_c5(c5)
        p4 = self._upsample_add(p5, self.reduce_conv_c4(c4))
        p4 = self.smooth_p4(p4)
        p3 = self._upsample_add(p4, self.reduce_conv_c3(c3))
        p3 = self.smooth_p3(p3)
        p2 = self._upsample_add(p3, self.reduce_conv_c2(c2))
        p2 = self.smooth_p2(p2)

        x = self._upsample_cat(p2, p3, p4, p5)
        x = self.conv(x)
        return x

    def _upsample_add(self, x, y):
        return F.interpolate(x, size=y.size()[2:]) + y

    def _upsample_cat(self, p2, p3, p4, p5):
        h, w = p2.size()[2:]
        p3 = F.interpolate(p3, size=(h, w))
        p4 = F.interpolate(p4, size=(h, w))
        p5 = F.interpolate(p5, size=(h, w))
        return torch.cat([p2, p3, p4, p5], dim=1)


@MODELS.register_module(Tasks.ocr_detection, module_name="FCEFPN")
class FCEFPN(nn.Module):
    """
    This code is refer from:
    https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.3/ppdet/modeling/necks/fpn.py
    """

    def __init__(self,
                 in_channels,
                 out_channels,
                 use_c5=True,
                 ):
        super(FCEFPN, self).__init__()
        self.out_channels = out_channels
        self.use_c5 = use_c5
        self.lateral_convs = nn.ModuleList()
        self.fpn_convs = nn.ModuleList()
        # stage index 0,1,2,3 stands for res2,res3,res4,res5 on ResNet Backbone
        # 0 <= st_stage < ed_stage <= 3
        st_stage = 4 - len(in_channels)
        ed_stage = st_stage + len(in_channels) - 1
        for i in range(st_stage, ed_stage + 1):
            in_c = in_channels[i - st_stage]
            self.lateral_convs.append(nn.Conv2d(
                in_channels=in_c,
                out_channels=out_channels,
                kernel_size=1))

        for i in range(st_stage, ed_stage + 1):
            self.fpn_convs.append(nn.Conv2d(
                in_channels=out_channels,
                out_channels=out_channels,
                kernel_size=3,
                padding=1))

        # add extra conv levels for RetinaNet(use_c5)/FCOS(use_p5)

    def forward(self, body_feats):
        laterals = []
        num_levels = len(body_feats)

        for i in range(num_levels):
            laterals.append(self.lateral_convs[i](body_feats[i]))

        for i in range(1, num_levels):
            lvl = num_levels - i
            upsample = F.interpolate(
                laterals[lvl],
                scale_factor=2.,
                mode='nearest')
            laterals[lvl - 1] += upsample

        fpn_output = []
        for lvl in range(num_levels):
            fpn_output.append(self.fpn_convs[lvl](laterals[lvl]))

        return fpn_output


class DSConv(nn.Module):
    def __init__(self,
                 in_channels,
                 out_channels,
                 kernel_size,
                 padding,
                 stride=1,
                 groups=None,
                 if_act=True,
                 act="relu",
                 **kwargs):
        super(DSConv, self).__init__()
        if groups == None:
            groups = in_channels
        self.if_act = if_act
        self.act = act
        self.conv1 = nn.Conv2d(
            in_channels=in_channels,
            out_channels=in_channels,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding,
            groups=groups,
            bias=False)

        self.bn1 = nn.BatchNorm2d(in_channels)

        self.conv2 = nn.Conv2d(
            in_channels=in_channels,
            out_channels=int(in_channels * 4),
            kernel_size=1,
            stride=1,
            bias=False)

        self.bn2 = nn.BatchNorm2d(in_channels * 4)

        self.conv3 = nn.Conv2d(
            in_channels=int(in_channels * 4),
            out_channels=out_channels,
            kernel_size=1,
            stride=1,
            bias=False)
        self._c = [in_channels, out_channels]
        if in_channels != out_channels:
            self.conv_end = nn.Conv2d(
                in_channels=in_channels,
                out_channels=out_channels,
                kernel_size=1,
                stride=1,
                bias=False)

    def forward(self, inputs):

        x = self.conv1(inputs)
        x = self.bn1(x)

        x = self.conv2(x)
        x = self.bn2(x)
        if self.if_act:
            if self.act == "relu":
                x = F.relu(x)
            elif self.act == "hardswish":
                x = F.hardswish(x)
            else:
                print("The activation function({}) is selected incorrectly.".
                      format(self.act))
                exit()

        x = self.conv3(x)
        if self._c[0] != self._c[1]:
            x = x + self.conv_end(inputs)
        return x


def weights_init(m):
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


@MODELS.register_module(Tasks.ocr_detection, module_name="DBFPN")
class DBFPN(nn.Module):
    def __init__(self, in_channels, out_channels=256, **kwargs):
        """
        :param in_channels: 基础网络输出的维度
        :param kwargs:
        """
        super().__init__()
        inplace = True
        self.out_channels = out_channels
        # reduce layers
        self.in2_conv = nn.Conv2d(in_channels[0], self.out_channels, kernel_size=1, bias=False)
        self.in3_conv = nn.Conv2d(in_channels[1], self.out_channels, kernel_size=1, bias=False)
        self.in4_conv = nn.Conv2d(in_channels[2], self.out_channels, kernel_size=1, bias=False)
        self.in5_conv = nn.Conv2d(in_channels[3], self.out_channels, kernel_size=1, bias=False)
        # Smooth layers
        self.p5_conv = nn.Conv2d(self.out_channels, self.out_channels // 4, kernel_size=3, padding=1, bias=False)
        self.p4_conv = nn.Conv2d(self.out_channels, self.out_channels // 4, kernel_size=3, padding=1, bias=False)
        self.p3_conv = nn.Conv2d(self.out_channels, self.out_channels // 4, kernel_size=3, padding=1, bias=False)
        self.p2_conv = nn.Conv2d(self.out_channels, self.out_channels // 4, kernel_size=3, padding=1, bias=False)

        self.in2_conv.apply(weights_init)
        self.in3_conv.apply(weights_init)
        self.in4_conv.apply(weights_init)
        self.in5_conv.apply(weights_init)
        self.p5_conv.apply(weights_init)
        self.p4_conv.apply(weights_init)
        self.p3_conv.apply(weights_init)
        self.p2_conv.apply(weights_init)

    def _interpolate_add(self, x, y):
        return F.interpolate(x, scale_factor=2) + y

    def _interpolate_cat(self, p2, p3, p4, p5):
        p3 = F.interpolate(p3, scale_factor=2)
        p4 = F.interpolate(p4, scale_factor=4)
        p5 = F.interpolate(p5, scale_factor=8)
        return torch.cat([p5, p4, p3, p2], dim=1)

    def forward(self, x):
        c2, c3, c4, c5 = x
        in5 = self.in5_conv(c5)
        in4 = self.in4_conv(c4)
        in3 = self.in3_conv(c3)
        in2 = self.in2_conv(c2)

        out4 = self._interpolate_add(in5, in4)
        out3 = self._interpolate_add(out4, in3)
        out2 = self._interpolate_add(out3, in2)

        p5 = self.p5_conv(in5)
        p4 = self.p4_conv(out4)
        p3 = self.p3_conv(out3)
        p2 = self.p2_conv(out2)

        x = self._interpolate_cat(p2, p3, p4, p5)
        return x


class RSELayer(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, shortcut=True):
        super(RSELayer, self).__init__()
        self.out_channels = out_channels
        self.in_conv = nn.Conv2d(
            in_channels=in_channels,
            out_channels=self.out_channels,
            kernel_size=kernel_size,
            padding=int(kernel_size // 2),
            bias=False)
        self.se_block = SEBlock(self.out_channels)
        self.shortcut = shortcut

    def forward(self, ins):
        x = self.in_conv(ins)
        if self.shortcut:
            out = x + self.se_block(x)
        else:
            out = self.se_block(x)
        return out


@MODELS.register_module(Tasks.ocr_detection, module_name="RSEFPN")
class RSEFPN(nn.Module):
    def __init__(self, in_channels, out_channels, shortcut=True, **kwargs):
        super(RSEFPN, self).__init__()
        self.out_channels = out_channels
        self.ins_conv = nn.ModuleList()
        self.inp_conv = nn.ModuleList()

        for i in range(len(in_channels)):
            self.ins_conv.append(
                RSELayer(
                    in_channels[i],
                    out_channels,
                    kernel_size=1,
                    shortcut=shortcut))
            self.inp_conv.append(
                RSELayer(
                    out_channels,
                    out_channels // 4,
                    kernel_size=3,
                    shortcut=shortcut))

    def forward(self, x):
        c2, c3, c4, c5 = x

        in5 = self.ins_conv[3](c5)
        in4 = self.ins_conv[2](c4)
        in3 = self.ins_conv[1](c3)
        in2 = self.ins_conv[0](c2)

        # out4 = in4 + F.interpolate(
        #     in5, scale_factor=2, mode="nearest")  # 1/16
        # out3 = in3 + F.interpolate(
        #     out4, scale_factor=2, mode="nearest")  # 1/8
        # out2 = in2 + F.interpolate(
        #     out3, scale_factor=2, mode="nearest")  # 1/4
        out4 = in4 + F.interpolate(in5, scale_factor=2)
        out3 = in3 + F.interpolate(
            out4, scale_factor=2)  # 1/8
        out2 = in2 + F.interpolate(
            out3, scale_factor=2)  # 1/4

        p5 = self.inp_conv[3](in5)
        p4 = self.inp_conv[2](out4)
        p3 = self.inp_conv[1](out3)
        p2 = self.inp_conv[0](out2)

        p5 = F.interpolate(p5, scale_factor=8, mode="nearest")
        p4 = F.interpolate(p4, scale_factor=4, mode="nearest")
        p3 = F.interpolate(p3, scale_factor=2, mode="nearest")

        fuse = torch.cat([p5, p4, p3, p2], dim=1)
        return fuse


@MODELS.register_module(Tasks.ocr_detection, module_name="LKPAN")
class LKPAN(nn.Module):
    def __init__(self, in_channels, out_channels, mode='large', **kwargs):
        super(LKPAN, self).__init__()
        self.out_channels = out_channels

        self.ins_conv = nn.ModuleList()
        self.inp_conv = nn.ModuleList()
        # pan head
        self.pan_head_conv = nn.ModuleList()
        self.pan_lat_conv = nn.ModuleList()

        if mode.lower() == 'lite':
            p_layer = DSConv
        elif mode.lower() == 'large':
            p_layer = nn.Conv2d
        else:
            raise ValueError(
                "mode can only be one of ['lite', 'large'], but received {}".
                format(mode))

        for i in range(len(in_channels)):
            self.ins_conv.append(
                nn.Conv2d(
                    in_channels=in_channels[i],
                    out_channels=self.out_channels,
                    kernel_size=1,
                    bias=False))

            self.inp_conv.append(
                p_layer(
                    in_channels=self.out_channels,
                    out_channels=self.out_channels // 4,
                    kernel_size=9,
                    padding=4,
                    bias=False))

            if i > 0:
                self.pan_head_conv.append(
                    nn.Conv2d(
                        in_channels=self.out_channels // 4,
                        out_channels=self.out_channels // 4,
                        kernel_size=3,
                        padding=1,
                        stride=2,
                        bias=False))
            self.pan_lat_conv.append(
                p_layer(
                    in_channels=self.out_channels // 4,
                    out_channels=self.out_channels // 4,
                    kernel_size=9,
                    padding=4,
                    bias=False))

    def forward(self, x):
        c2, c3, c4, c5 = x

        in5 = self.ins_conv[3](c5)
        in4 = self.ins_conv[2](c4)
        in3 = self.ins_conv[1](c3)
        in2 = self.ins_conv[0](c2)

        out4 = in4 + F.interpolate(
            in5, scale_factor=2, mode="nearest")  # 1/16
        out3 = in3 + F.interpolate(
            out4, scale_factor=2, mode="nearest")  # 1/8
        out2 = in2 + F.interpolate(
            out3, scale_factor=2, mode="nearest")  # 1/4

        f5 = self.inp_conv[3](in5)
        f4 = self.inp_conv[2](out4)
        f3 = self.inp_conv[1](out3)
        f2 = self.inp_conv[0](out2)

        pan3 = f3 + self.pan_head_conv[0](f2)
        pan4 = f4 + self.pan_head_conv[1](pan3)
        pan5 = f5 + self.pan_head_conv[2](pan4)

        p2 = self.pan_lat_conv[0](f2)
        p3 = self.pan_lat_conv[1](pan3)
        p4 = self.pan_lat_conv[2](pan4)
        p5 = self.pan_lat_conv[3](pan5)

        p5 = F.interpolate(p5, scale_factor=8, mode="nearest")
        p4 = F.interpolate(p4, scale_factor=4, mode="nearest")
        p3 = F.interpolate(p3, scale_factor=2, mode="nearest")

        fuse = torch.cat([p5, p4, p3, p2], dim=1)
        return fuse


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


@MODELS.register_module(Tasks.ocr_detection, module_name="DBASF")
class DBASF(nn.Module):
    def __init__(self, in_channels, out_channels=256, **kwargs):
        """
        :param in_channels: 基础网络输出的维度
        :param kwargs:
        """
        super().__init__()
        inplace = True
        self.out_channels = out_channels
        # reduce layers
        self.in2_conv = nn.Conv2d(in_channels[0], self.out_channels, kernel_size=1, bias=False)
        self.in3_conv = nn.Conv2d(in_channels[1], self.out_channels, kernel_size=1, bias=False)
        self.in4_conv = nn.Conv2d(in_channels[2], self.out_channels, kernel_size=1, bias=False)
        self.in5_conv = nn.Conv2d(in_channels[3], self.out_channels, kernel_size=1, bias=False)
        # Smooth layers
        self.p5_conv = nn.Sequential(
            nn.Conv2d(self.out_channels, self.out_channels // 4, kernel_size=3, padding=1, bias=False),
            nn.Upsample(scale_factor=8, mode='nearest'))

        self.p4_conv = nn.Sequential(
            nn.Conv2d(self.out_channels, self.out_channels // 4, kernel_size=3, padding=1, bias=False),
            nn.Upsample(scale_factor=4, mode='nearest'))
        self.p3_conv = nn.Sequential(
            nn.Conv2d(self.out_channels, self.out_channels // 4, kernel_size=3, padding=1, bias=False),
            nn.Upsample(scale_factor=2, mode='nearest'))
        self.p2_conv = nn.Conv2d(self.out_channels, self.out_channels // 4, kernel_size=3, padding=1, bias=False)

        self.concat_attention = ScaleFeatureSelection(out_channels, out_channels // 4,
                                                      attention_type='scale_channel_spatial')

        self.in2_conv.apply(weights_init)
        self.in3_conv.apply(weights_init)
        self.in4_conv.apply(weights_init)
        self.in5_conv.apply(weights_init)
        self.p5_conv.apply(weights_init)
        self.p4_conv.apply(weights_init)
        self.p3_conv.apply(weights_init)
        self.p2_conv.apply(weights_init)

    def weights_init(self, m):
        classname = m.__class__.__name__
        if classname.find('Conv') != -1:
            nn.init.kaiming_normal_(m.weight.data)
        elif classname.find('BatchNorm') != -1:
            m.weight.data.fill_(1.)
            m.bias.data.fill_(1e-4)

    def _upsample_add(self, x, y):
        return F.interpolate(x, scale_factor=2) + y

    def _upsample_cat(self, p2, p3, p4, p5):
        p3 = F.interpolate(p3, scale_factor=2)
        p4 = F.interpolate(p4, scale_factor=4)
        p5 = F.interpolate(p5, scale_factor=8)
        return torch.cat([p5, p4, p3, p2], dim=1)

    def forward(self, x):
        c2, c3, c4, c5 = x
        in5 = self.in5_conv(c5)
        in4 = self.in4_conv(c4)
        in3 = self.in3_conv(c3)
        in2 = self.in2_conv(c2)

        out4 = self._upsample_add(in5, in4)
        out3 = self._upsample_add(out4, in3)
        out2 = self._upsample_add(out3, in2)

        p5 = self.p5_conv(in5)
        p4 = self.p4_conv(out4)
        p3 = self.p3_conv(out3)
        p2 = self.p2_conv(out2)

        fuse = torch.cat((p5, p4, p3, p2), 1)
        fuse = self.concat_attention(fuse, [p5, p4, p3, p2])

        return fuse
