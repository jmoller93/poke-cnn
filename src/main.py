#!/env/python

"""
This is the main script to train and optimize the neural network

Args:
    TBD

"""

# Import necessary libraries
import os
import time
import copy
import argparse
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torch.utils.data import Dataset, DataLoader

# Import local classes
from hyperparams import HyperParameters
from dataset import PokemonDataset
from transform import *
from nnet import Net

# Model trainer from https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
def train_model(model, loaders, criterion, optimizer, scheduler, device,batch_size, num_epochs=25):
    since = time.time()

    # Load best possible model
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    # Loop through training epochs
    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        # Loop through evaluation and training
        for phase in ['train','val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            elif phase == 'val':
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data.
            for i,data in enumerate(loaders[phase],0):
                image, label = data['image'], data['generation']
                image = image.to(device)
                label = label.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(image)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, label)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # Capture running statistics
                running_loss += loss.item() * image.size(0)
                running_corrects += torch.sum(preds == label.data)

            # After each training epoch move the scheduler forward
            if phase == 'train':
                scheduler.step()

            # Calculate loss and accuracy for each
            epoch_loss = running_loss / len(loaders[phase]) / float(batch_size)
            epoch_acc = running_corrects.double() / len(loaders[phase]) / float(batch_size)

            # Print the loss
            print('Loss: {:.4f} Acc: {:.4f}'.format(epoch_loss, epoch_acc))

            # Save best version of the model on validation set
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())


    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))

    return model

def main():
    # Parse the inputs
    parser = argparse.ArgumentParser(description='Inputs for the neural network trainer')
    parser.add_argument('--n_epoch','-n',type=int,help='Number of epochs to train the network with',required=True)
    args = parser.parse_args()

    # Trying to see if this fixes a small bug
    torch.set_default_tensor_type('torch.DoubleTensor')

    # Make sure files exists
    labels = ['train','test','val']
    for label in labels:
        fnme = '../data_' + label + '.csv'
        if not os.path.isfile(fnme):
            raise EnvironmentError("File %s is not found!\n Please run the poke_downloader.py script in the data directory!\n" % fnme)

    # Initialize the dataset
    train_dataset = PokemonDataset('../data_train.csv','../',
            transform=transforms.Compose([Rescale(32),
                                          RandomCrop(30),
                                          ToTensor()
                                         ])
                                    )
    val_dataset = PokemonDataset('../data_val.csv','../',
            transform=transforms.Compose([Rescale(32),
                                          RandomCrop(30),
                                          ToTensor()
                                          ])
                                  )

    # Initialize the hyperparameters
    hyperparams = HyperParameters()

    # Dataloaders
    trainloader = torch.utils.data.DataLoader(train_dataset, batch_size=hyperparams.batch_size,shuffle=True,num_workers=hyperparams.num_workers)
    valloader   = torch.utils.data.DataLoader(val_dataset, batch_size=hyperparams.batch_size,shuffle=True,num_workers=hyperparams.num_workers)

    loaders = {'train' : trainloader,
               'val'   : valloader
              }

    # Initialize the neural net
    model = Net(hyperparams.filter_size,hyperparams.pool_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer,step_size=7,gamma=0.1)

    # Send the network to gpu if available
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Train the neural net for the appropriate number of epochs
    model = train_model(model, # Neural net
                        loaders, # Data (for now it is only training data)
                        criterion, # Loss criteria
                        optimizer, # Optimization routine
                        exp_lr_scheduler, # Learning rate scheduler
                        device, # Which device is this being run on
                        hyperparams.batch_size, # Size of batches
                        num_epochs=args.n_epoch # Number of epochs
                       )

    return

if __name__ == "__main__":
    main()
