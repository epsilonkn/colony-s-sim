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

UPDATE_RATE = 50

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

START_FOOD = 20
START_IRON = 10
START_COPPER = 10
START_SILICIUM = 10

OBJECT_DETECTION = 150
CORPS_DETECTION = 75
START_ANT_NB = 20
CELLAR_CAPACITY = 100
WAREHOUSE_CAPACITY = 100


#engineer file :