import numpy as np
import argparse
import os
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

'''
def display_grid(maze):
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
'''

def output_data(filename, grid):
    ext = os.path.splitext(filename)[-1]
    if ext == ".txt":
        util.output_txt_file(filename, grid)
    else:
        print("Error: Unsupported Output File Type...")
        

def main():   
    maze = mazes.get_gen(args.generator_type)(args.width, args.height, args.length, args.time)
    maze.generate()

    '''
    if args.show_steps:
        for m in maze.step_array:
            display_grid(m)
    else:
        display_grid(maze.grid)
    '''
        
    read, write, time_taken = maze.get_stats()
    print("Read Instruction: ", read)
    print("Write Instructions: ", write)
    print("Time Taken: ", time_taken)
    
    if args.output_file != "null":
        output_data(args.output_file, maze.grid)


if __name__ == '__main__':
    main()