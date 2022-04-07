import math
import numpy as np

DIRECTIONS = {"N": 0x1, "S": 0x2, "E": 0x4, "W": 0x8 }

def get_open_room():
    val = 0x0;
    for x in DIRECTIONS.values():
        val += x
    return val
    
def convert_maze_to_image_array(m, cell_size):
    w, h = np.shape(m)
    img_w = cell_size * w + w + 1
    img_h = cell_size * h + h + 1
    img = np.ones((img_w, img_h, 3))
    
    # Set Walls
    for i in range(0, w + 1):
        img[i * (cell_size + 1),:] = [0.0, 0.0, 0.0]
    for i in range(0, h + 1):
        img[:,i * (cell_size + 1)] = [0.0, 0.0, 0.0]
        
    # Set "Hallways"
    hall_size = 5
    for i in range(0, w):
        for j in range(0, h):
            if (m[i,j] & DIRECTIONS["S"]):
                row = i * (cell_size + 1) + cell_size + 1
                col = j * (cell_size + 1) + math.ceil(cell_size / 2)
                img[row, col - math.floor(hall_size / 2):col + math.ceil(hall_size / 2)] = [1.0, 1.0, 1.0]
            if (m[i,j] & DIRECTIONS["E"]):
                row = i * (cell_size + 1) + math.ceil(cell_size / 2)
                col = j * (cell_size + 1) + cell_size + 1
                img[row - math.floor(hall_size / 2):row + math.ceil(hall_size / 2), col] = [1.0, 1.0, 1.0]
    
    return img
    
def convert_maze_and_path_to_image_array(m, p, cell_size):
    img = convert_maze_to_image_array(m, cell_size)
    
    for edge in p:
        p_a, p_b = edge
        
        if p_a[0] > p_b[0] or p_a[1] > p_b[1]:
            tmp = p_a
            p_a = p_b
            p_b = tmp
        
        row_a, col_a = p_a
        row_a = math.ceil(cell_size / 2) + row_a * (cell_size + 1)
        col_a = math.ceil(cell_size / 2) + col_a * (cell_size + 1)
        
        row_b, col_b = p_b
        row_b = math.ceil(cell_size / 2) + row_b * (cell_size + 1)
        col_b = math.ceil(cell_size / 2) + col_b * (cell_size + 1)
        
        img[row_a:row_b + 1, col_a:col_b + 1] = [0.0, 0.0, 1.0]
    return img;
    
def convert_maze_and_xgrid_to_image_array(m, x, cell_size):
    img = convert_maze_to_image_array(m, cell_size)
    cross = [[[0.0, 0.0, 0.0] if i == j or i+j == cell_size-1 else [1.0, 1.0, 1.0] for i in range(cell_size)] for j in range(cell_size)]
    
    w, h = np.shape(x)
    for i in range(w):
        for j in range(h):
            if x[i, j] == 0:
                continue
            row = 1+i*(cell_size+1)
            col = 1+j*(cell_size+1)
            img[row:row+cell_size,col:col+cell_size] = np.copy(cross)
    
    return img
    
def output_txt_file(filename, grid):
    with open(filename, "wb") as f:
        w, h = np.shape(grid)
        f.write(bytes("WIDTH: %i\n" % w, 'utf-8'));
        f.write(bytes("HEIGHT: %i\n" % h, 'utf-8'));
        f.write(bytes("ENDIAN: BIG\n", 'utf-8'));
        f.write(grid.tobytes());
    return
    
def import_txt_file(filename):
    with open(filename, "rb") as f:
        lines = f.readlines()
        
        w = int(lines[0].decode('utf-8').split(' ')[1])
        h = int(lines[1].decode('utf-8').split(' ')[1])
        
        b_str = b""
        for i in range(3, len(lines)):
            b_str += lines[i]
            
        grid = np.frombuffer(b_str, dtype=int).reshape((w, h))
    return grid