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
import sys, os
import requests
from PIL import Image

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

def gif_to_png(img,pokeIdx,genIdx,rows):
    for i,frame in enumerate(iter_frames(img)):
        rows.append(['data/gen%d/%d-%d.png' % (genIdx,pokeIdx,i),genIdx])
        frame.save('gen%d/%d-%d.png' % (genIdx,pokeIdx,i))
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
    rows   = []

    # Loop through all possible pokemon and download image
    for i in range(1,maxPoke):
        if i > d['%d' % genIdx]['max']:
            genIdx += 1

        # Download the gif here
        download_gif(i)

        # Decompose gif into separate images
        img = Image.open('img.gif')
        gif_to_png(img,i,genIdx,rows)

    # Make the labeled CSV here
    csvFile = 'data.csv'
    header = ['image_file','generation_number']
    with open(csvFile,'wt') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


if __name__ == "__main__":
    main()

