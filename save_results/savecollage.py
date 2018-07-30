from PIL.ImageDraw import Draw
from PIL.Image import new as new_image
from math import ceil
from os.path import join
from shutil import rmtree
from os import mkdir

def save_collage(crown_dict, mse_dict):

    rmtree('saved_files')
    mkdir('saved_files')

    number_of_crowns = len(crown_dict)
    rows = ceil(number_of_crowns / 4)
    collage = new_image('RGB', (1200, 300 * rows))

    crowns = crown_dict.keys()

    i = 1
    h_offset = 0
    v_offset = 0

    for crown in crowns:
        img = crown_dict[crown].resize((300, 300))
        Draw(img).text((30, 5), crown + ' with error: ' + str(mse_dict[crown]), fill=(255, 255, 255))
        collage.paste(img, (h_offset, v_offset))
        h_offset += 300
        if i % 4 == 0:
            v_offset += 300
            h_offset = 0
        i += 1

    collage.save(join('saved_files', 'collage.jpg'))
    print('Collage saved: ' + join('saved_files', 'collage.jpg'))
