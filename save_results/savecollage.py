from os import mkdir
from shutil import rmtree

from PIL import ImageFont
from PIL.ImageDraw import Draw
from PIL.Image import new as new_image
from math import ceil
from os.path import join, isdir


def save_collage(filename, crown_dict, mse_dict):

    number_of_crowns = len(crown_dict)
    rows = ceil(number_of_crowns / 4)
    collage = new_image('RGB', (1200, 300 * rows))

    crowns = crown_dict.keys()

    font = ImageFont.truetype("arial.ttf", 15)

    i = 1
    h_offset = 0
    v_offset = 0

    for crown in crowns:
        img = crown_dict[crown].resize((300, 300))
        Draw(img).text((30, 5), crown + ' with error: ' + str(mse_dict[crown]), fill=(255, 255, 255), font=font)
        collage.paste(img, (h_offset, v_offset))
        h_offset += 300
        if i % 4 == 0:
            v_offset += 300
            h_offset = 0
        i += 1

    if isdir(join('saved_files', filename)):
        rmtree(join('saved_files', filename))
    mkdir(join('saved_files', filename))

    collage.save(join('saved_files', filename, 'collage.jpg'))
    print('Collage saved: ' + join('saved_files', filename, 'collage.jpg'))
    collage.show()
    # return collage


def save_images(filename, crown_dict, mse_dict):

    crowns = crown_dict.keys()

    i = 0

    font = ImageFont.truetype("arial.ttf", 15)

    for crown in crowns:
        img = crown_dict[crown].resize((300, 300))
        Draw(img).text((10, 5), crown + ' with error: ' + str(mse_dict[crown]), fill=(255, 255, 255), font=font)
        img.save(join('saved_files', filename, 'crown'+str(i)+'.jpg'))
        print('Saved ' + join('saved_files', filename, 'crown'+str(i)+'.jpg'))
        # img.show()
        i += 1
