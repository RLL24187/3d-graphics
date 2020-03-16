from display import *
from draw import *
from parsefile import *
from matrix import *
import math

screen = new_screen()
color = [ 0, 100, 255 ]
edges = []
transform = new_matrix()

parse_file( 'script', edges, transform, screen, color )
