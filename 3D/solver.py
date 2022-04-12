import numpy as np
import cv2
import argparse
import os

import solver_algorithms as solvers
import utilities as util

parser = argparse.ArgumentParser()
parser.add_argument('solver', type=str, help='maze solver')
parser.add_argument('file', type=str, help='maze file')
parser.add_argument('--show_steps', type=bool, default=False, help='show slideshow of steps taken')
parser.add_argument('--output_file', type=str, default="null", help='output file')
args = parser.parse_args()

def display_grid_and_path(grid, path):
    img = util.create_viewer_image_with_path(grid, path)
    resized = cv2.resize(img, (200,600), interpolation = cv2.INTER_AREA)

    cv2.imshow('Maze', resized)
    cv2.waitKey(0)
    

def output_data(maze):
    ext = os.path.splitext(args.output_file)[-1]
    if ext == ".png":
        img = util.create_viewer_image_with_path(maze.grid, maze.path)
        resized = cv2.resize(img, (200, 600), interpolation = cv2.INTER_AREA)
        cv2.imwrite(args.output_file, 255 * resized)
    elif ext == ".mp4":
        video = cv2.VideoWriter(args.output_file, cv2.VideoWriter_fourcc(*'mp4v'), 25, (200,600))
        for i in range(len(maze.path_array)):
            img = util.create_viewer_image_with_path(maze.grid, maze.path_array[i])
            resized = cv2.resize(img, (200, 600), interpolation = cv2.INTER_AREA)
            print("Writing Video Frame " + str(i) + " of " + str(len(maze.path_array)) + "...\r", end="")
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
    
    if args.show_steps:
        for p in solver.path_array:
            display_grid_and_path(solver.grid, p)
    else:
        display_grid_and_path(solver.grid, solver.path)
    
    if args.output_file != "null":
        output_data(solver)

if __name__ == "__main__":
    main()