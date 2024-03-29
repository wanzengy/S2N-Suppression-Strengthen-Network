import torch
import torch.nn as nn
import torch.nn.functional as F

class ResidualBlock(nn.Module):
    def __init__(self, inchannel, outchannel, stride=1):
        super(ResidualBlock, self).__init__()
        self.left = nn.Sequential(
            nn.Conv2d(inchannel, outchannel, kernel_size=3, stride=stride, padding=1),
            nn.BatchNorm2d(outchannel),
            nn.ReLU(inplace=True),
            nn.Conv2d(outchannel, outchannel, kernel_size=3, padding=1),
            nn.BatchNorm2d(outchannel)
        )
        self.shortcut = nn.Sequential()

    def forward(self, x):
        # print("x:" + str(x.shape))
        out = self.left(x)
        # print("out: " +str(out.shape))
        out += self.shortcut(x)
        out = F.relu(out)
        return out

class Model(nn.Module):
    def __init__(self, num_classes=10, in_channels=2, **kwargs):
        super().__init__()
        
        self.features = nn.Sequential(
            nn.Conv2d(in_channels, 64, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 512, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            ResidualBlock(512, 512),
            ResidualBlock(512, 512),
            nn.AdaptiveAvgPool2d((16, 16)),
        )

        self.classifier = nn.Sequential(
            # nn.Dropout(),
            # nn.Linear(num_channel*16*5*5,128),
            # nn.ReLU(inplace=True),
            # nn.Dropout(),
            # nn.Linear(128,10),
            nn.Linear(16*16*512, 1024),
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(1024),
            nn.Dropout(),
            nn.Linear(1024, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(512, num_classes),
        )


    def forward(self,x):
        x=self.features(x)
        x=torch.flatten(x, 1)
        # x = x[0].view(-1, self.fc1.weight.size(1))
        x = self.classifier(x)
        return x

if __name__ == '__main__':
    image = torch.randn([1,4,128,128])
    net = Model(10, 4)
    net(image)
    # print(net.named_modules)