#!/env/python

"""
This is the dataset class for the classification routine.
It will have to perform transformations on the images

Attributes:
    __getitem__: Gets an item
    __init__: Initializes the class
    __len__: Length of the dataset

"""
import os
import torch
import numpy as np
import pandas as pd
from skimage import io, transform
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils

# Type dictionary
d = {'fire' : 0,
     'water' : 1,
     'grass' : 2,
     'rock'  : 3,
     'electric' : 4,
     'bug' : 5,
     'ground' : 6,
     'normal' : 7,
     'poison' : 8,
     'psychic' : 9,
     'ghost' : 10,
     'dark' : 11,
     'flying' : 12,
     'fighting' : 13,
     'steel' : 14,
     'ice' : 15,
     'fairy' : 16,
     'dragon' : 17 }

# Primarily generated from the pytorch tutorial: https://pytorch.org/tutorials/beginner/data_loading_tutorial.html
class PokemonDataset(Dataset):
    """Pokemon images dataset."""

    def __init__(self, csv_file, root_dir, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.pokemon_frame = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.pokemon_frame)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = os.path.join(self.root_dir,
                                self.pokemon_frame.iloc[idx, 0])
        poke_image = io.imread(img_name)
        gen   = self.pokemon_frame.iloc[idx, 1] - 1
        type  = d[self.pokemon_frame.iloc[idx, 2]]
        sample = {'image': poke_image[:,:,:3], 'generation': gen ,'typing' : type}

        if self.transform:
            sample = self.transform(sample)

        return sample
