from os import walk
import pygame
from settings import *

def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list


def timer(active = int, cooldown = int, variale = bool):
    current_time = pygame.time.get_ticks()

    if current_time - active >= cooldown:
        active = False

    return active



