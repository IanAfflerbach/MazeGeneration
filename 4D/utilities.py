import math
import numpy as np

DIRECTIONS = {"N": 0x1, "S": 0x2, "E": 0x4, "W": 0x8, "F": 0x10, "B": 0x20, "C": 0x40, "R": 0x80 }

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
                for t in range(shape[3]):
                    val = maze[i,j,k,t]
                    if (val & DIRECTIONS["E"]):
                        lines.append(((i, j, k, t), (i+1, j, k, t)))
                    if (val & DIRECTIONS["N"]):
                        lines.append(((i, j, k, t), (i, j+1, k, t)))
                    if (val & DIRECTIONS["F"]):
                        lines.append(((i, j, k, t), (i, j, k+1, t)))
                    if (val & DIRECTIONS["C"]):
                        lines.append(((i, j, k, t), (i, j, k, t+1)))

    return lines
    
def output_txt_file(filename, grid):
    with open(filename, "wb") as f:
        w, h, l, t = np.shape(grid)
        f.write(bytes("WIDTH: %i\n" % w, 'utf-8'))
        f.write(bytes("HEIGHT: %i\n" % h, 'utf-8'))
        f.write(bytes("LENGTH: %i\n" % l, 'utf-8'))
        f.write(bytes("TIMEFRAME: %i\n" % t, 'utf-8'))
        f.write(bytes("ENDIAN: BIG\n", 'utf-8'))
        f.write(grid.tobytes());
    return