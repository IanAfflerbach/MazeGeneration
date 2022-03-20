import math
import numpy as np

DIRECTIONS = {"N": 0x1, "S": 0x2, "E": 0x4, "W": 0x8 }

def get_open_room():
    val = 0x0;
    for x in DIRECTIONS.values():
        val += x
    return val
    
def convert_maze_to_image_array(m):
    cell_size = 5
    w, h = np.shape(m)
    img_w = cell_size * w + w + 1
    img_h = cell_size * h + h + 1
    img = np.ones((img_w, img_h))
    
    # Set Walls
    for i in range(0, w + 1):
        img[i * (cell_size + 1),:] = 0.0
    for i in range(0, h + 1):
        img[:,i * (cell_size + 1)] = 0.0
        
    # Set "Hallways"
    hall_size = 5
    for i in range(0, w):
        for j in range(0, h):
            if (m[i,j] & DIRECTIONS["S"]):
                row = i * (cell_size + 1) + cell_size + 1
                col = j * (cell_size + 1) + math.ceil(cell_size / 2)
                img[row, col - math.floor(hall_size / 2):col + math.ceil(hall_size / 2)] = 1.0
            if (m[i,j] & DIRECTIONS["E"]):
                row = i * (cell_size + 1) + math.ceil(cell_size / 2)
                col = j * (cell_size + 1) + cell_size + 1
                img[row - math.floor(hall_size / 2):row + math.ceil(hall_size / 2), col] = 1.0
    
    return img