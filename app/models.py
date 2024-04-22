"""Flexible deep neural network model for classification tasks."""

from torch import nn
import torch.nn.functional as F

class FullyConnected(nn.Module):
    """Fully connected neural network model for classification tasks."""
    numClasses=7
    inputSize=16
    def __init__(self,opt):
        super(FullyConnected,self).__init__()
        self.k=None
        if len(opt.fcn)>0:
            self.k=opt.fcn
            for i,ki in enumerate(self.k):
                if i==0:
                    setattr(self,f'fc{i+1}',nn.Linear(self.inputSize,ki))
                else:
                    setattr(self,f'fc{i+1}',nn.Linear(self.k[i-1],ki))
            setattr(self,f'fc{i+2}',nn.Linear(self.k[-1],self.numClasses))
        else:
            self.fc1=nn.Linear(self.inputSize,self.numClasses)

    def forward(self, xb):
        """Forward pass of the model."""
        xb = xb.reshape(-1,self.inputSize)
        if self.k:
            for i in range(len(self.k)):
                xb=F.relu(getattr(self,f'fc{i+1}')(xb))
            x=getattr(self,f'fc{i+2}')(xb)
        else:
            x=self.fc1(xb)
        return x
    