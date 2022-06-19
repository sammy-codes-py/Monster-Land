from csv import reader
from os import walk

import pygame


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surface_list = []
    """walking through the files """
    """_ - folder path, __ - folders we dont need them we need only the files"""
    for _, __, img_files in walk(path):
        for img in img_files:
            """returning full path like: media/some_file.png"""
            full_path = path + '/' + img
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list
