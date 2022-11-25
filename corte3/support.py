from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    terrain_map = []
    with open(path) as levelmap:
        layout  =  reader(levelmap,delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map   

def import_folder(path):
    surface_list = []

    for _,__,image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list


