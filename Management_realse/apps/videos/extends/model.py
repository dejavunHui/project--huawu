import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):

    def __init__(self,scale):
        super(Net,self).__init__()

        self.conv1 = nn.Conv2d(1,64,(5,5),(1,1),(2,2))
        self.conv2 = nn.Conv2d(64,64,(3,3),(1,1),(1,1))
        self.conv3 = nn.Conv2d(64,32,(3,3),(1,1),(1,1))
        self.conv4 = nn.Conv2d(32,1 * scale * scale,(3,3),(1,1),(1,1))
        self.pixel_shuffle = nn.PixelShuffle(scale)

    def forward(self,x):

        x = F.tanh(self.conv1(x))
        x = F.tanh(self.conv2(x))
        x = F.tanh(self.conv3(x))
        x = F.sigmoid(self.pixel_shuffle(self.conv4(x)))
        return x


if __name__ == '__main__':

    net = Net(3)
    print(net)