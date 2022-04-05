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
    
def import_txt_file(filename):
    with open(filename, "rb") as f:
        lines = f.readlines()
        
        w = int(lines[0].decode('utf-8').split(' ')[1])
        h = int(lines[1].decode('utf-8').split(' ')[1])
        l = int(lines[2].decode('utf-8').split(' ')[1])
        t = int(lines[3].decode('utf-8').split(' ')[1])
        
        b_str = b""
        for i in range(5, len(lines)):
            b_str += lines[i]
            
        grid = np.frombuffer(b_str, dtype=int).reshape((w, h, l, t))
    return grid
    
def create_viewer_image(grid):
    cell_size = 5
    w, h, l, t = np.shape(grid)
    maze_w = cell_size * w + (w + 1)
    maze_h = cell_size * h + (h + 1)
    
    img_w = maze_w * l + 2 * (l + 1)
    img_h = maze_h * t + 2 * (t + 1)
    
    # print(maze_w, maze_h, img_w, img_h)
    
    # init image
    img = np.ones((img_w, img_h, 3))
    
    # set image borders
    img[0,:] = img[:,0] = img[-1,:] = img[:,-1] = [0.5, 0.5, 0.5]
    
    # set maze walls
    for i in range(l):
        for j in range(t):
            row=i*(maze_h+2)
            col=j*(maze_w+2)
            
            for k in range(w+1):
                sub_row=k*math.floor(maze_h/h)
                img[2+row+sub_row,2+col:2+col+(maze_w)] = [0.0, 0.0, 0.0]
            
            for k in range(h+1):
                sub_col=k*math.floor(maze_w/w)
                img[2+row:2+(maze_h)+row,2+col+sub_col] = [0.0, 0.0, 0.0]
    
    # set maze hallways and portals
    for i in range(l):
        for j in range(t):
            curr_grid = grid[:,:,i,j]
            hall_size=cell_size-2
            row=2+i*(2+maze_w)
            col=2+j*(2+maze_h)
            
            for k in range(0, w):
                for g in range(0, h):
                    # hallways
                    if (curr_grid[k,g] & DIRECTIONS["N"]):
                        sub_row = 2+k*math.floor(maze_h/h)
                        sub_col = (g+1)*math.floor(maze_w/w)
                        img[row+sub_row:row+sub_row+hall_size, col+sub_col] = [1.0, 1.0, 1.0]
                    if (curr_grid[k,g] & DIRECTIONS["E"]):
                        sub_row = (k+1)*math.floor(maze_h/h)
                        sub_col = 2+g*math.floor(maze_w/w)
                        img[row+sub_row, col+sub_col:col+sub_col+hall_size] = [1.0, 1.0, 1.0]
                    
                    # fb portals
                    if (curr_grid[k,g] & DIRECTIONS["F"]):
                        sub_row=1+k*math.floor(maze_h/h)
                        sub_col=1+g*math.floor(maze_w/w)
                        img[row+sub_row,col+sub_col]=[1.0, 0.0, 0.0]
                    if (curr_grid[k,g] & DIRECTIONS["B"]):
                        sub_row=-1+(k+1)*math.floor(maze_h/h)
                        sub_col=-1+(g+1)*math.floor(maze_w/w)
                        img[row+sub_row,col+sub_col]=[0.0, 0.0, 1.0]
                        
                    # cr portals
                    if (curr_grid[k,g] & DIRECTIONS["C"]):
                        sub_row=-1+(k+1)*math.floor(maze_h/h)
                        sub_col=1+g*math.floor(maze_w/w)
                        img[row+sub_row,col+sub_col]=[0.0, 1.0, 1.0]
                    if (curr_grid[k,g] & DIRECTIONS["R"]):
                        sub_row=1+k*math.floor(maze_h/h)
                        sub_col=-1+(g+1)*math.floor(maze_w/w)
                        img[row+sub_row,col+sub_col]=[0.0, 1.0, 0.0]

    return img