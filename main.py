import numpy as np
import cv2
import argparse

import maze_algorithms as mazes
import utilities as util

parser = argparse.ArgumentParser()
parser.add_argument('generator_type', type=str, help='what type of generator')
parser.add_argument('--width', metavar='w', type=int, default=5, help='width of maze')
parser.add_argument('--height', metavar='h', type=int, default=5, help='height of maze')
args = parser.parse_args()

maze = mazes.get_gen(args.generator_type)(args.width, args.height)
maze.generate()

for m in maze.step_array:
    img = util.convert_maze_to_image_array(m)
    resized = cv2.resize(img, (600,600), interpolation = cv2.INTER_AREA)

    cv2.imshow('Maze', resized)
    cv2.waitKey(0)
    
    
'''
img = np.zeros([256,256,3])

img[:,:,0] = np.ones([256,256])
img[:,:,1] = np.ones([256,256]) * 0.0
img[:,:,2] = np.ones([256,256])

cv2.imshow('Color image', img)
cv2.waitKey(0)
'''