#!/env/python

"""
This is the neural network that will be trained to run the model.

Attributes:
    TBD: Model parameters will change with accuracy on the test set

"""
import torch.nn as nn
import torch.nn.functional as F

# The neural network class model
# this will be changed constantly and updated
class Net(nn.Module):
    def __init__(self,f,p):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(12*12*16, 8)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = x.view(-1, self.num_flat_features(x))
        x = self.fc1(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

