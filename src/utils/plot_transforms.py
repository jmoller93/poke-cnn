#!/env/python

"""
Function to plot a reshaped batch of figures

Args:
    TBD

"""

# Import libraries
from __future__ import print_function, division
import os,sys
from skimage import io, transform
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils

# Import local files
sys.path.append('/home/jmoller/Documents/poke-cnn/src/')
from dataset import PokemonDataset
from transform import *

plt.ion()   # interactive mode

scale = Rescale(32)
crop = RandomCrop(30)
composed = transforms.Compose([Rescale(32),
                               RandomCrop(30)])

# Load dataset
pokemon_dataset = PokemonDataset('../../data_train.csv','../../')

# Apply each of the above transforms on sample.
fig = plt.figure()
sample = pokemon_dataset[65]
for i, tsfrm in enumerate([scale, crop, composed]):
    transformed_sample = tsfrm(sample)

    ax = plt.subplot(1, 3, i + 1)
    plt.tight_layout()
    ax.set_title(type(tsfrm).__name__)
    plt.imshow(transformed_sample['image'])

plt.savefig('transforms.png')

