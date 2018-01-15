#! /usr/bin/env python

from gamelib import main
from gamelib.game import Game
from NEAT.generation import  *
from NEAT.genome import *
from NEAT.gene import *
import pygame
from gamelib import data
import pygame, os
from pygame.locals import *
import numpy as np
import collections
import math
import pickle
import json
import io

from NEAT.gene import *




# pygame.init()
# pygame.mouse.set_visible(0)
# pygame.display.set_icon(pygame.image.load(data.filepath("bowser1.gif")))
# pygame.display.set_caption("Super Mario Python")
# screen = pygame.display.set_mode((640, 480), HWSURFACE | DOUBLEBUF | RESIZABLE)
# pygame.display.set_caption("Box")
#
generation = Generation()
Game(neural_network=generation)

# def evolution_driver():
#     solver =

# print genome
# if all([os.path.isfile(f) for f in filelist]):
#       break
#    else:
#       time.sleep(600)
# i= 5
# filename= "generation_%d.json" % i
#
# with open(filename, 'w') as f:
#     pickle.dump(genome, f)
#
# new_genome = None
# with open(filename, 'r') as f:
#      new_genome = pickle.load(f)
#
# print isinstance(new_genome, Gene)