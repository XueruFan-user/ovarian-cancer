""" Full assembly of the parts to form the complete network """

from .unet_parts import *


class KiteNet(nn.Module):
    def __init__(self, n_channels=1, n_classes=2, bilinear=False):
        super(KiteNet, self).__init__()
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.bilinear = bilinear

        self.inc = (DoubleConv(n_channels, 64))
        factor = 2 if bilinear else 1
        self.up1 = (Up(64, 128 // factor, bilinear))
        self.up2 = (Up(128, 256 // factor, bilinear))
        self.up3 = (Up(256, 512 // factor, bilinear))
        self.up4 = (Up(512, 1024, bilinear))
        self.down1 = (Down(1024, 512))
        self.down2 = (Down(512, 256))
        self.down3 = (Down(256, 128))
        self.down4 = (Down(128, 64))


    def forward(self, x):
        x1 = self.inc(x)
        x2 = self.up1(x1)
        x3 = self.up2(x2)
        x4 = self.up3(x3)
        x5 = self.up4(x4)
        x = self.down1(x5, x4)
        x = self.down2(x, x3)
        x = self.down3(x, x2)
        x = self.down4(x, x1)

        return x

    def use_checkpointing(self):
        self.inc = torch.utils.checkpoint(self.inc)
        self.down1 = torch.utils.checkpoint(self.down1)
        self.down2 = torch.utils.checkpoint(self.down2)
        self.down3 = torch.utils.checkpoint(self.down3)
        self.down4 = torch.utils.checkpoint(self.down4)
        self.up1 = torch.utils.checkpoint(self.up1)
        self.up2 = torch.utils.checkpoint(self.up2)
        self.up3 = torch.utils.checkpoint(self.up3)
        self.up4 = torch.utils.checkpoint(self.up4)
        self.outc = torch.utils.checkpoint(self.outc)