from PIL import Image
from os import listdir
from os.path import isfile, isdir, join
import sys
import argparse
import math
import re

def calculate_grid(imgs: list) -> list[int]:
    total = len(imgs)
    m = math.floor(math.sqrt(total)) # rows
    n = total // m + (1 if total % m else 0) # cols

    return [m, n]

def calculate_canvas(tile, grid_dims):
    cols, rows, padding = grid_dims
    canvas_width = tile.width * cols + (padding * cols) - padding
    canvas_height = tile.height * rows + (padding * rows) - padding
    return Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255))

def combine_images(padding, images, basedir, grid_dims=None, rotation=180, standardized=True):
    if not grid_dims: # calculate dims if not provided
        rows, cols = calculate_grid(images)
    if not standardized: # calculate max dims
        width_max = max([Image.open(basedir + image).width for image in images])
        height_max = max([Image.open(basedir + image).height for image in images])
    else:
        tile0 = Image.open(basedir + images[0])
        width_max = tile0.width
        height_max = tile0.height
    canvas = calculate_canvas(tile0, (cols, rows, padding))

    x = 0
    y = 0
    for i, image in enumerate(images):
        img = Image.open(basedir + image)
        img = img.rotate(rotation) # rotate image
        x_offset = 0
        y_offset = 0
        if not standardized:
            x_offset = int((width_max-img.width)/2)
            y_offset = int((height_max-img.height)/2)
        canvas.paste(img, (x+x_offset, y+y_offset))
        x += width_max + padding
        if (i+1) % cols == 0:
            y += height_max + padding
            x = 0
    canvas.save(basedir + 'image_grid.png')

def main():
    # parse args
    parser = argparse.ArgumentParser(description="Formats images in given directory as a grid of images. Can provide grid size or size automatically.")
    parser.add_argument("path", default="./")
    parser.add_argument("-d", "--dimensions", nargs=2, type=int)
    parser.add_argument("-r", "--rotation", type=int, default=180)
    parser.add_argument("-ns", action="store_true")
    args = parser.parse_args()
    print(args)
    
    # config
    if isdir(args.path):
        imgdir = args.path
    else: 
        raise RuntimeError(f'{args.path} is not a valid directory!')
    
    sort_key = lambda f: int(re.search("(?:_|-)([0-9]+).tif", f).group(1)) # key for sorting images into order - modify as necessary
    try:
        imgs = sorted([ f for f in listdir(imgdir) if isfile(join(imgdir, f)) ], key=sort_key)
    except AttributeError as e:
        if "no attribute \'group\'" in str(e):
            raise ValueError(
                ("Please ensure the target directory contains only tifs and that "
                 "filenames end in a number following an underscore or hyphen (i.e. KA331_1.tif)"))
        else: raise
    
    # create grid
    combine_images(50, imgs, imgdir, args.dimensions, args.rotation, not args.ns)
    print(f'Done with {imgdir}!')

    return 0

if __name__ == "__main__":
    sys.exit(main())