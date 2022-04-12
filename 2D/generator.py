import numpy as np
import cv2
import argparse
import os

from PIL import Image
import maze_algorithms as mazes
import utilities as util


parser = argparse.ArgumentParser()
parser.add_argument('generator_type', type=str, help='what type of generator (kruskals, prims, recursive_backtrack, ellers)')
parser.add_argument('--width', metavar='w', type=int, default=5, help='width of maze')
parser.add_argument('--height', metavar='h', type=int, default=5, help='height of maze')
parser.add_argument('--show_steps', type=bool, default=False, help='show slideshow of steps taken')
parser.add_argument('--output_file', type=str, default="null", help='output file')
args = parser.parse_args()


def display_grid(grid):
    img = util.convert_maze_to_image_array(grid, 5)
    resized = cv2.resize(img, (600,600), interpolation = cv2.INTER_AREA)

    cv2.imshow('Maze', resized)
    cv2.waitKey(0)
 
 
def output_data(maze):
    ext = os.path.splitext(args.output_file)[-1]
    if ext == ".txt":
        util.output_txt_file(args.output_file, maze.grid)
    elif ext == ".png":
        img = util.convert_maze_to_image_array(maze.grid, 5)
        resized = cv2.resize(img, (800, 800), interpolation = cv2.INTER_AREA)
        cv2.imwrite(args.output_file, 255 * resized)
    elif ext == ".mp4":
        video = cv2.VideoWriter(args.output_file, cv2.VideoWriter_fourcc(*'mp4v'), 60, (800,800))
        for i in range(len(maze.step_array)):
            img = util.convert_maze_to_image_array(maze.step_array[i], 5)
            resized = cv2.resize(img, (800, 800), interpolation = cv2.INTER_AREA)
            print("Writing Video Frame " + str(i) + " of " + str(len(maze.step_array)) + "...\r", end="")
            video.write((resized * 255).astype(np.uint8))
        video.release()
    else:
        print("Error: Unsupported Output File Type...")


def main():
    maze = mazes.get_gen(args.generator_type)(args.width, args.height)
    maze.generate()
    
    time_taken = maze.get_stats()
    print("Time Taken: ", time_taken)

    if args.show_steps:
        for m in maze.step_array:
            display_grid(m)
    else:
        display_grid(maze.grid)
    
    if args.output_file != "null":
        output_data(maze)
    
if __name__ == '__main__':
    main()