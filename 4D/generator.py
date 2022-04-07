import numpy as np
import argparse
import os
import cv2
import matplotlib.pyplot as plt

import maze_algorithms as mazes
import utilities as util

parser = argparse.ArgumentParser()
parser.add_argument('generator_type', type=str, help='what type of generator')
parser.add_argument('--width', metavar='w', type=int, default=3, help='width of maze (x-axis)')
parser.add_argument('--height', metavar='h', type=int, default=3, help='height of maze (y-axis)')
parser.add_argument('--length', metavar='l', type=int, default=3, help='length of maze (z-axis)')
parser.add_argument('--time', metavar='t', type=int, default=3, help='time frame of maze (t-axis)')
parser.add_argument('--show_steps', type=bool, default=False, help='show slideshow of steps taken')
parser.add_argument('--output_file', type=str, default="null", help='output file')
args = parser.parse_args()

def display_grid(grid):
    img = util.create_viewer_image(grid, 5)
    resized = cv2.resize(img, (600,600), interpolation = cv2.INTER_AREA)

    cv2.imshow('Maze', resized)
    cv2.waitKey(0)
    return

def output_data(filename, grid):
    ext = os.path.splitext(filename)[-1]
    if ext == ".txt":
        util.output_txt_file(filename, grid)
    else:
        print("Error: Unsupported Output File Type...")
        

def main():   
    maze = mazes.get_gen(args.generator_type)(args.width, args.height, args.length, args.time)
    maze.generate()

    if args.show_steps:
        for m in maze.step_array:
            display_grid(m)
    else:
        display_grid(maze.grid)
      
    read, write, time_taken = maze.get_stats()
    print("Read Instruction: ", read)
    print("Write Instructions: ", write)
    print("Time Taken: ", time_taken)
    
    if args.output_file != "null":
        output_data(args.output_file, maze.grid)


if __name__ == '__main__':
    main()