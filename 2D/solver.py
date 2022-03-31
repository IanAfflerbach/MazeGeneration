import numpy as np
import cv2
import argparse

import solver_algorithms as solvers
import utilities as util

parser = argparse.ArgumentParser()
parser.add_argument('solver', type=str, help='maze solver')
parser.add_argument('file', type=str, help='maze file')
parser.add_argument('--show_steps', type=bool, default=False, help='show slideshow of steps taken')
args = parser.parse_args()

def display_grid_and_path(grid, path):
    img = util.convert_maze_and_path_to_image_array(grid, path, 5)
    resized = cv2.resize(img, (600,600), interpolation = cv2.INTER_AREA)

    cv2.imshow('Maze', resized)
    cv2.waitKey(0)

def main():
    grid = util.import_txt_file(args.file)
    solver = solvers.get_solv(args.solver)(grid)
    solver.solve()
    
    if args.show_steps:
        for p in solver.path_array:
            display_grid_and_path(solver.grid, p)
    else:
        display_grid_and_path(solver.grid, solver.path)
    
    read, write, time_taken = solver.get_stats()
    print("Read Instruction: ", read)
    print("Write Instructions: ", write)
    print("Time Taken: ", time_taken)

if __name__ == "__main__":
    main()