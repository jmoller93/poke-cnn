#!/env/python

"""
This is the dataset class for the classification routine.
It will have to perform transformations on the images

Attributes:
    __get__: Gets an item
    __init__: Initializes the class
    __len__: Length of the dataset

"""
import os
import torch
import pandas as pd

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
        image = io.imread(img_name)
        gen   = self.pokmeon_frame.iloc[idx, 1:]
        sample = {'image': image, 'generation': gen}

        if self.transform:
            sample = self.transform(sample)

        return sample
