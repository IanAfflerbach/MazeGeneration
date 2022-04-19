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
parser.add_argument('--show_steps', type=bool, default=False, help='show slideshow of steps taken')
parser.add_argument('--output_file', type=str, default="null", help='output file')
args = parser.parse_args()


def display_grid(maze):
    img = util.create_viewer_image(maze, 5)
    resized = cv2.resize(img, (150,600), interpolation = cv2.INTER_AREA)

    cv2.imshow('Maze', resized)
    cv2.waitKey(0)


def display_3D_grid(maze):
    lines = util.convert_maze_to_list_of_lines(maze)
    shape = np.shape(maze)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for i in range(len(lines)):
        ax.plot([lines[i][0][0], lines[i][1][0]], [lines[i][0][1], lines[i][1][1]], [lines[i][0][2], lines[i][1][2]])
    
    ax.set_xlim(0, shape[0] - 1)
    ax.set_ylim(0, shape[1] - 1)
    ax.set_zlim(0, shape[2] - 1)
    plt.show()


def output_data(maze):
    ext = os.path.splitext(args.output_file)[-1]
    if ext == ".txt":
        util.output_txt_file(args.output_file, maze.grid)
    elif ext == ".png":
        img = util.create_viewer_image(maze.grid, 5)
        resized = cv2.resize(img, (200, 600), interpolation = cv2.INTER_AREA)
        cv2.imwrite(args.output_file, 255 * resized)
    elif ext == ".mp4":
        video = cv2.VideoWriter(args.output_file, cv2.VideoWriter_fourcc(*'mp4v'), 25, (200,600))
        for i in range(len(maze.step_array)):
            img = util.create_viewer_image(maze.step_array[i], 5)
            resized = cv2.resize(img, (200, 600), interpolation = cv2.INTER_AREA)
            print("Writing Video Frame " + str(i) + " of " + str(len(maze.step_array)) + "...\r", end="")
            video.write((resized * 255).astype(np.uint8))
        video.release()
    else:
        print("Error: Unsupported Output File Type...")


def main():   
    maze = mazes.get_gen(args.generator_type)(args.width, args.height, args.length)
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