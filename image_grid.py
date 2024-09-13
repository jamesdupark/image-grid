from PIL import Image
from os import listdir
from os.path import isfile, join
import sys
import argparse
import math
import re

def calculate_grid(imgs: list) -> list[int]:
    total = len(imgs)
    n = math.floor(math.sqrt(total)) # cols
    m = total // n + 1 # rows

    return [m, n]

def calculate_canvas(tile):
    canvas_width = tile.width * cols + (padding * cols) - padding
    canvas_height = tile.height * rows + (padding * rows) - padding
    return Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255))

def combine_images(columns, padding, images, basedir, rows=0, rotation=180, standardized=True):
    if not rows: # calculate number of rows
        rows = len(images) // columns
        if len(images) % columns:
            rows += 1
    if not standardized: # calculate max dims
        width_max = max([Image.open(basedir + image).width for image in images])
        height_max = max([Image.open(basedir + image).height for image in images])
    else:
        tile0 = Image.open(basedir + images[0])
        width_max = tile0.width
        height_max = tile0.height
    canvas = calculate_canvas(tile0)

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
        if (i+1) % columns == 0:
            y += height_max + padding
            x = 0
    canvas.save(basedir + 'image_grid.png')

def main():
    # parse args
    parser = argparse.ArgumentParser(description="Formats equally sized images in given directory as a grid of images. Can provide grid size or size automatically.")
    parser.add_argument("path", default="./")
    parser.add_argument("-d", "--dimensions", nargs=2, type=int)
    args = parser.parse_args()
    
    # config
    imgdir = args.path
    sort_key = lambda n: int(re.search("_([0-9]+).tif", n).group(1)) # key for sorting images into order - modify as necessary
    imgs = sorted([ f for f in listdir(imgdir) if isfile(join(imgdir, f)) ], key=sort_key)
    m, n = args.dimensions if args.dimensions else calculate_grid(imgs)
    # print(imgs)

    # create grid
    combine_images(n, 50, imgs, imgdir)
    print(f'Done with {imgdir}!')

    return 0

if __name__ == "__main__":
    sys.exit(main())