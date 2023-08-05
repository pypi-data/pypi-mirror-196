import torch
import torch.nn as nn
import torchvision.transforms.functional as TF

from pathlib import Path

class DoubleConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(DoubleConv, self).__init__() # NOTE Check if working
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, 1, 1, bias = False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, 1, 1, bias = False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )

        self.initialize_weights()

    def forward(self, x):
        return self.conv(x)
    
    def initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.xavier_uniform_(m.weight)
            
            if isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            

class SELayer(nn.Module):
    """"https://github.com/moskomule/senet.pytorch/blob/master/senet/se_module.py"""
    def __init__(self, channel, reduction=16):
        super(SELayer, self).__init__()

        reduction = channel if channel // reduction == 0 else 16
        
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channel, channel // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channel // reduction, channel, bias=False),
            nn.Sigmoid()
        )

        self.initialize_weights()
    
    def forward(self, x): # NOTE Weird forward, don't know these functions
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y)
        y = y.view(b, c, 1, 1)
        return x * y.expand_as(x)

    def initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
            

class MainNET(nn.Module):
    def __init__(self, in_channels, out_channels, features=[64,128,256,512]):
        super(MainNET, self).__init__()

        self.predown = SELayer(in_channels)
        self.downs = nn.ModuleList()
        self.ups = nn.ModuleList()
        
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        for feature in features: # One Module per feature
            self.downs.append(DoubleConv(in_channels, feature))
            in_channels = feature

        for feature in reversed(features): # Two Modules per feature
            self.ups.append(nn.ConvTranspose2d(2*feature, feature, kernel_size=2, stride=2))
            self.ups.append(DoubleConv(2*feature, feature))
    
        self.bottleneck = DoubleConv(features[-1], 2*features[-1])
        self.out = nn.Conv2d(features[0], out_channels, kernel_size=1)

        self.initialize_weights()


    def forward(self, x):
        x = self.predown(x)

        skip_connections = []
        for down in self.downs:
            x = down(x)
            skip_connections.append(x)
            x = self.pool(x)

        x = self.bottleneck(x)
        
        for idx, skip_connection in enumerate(reversed(skip_connections)):
            x = self.ups[2*idx](x)

            if x.shape != skip_connection.shape:
                x = TF.resize(x, size=skip_connection.shape[2:])

            concat_skip = torch.cat((skip_connection, x), dim=1)
            x = self.ups[2*idx + 1](concat_skip)
        
        return self.out(x)

    def initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.ConvTranspose2d):
                nn.init.xavier_uniform_(m.weight)

            if isinstance(m, nn.Conv2d):
                nn.init.xavier_uniform_(m.weight)


class FloodsensModel():
    def __init__(self, path, name=None, means=None, stds=None, channels=None, device="cpu"):
        model_dict = torch.load(path, map_location=torch.device(device))
        self.path = Path(path)

        self.name = self.path.stem if name is None else name
        self.means = means if means is not None else model_dict["model_means"]
        self.stds = stds if stds is not None else model_dict["model_stds"]

        if channels is not None:
            self.channels = channels
        elif len(self.stds) == 14:
            self.channels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.path}, {self.name}, {self.channels}, {self.means}, {self.stds})'.format(self=self)
    
    def __str__(self) -> str:
        s = f"\tName: {self.name}\n" 
        s += f"\t\tPath: {self.path}\n" 
        s += f"\t\tNumber of Channels: {len(self.channels)}\n" 

        return s