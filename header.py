#header
from random import *
import arcade
import math
from AntClass import Ant
from Main import Task
from typing import Union
from  concurrent.futures import *
from os import *
import time



#main file variables : 

SPRITE_SCALING = 0.5

DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
SCREEN_TITLE = "Ant Sim"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 220

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.1

# How fast the character moves
PLAYER_MOVEMENT_SPEED = 15

ZOOM_INCREMENT = 0.1
MIN_ZOOM = 0.5
MAX_ZOOM = 4

FOOD_DETECTION = 150
CORPS_DETECTION = 75
START_ANT_NB = 20