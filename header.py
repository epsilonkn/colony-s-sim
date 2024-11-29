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
from engineering import *



#main file variables : 

SPRITE_SCALING = 0.5

DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
SCREEN_TITLE = "Ant Sim"


VIEWPORT_MARGIN = 220

CAMERA_SPEED = 0.1

PLAYER_MOVEMENT_SPEED = 15

ZOOM_INCREMENT = 0.1
MIN_ZOOM = 0.5
MAX_ZOOM = 4

OBJECT_DETECTION = 150
CORPS_DETECTION = 75
START_ANT_NB = 15


#engineer file :

DEFENSE_COEF = 1
STORAGE_COEF = 0.7
RESEARCH_COEF = 0.7
DRONE_BUILD_COEF = 0.7
MIN_POPU = 15
MAX_POPU = 25

SEUIL_ACTIVATION = 0.5