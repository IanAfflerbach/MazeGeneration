import math
import numpy as np

DIRECTIONS = {"N": 0x1, "S": 0x2, "E": 0x4, "W": 0x8, "F": 0x10, "B": 0x20 }

def get_open_room():
    val = 0x0;
    for x in DIRECTIONS.values():
        val += x
    return val
    

def convert_maze_to_list_of_lines(maze):
    lines = []
    shape = np.shape(maze)
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                val = maze[i,j,k]
                if (val & DIRECTIONS["E"]):
                    lines.append(((i, j, k), (i+1, j, k)))
                if (val & DIRECTIONS["N"]):
                    lines.append(((i, j, k), (i, j+1, k)))
                if (val & DIRECTIONS["F"]):
                    lines.append(((i, j, k), (i, j, k+1)))

    return lines