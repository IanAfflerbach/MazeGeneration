import numpy as np
import cv2
import os
import argparse

import solver_algorithms as solvers
import utilities as util

parser = argparse.ArgumentParser()
parser.add_argument('solver', type=str, help='maze solver')
parser.add_argument('file', type=str, help='maze file')
parser.add_argument('--output_file', type=str, default="null", help='output file')
parser.add_argument('--show_steps', type=bool, default=False, help='show slideshow of steps taken')
args = parser.parse_args()

def display_grid_and_path(grid, path):
    img = util.convert_maze_and_path_to_image_array(grid, path, 5)
    resized = cv2.resize(img, (600,600), interpolation = cv2.INTER_AREA)

    cv2.imshow('Maze', resized)
    cv2.waitKey(0)


def display_grid_and_xs(grid, x_grid):
    img = util.convert_maze_and_xgrid_to_image_array(grid, x_grid, 5)
    resized = cv2.resize(img, (600,600), interpolation = cv2.INTER_AREA)

    cv2.imshow('Maze', resized)
    cv2.waitKey(0)
    return
    
    
def output_data(solver):
    ext = os.path.splitext(args.output_file)[-1]
    if ext == ".png":
        img = util.convert_maze_and_path_to_image_array(solver.grid, solver.path, 5)
        resized = cv2.resize(img, (800, 800), interpolation = cv2.INTER_AREA)
        cv2.imwrite(args.output_file, 255 * resized)
    elif ext == ".mp4" and solver.path_search_flag:
        video = cv2.VideoWriter(args.output_file, cv2.VideoWriter_fourcc(*'mp4v'), 60, (800,800))
        for i in range(len(solver.path_array)):
            img = util.convert_maze_and_path_to_image_array(solver.grid, solver.path_array[i], 5)
            resized = cv2.resize(img, (800, 800), interpolation = cv2.INTER_AREA)
            print("Writing Video Frame " + str(i) + " of " + str(len(solver.path_array)) + "...\r", end="")
            video.write((resized * 255).astype(np.uint8))
        video.release()
    elif ext == ".mp4" and not solver.path_search_flag:
        video = cv2.VideoWriter(args.output_file, cv2.VideoWriter_fourcc(*'mp4v'), 60, (800,800))
        for i in range(len(solver.x_grid_array)):
            img = util.convert_maze_and_xgrid_to_image_array(solver.grid, solver.x_grid_array[i], 5)
            resized = cv2.resize(img, (800, 800), interpolation = cv2.INTER_AREA)
            print("Writing Video Frame " + str(i) + " of " + str(len(solver.x_grid_array)) + "...\r", end="")
            video.write((resized * 255).astype(np.uint8))
        video.release()
    else:
        print("Error: Unsupported Output File Type...")
    

def main():
    grid = util.import_txt_file(args.file)
    solver = solvers.get_solv(args.solver)(grid)
    solver.solve()
    
    time_taken = solver.get_stats()
    print("Time Taken: ", time_taken)
    
    if args.show_steps and solver.path_search_flag:
        for p in solver.path_array:
            display_grid_and_path(solver.grid, p)
    elif args.show_steps:
        for x in solver.x_grid_array:
            display_grid_and_xs(solver.grid, x)
    else:
        display_grid_and_path(solver.grid, solver.path)
        
    if args.output_file != "null":
        output_data(solver)

if __name__ == "__main__":
    main()