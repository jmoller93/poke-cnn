#!/env/python

"""
This is the pokemon downloader for the poke-cnn repository

All images are taken from the following host-site: https://randompokemon.com/

Inputs:
    Nothing
Outputs:
    Downloaded pokemon frames

"""
import csv
import shutil
import sys, os
import requests
import numpy as np
import pokebase as pb
from PIL import Image

# Append pokemon type data to dataset
def get_types(idx):
    types = [x.type.name for x in pb.pokemon(idx).types]
    return types

# Downloader courtesy of https://stackoverflow.com/questions/39534830/how-to-download-this-gifdynamic-by-python
# I realize that may not be the best solution to link, but they did solve my problem...
def download_gif(idx):
    url = 'https://randompokemon.com/sprites/normal/%d.gif' % idx
    response = requests.get(url,stream=True)
    with open('img.gif','wb') as f:
        f.write(requests.get(url).content)
    del response
    return

# Convert gif to mulitple png frames courtesy of https://stackoverflow.com/questions/4904940/python-converting-gif-frames-to-png
def iter_frames(img):
    try:
        i=0
        while True:
            img.seek(i)
            imgframe = img.copy()
            if i==0:
                palette = imgframe.getpalette()
            else:
                imgframe.putpalette(palette)
            yield imgframe
            i+=1
    except EOFError:
        pass

# Split the dataset into training, validation, and testing
def split_dataset(d,types,idx):
    # Save directory information
    dir='./gen%d' % idx
    nfiles=len(next(os.walk(dir))[2])

    # Loop through training, validation, and testing set and sort data accordingly
    for key,val in d.items():
        # Count the number of files
        filelist=next(os.walk(dir))[2]

        # Make the directory if it does not exist
        if not os.path.isdir('%s/%s' % (dir,key)):
            os.mkdir('%s/%s' % (dir,key))

        # Select a random number of files
        files=np.random.choice(filelist,int(val['frac']*nfiles),replace=False)
        for file in files:
            shutil.move('%s/%s' % (dir,file),'%s/%s/%s' % (dir,key,file))
            row = ['data/gen%d/%s/%s' % (idx,key,file),idx]
            poke_idx = file.split('.png')[0]
            # Pokemon database does not yet have info for 8th generation info
            if int(poke_idx) < 808:
                for type in types[poke_idx]:
                    row.append(type)
            val['rows'].append(row)
    return

def gif_to_png(img,pokeIdx,genIdx):
    frames = []
    for frame in iter_frames(img):
        frames.append(frame)
    rand_frame = np.random.randint(0,len(frames))
    frame = frames[rand_frame]
    frame.save('gen%d/%d.png' % (genIdx,pokeIdx))
    return

def main():
    # Max number of pokemon
    maxPoke = 890

    # Dictionary of pokemon from each generation
    d = {'1' : {'min' : 1, 'max' : 151},
         '2' : {'min' : 152, 'max' : 251},
         '3' : {'min' : 252, 'max' : 386},
         '4' : {'min' : 387, 'max' : 493},
         '5' : {'min' : 494, 'max' : 649},
         '6' : {'min' : 650, 'max' : 721},
         '7' : {'min' : 722, 'max' : 809},
         '8' : {'min' : 810, 'max' : 890}
        }

    # Check to make sure the directory for each generation exists
    for key,_ in d.items():
        dnme = 'gen%s' % key
        if not os.path.isdir(dnme):
            os.mkdir(dnme)

    # Initialize the generation index with the first gen
    genIdx = 1

    # The rows will be split into training, validation, and testing dataset
    split   = {'train' : {'rows' : [], 'frac' : 0.70, 'file' : 'data_train.csv'},
               'val'   : {'rows' : [], 'frac' : 0.15, 'file' : 'data_val.csv'},
               'test'  : {'rows' : [], 'frac' : 0.15, 'file' : 'data_test.csv'}
              }

    # Type dictionary
    types  = {}

    # Loop through all possible pokemon and download image
    for i in range(1,maxPoke):

        # 8th gen not yet added to API
        if i < 808:
            types['%d' % i] = get_types(i)

        if i > d['%d' % genIdx]['max']:
            split_dataset(split,types,genIdx)
            genIdx += 1

        # Download the gif here
        download_gif(i)

        # Decompose gif into separate images
        img = Image.open('img.gif')
        gif_to_png(img,i,genIdx)

    # One last split
    split_dataset(split,types,genIdx)

    # Make the labeled CSV here
    header = ['image_file','generation_number','types1','types2']
    for key,val in split.items():
        with open(val['file'],'wt') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(val['rows'])


if __name__ == "__main__":
    main()

