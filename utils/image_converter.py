import glob
import os

from PIL import Image, UnidentifiedImageError


def convert(path='sprites/front'):
    """ Convert the .png files in the given directory from RGBA to RGB
    """
    base_dir = os.getcwd()
    os.chdir(path)
    for file in glob.glob('*.png'):
        try:
            with Image.open(file).convert('RGB') as img:
                img.save(file)
        except UnidentifiedImageError:
            print(f'Could not identify image in {file}')
    os.chdir(base_dir)



if __name__ == '__main__':
    # convert('sprites/front')
    # convert('sprites/back')
    ...