import numpy as np
import cv2
import argparse

import solver_algorithms as solvers
import utilities as util

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, help='maze file')
args = parser.parse_args()

def display_grid_and_path(grid, path):
    img = util.convert_maze_and_path_to_image_array(grid, path, 5)
    resized = cv2.resize(img, (600,600), interpolation = cv2.INTER_AREA)

    cv2.imshow('Maze', resized)
    cv2.waitKey(0)

def main():
    grid = util.import_txt_file(args.file)
    solver = solvers.RecursiveDFS(grid)
    solver.solve()
    
    display_grid_and_path(solver.grid, solver.path)

if __name__ == "__main__":
    main()