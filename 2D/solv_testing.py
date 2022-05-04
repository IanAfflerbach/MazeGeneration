import argparse
import numpy as np
import os

import maze_algorithms as mazes
import solver_algorithms as solvers
import utilities as util

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('generator_type', type=str, help='what type of generator')
parser.add_argument('solver_type', type=str, help='what type of solver')
parser.add_argument('--size', metavar='w', type=int, default=5, help='square size of maze')
parser.add_argument('--num_trials', type=int, default=5, help='number of trials to run')
args = parser.parse_args()

def main():
    # total_time taken for all trials
    total_time = 0.0
    
    # run argument number of trials
    for i in range(args.num_trials):
        print("Performing Trial ", i, "...\r", end="")
        
        # generate maze
        maze = mazes.get_gen(args.generator_type)(args.size, args.size)
        maze.generate()
        
        # solve maze
        solver = solvers.get_solv(args.solver_type)(maze.grid)
        solver.solve()
        
        # record and update time taken 
        time_taken = solver.get_stats()
        total_time += time_taken
    
    # output average time
    print("Average time per Trial: ", total_time / args.num_trials)
    
if __name__ == "__main__":
    main()