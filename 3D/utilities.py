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
    
def output_txt_file(filename, grid):
    with open(filename, "wb") as f:
        w, h, l = np.shape(grid)
        f.write(bytes("WIDTH: %i\n" % w, 'utf-8'));
        f.write(bytes("HEIGHT: %i\n" % h, 'utf-8'));
        f.write(bytes("LENGTH: %i\n" % l, 'utf-8'))
        f.write(bytes("ENDIAN: BIG\n", 'utf-8'));
        f.write(grid.tobytes());
    return
    
def import_txt_file(filename):
    with open(filename, "rb") as f:
        lines = f.readlines()
        
        w = int(lines[0].decode('utf-8').split(' ')[1])
        h = int(lines[1].decode('utf-8').split(' ')[1])
        l = int(lines[2].decode('utf-8').split(' ')[1])
        
        b_str = b""
        for i in range(4, len(lines)):
            b_str += lines[i]
            
        grid = np.frombuffer(b_str, dtype=int).reshape((w, h, l))
    return grid