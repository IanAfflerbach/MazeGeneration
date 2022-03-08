import numpy as np
import random
import utilities as util
from utilities import DIRECTIONS

class MazeBase:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.grid = img = np.zeros([w, h], dtype=int)
        return
        
    def generate(self):
        self.grid[:,:] = util.get_directionless_room()
       
    def init_edge_tuples(self):
        self.edges = []
        for i in range(0, self.w - 1):
            for j in range(0, self.h):
                self.edges.append(((i, j), (i + 1, j)))
        for i in range(0, self.w):
            for j in range(0, self.h - 1):
                self.edges.append(((i, j), (i, j + 1)))
                
    def add_edge(self, edge):
        l, g = edge
        if l[0] == g[0]:
            if l[1] > g[1]:
                g, l = edge
            row = l[0]
            assert (self.grid[row,l[1]] & DIRECTIONS["E"]) == 0x0, "edge {} already exists".format(edge)            
            
            self.grid[row,l[1]] ^= DIRECTIONS["E"]
            self.grid[row,g[1]] ^= DIRECTIONS["W"]
        elif l[1] == g[1]:
            if l[0] > g[0]:
                g, l = edge
            col = l[1]
            assert (self.grid[l[0],col] & DIRECTIONS["S"]) == 0x0, "edge {} already exists".format(edge)  
            
            self.grid[l[0],col] ^= DIRECTIONS["S"]
            self.grid[g[0],col] ^= DIRECTIONS["N"]
        
    def get_possible_edges(self, coord):
        x, y = coord
        edges = []
        
        if x != 0 and self.grid[x-1, y] == 0:
            edges.append(((x, y), (x-1, y)))
        if x != self.w - 1 and self.grid[x+1, y] == 0:
            edges.append(((x, y), (x+1, y)))
        if y != 0 and self.grid[x, y-1] == 0:
            edges.append(((x, y), (x, y-1)))
        if y != self.h - 1 and self.grid[x, y+1] == 0:
            edges.append(((x, y), (x, y+1)))
    
        return edges
    
    def display_data_grid(self):
        print(self.grid)

class KruskalsMaze(MazeBase):
    def __init__(self, w, h):
        super().__init__(w, h)
        
    def generate(self, output_steps_flag):
        self.init_edge_tuples()
        cells = np.arange(self.w * self.h).reshape(self.w, self.h)
        step_array = []
        
        random.shuffle(self.edges)
        for edge in self.edges:
            # check if edge already exists
            if (cells[edge[0]] == cells[edge[1]]):
                continue
                
            # add edge
            self.add_edge(edge)
            if output_steps_flag != None:
                step_array.append(np.copy(self.grid))
            
            # reassign cells
            c_one = cells[edge[0]]
            c_two = cells[edge[1]]
            cells[edge[0]] = c_two
            for i in range(0, self.w):
                for j in range(0, self.h):
                    if cells[i,j] == c_one:
                        cells[i,j] = c_two
            
            # check if all cells are equal
            check = cells[0,0]
            result = True
            for x in cells.reshape(self.w * self.h):
                if x != check:
                    result = False
                    break
            if result == True:
                break
        
        if output_steps_flag:
            return step_array
    
    
class PrimsMaze(MazeBase):
    def __init__(self, w, h):
        super().__init__(w, h)
        
    def generate(self, output_steps_flag):
        step_array = []
        
        start_tuple = (random.randint(0, self.w - 1), random.randint(0, self.h - 1))
        curr_edges = self.get_possible_edges(start_tuple)
        
        while len(curr_edges) != 0:
            random.shuffle(curr_edges)
            
            # add new edge to grid
            edge = curr_edges.pop()
            self.add_edge(edge)
            step_array.append(np.copy(self.grid))
            
            # define start and end points
            start, dest = edge
            
            # remove edges with same destination
            curr_edges = [edge for edge in curr_edges if edge[1] != dest]
            
            # get edges to add
            curr_edges += self.get_possible_edges(dest)
        
        if output_steps_flag:
            return step_array
        
class RecursiveBacktrackMaze(MazeBase):
    def __init__(self, w, h):
        super().__init__(w, h)
        
    def generate(self, output_steps_flag):
        setup_array = []
        start_tuple = (random.randint(0, self.w - 1), random.randint(0, self.h - 1))
        self.carve_path(start_tuple)
        
    def carve_path(self, coord):
        edges = self.get_possible_edges(coord)
        random.shuffle(edges)
        for edge in edges:
            if self.grid[edge[1]] != 0:
                continue
            self.add_edge(edge)
            self.carve_path(edge[1])   
        
    