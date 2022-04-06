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
    
def create_viewer_image(grid, cell_size):
    w, h, l = np.shape(grid)
    maze_w = cell_size * w + (w + 1)
    maze_h = cell_size * h + (h + 1)
    
    img_w = maze_w * l + 2 * (l + 1)
    img_h = maze_h + 4
    
    # print(maze_w, maze_h, img_w, img_h)
    
    # init image
    img = np.ones((img_w, img_h, 3))
    
    # set image borders
    img[0,:] = img[:,0] = img[-1,:] = img[:,-1] = [0.5, 0.5, 0.5]
    
    # set maze walls
    for i in range(l):
        row=i*(maze_h+2)
        
        for j in range(w+1):
            sub_row=j*math.floor(maze_h/h)
            img[2+row+sub_row,2:2+(maze_w)] = [0.0, 0.0, 0.0]
        
        for j in range(h+1):
            sub_col=j*math.floor(maze_w/w)
            img[2+row:2+(maze_h)+row,2+sub_col] = [0.0, 0.0, 0.0]
    
    # set maze hallways and portals
    for i in range(l):
        curr_grid = grid[:,:,i]
        hall_size=cell_size-2
        row=2+i*(2+maze_w)
        col=2
        
        for j in range(0, w):
            for k in range(0, h):
                # hallways
                if (curr_grid[j,k] & DIRECTIONS["N"]):
                    sub_row = 2+j*math.floor(maze_h/h)
                    sub_col = (k+1)*math.floor(maze_w/w)
                    img[row+sub_row:row+sub_row+hall_size, col+sub_col] = [1.0, 1.0, 1.0]
                if (curr_grid[j,k] & DIRECTIONS["E"]):
                    sub_row = (j+1)*math.floor(maze_h/h)
                    sub_col = 2+k*math.floor(maze_w/w)
                    img[row+sub_row, col+sub_col:col+sub_col+hall_size] = [1.0, 1.0, 1.0]
                
                # portals
                if (curr_grid[j,k] & DIRECTIONS["F"]):
                    sub_row=1+j*math.floor(maze_h/h)
                    sub_col=1+k*math.floor(maze_w/w)
                    img[row+sub_row,col+sub_col]=[1.0, 0.0, 0.0]
                if (curr_grid[j,k] & DIRECTIONS["B"]):
                    sub_row=-1+(j+1)*math.floor(maze_h/h)
                    sub_col=-1+(k+1)*math.floor(maze_w/w)
                    img[row+sub_row,col+sub_col]=[0.0, 0.0, 1.0]

    return img
    
def create_viewer_image_with_path(grid, path):
    cell_size = 5
    w, h, l = np.shape(grid)
    maze_w = cell_size * w + (w + 1)
    maze_h = cell_size * h + (h + 1)
    img = create_viewer_image(grid, cell_size)
    
    for edge in path:
        p_a, p_b = edge
        
        if p_a[0] > p_b[0] or p_a[1] > p_b[1]:
            tmp = p_a
            p_a = p_b
            p_b = tmp
        
        x_a, y_a, z_a = p_a
        x_b, y_b, z_b = p_b
        
        row_a = 5+x_a*math.floor(maze_h/h)+z_a*(2+maze_h)
        col_a = 5+y_a*math.floor(maze_w/w)
        
        row_b = 5+x_b*math.floor(maze_h/h)+z_b*(2+maze_h)
        col_b = 5+y_b*math.floor(maze_w/w)
        
        if z_a != z_b:
            img[row_a,col_a] = [0.0, 0.0, 1.0]
            img[row_b,col_b] = [0.0, 0.0, 1.0]
        else:        
            img[row_a:row_b+1,col_a:col_b+1] = [0.0, 0.0, 1.0]
        
    return img