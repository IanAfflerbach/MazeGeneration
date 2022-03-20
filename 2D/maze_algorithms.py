import numpy as np
import random
import time
import utilities as util
from utilities import DIRECTIONS

class MazeBase:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.grid = img = np.zeros([w, h], dtype=int)
        
        self.step_array = []
        self.read_num = 0
        self.write_num = 0
        self.start_time = 0
        self.end_time = 0
        return
        
    def generate(self):
        self.grid[:,:] = util.get_open_room()
            
    def display_data_grid(self):
        print(self.grid)
        
    def get_stats(self):
        return self.read_num, self.write_num, self.end_time - self.start_time
       
    def _init_edge_tuples(self):
        self.edges = []
        for i in range(0, self.w - 1):
            for j in range(0, self.h):
                self.edges.append(((i, j), (i + 1, j)))
        for i in range(0, self.w):
            for j in range(0, self.h - 1):
                self.edges.append(((i, j), (i, j + 1)))
                
    def _add_edge(self, edge):
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
            
        self.step_array.append(np.copy(self.grid))
        self.write_num += 1
        
    def _get_possible_edges(self, coord):
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

class Kruskals(MazeBase):
    def __init__(self, w, h):
        super().__init__(w, h)
        
    def generate(self):
        self.start_time = time.time()
        self._init_edge_tuples()
        cells = np.arange(self.w * self.h).reshape(self.w, self.h)
        
        random.shuffle(self.edges)
        for edge in self.edges:
            # check if edge already exists
            self.read_num += 1
            if (cells[edge[0]] == cells[edge[1]]):
                continue
                
            # add edge
            self._add_edge(edge)
            
            # reassign cells
            c_one = cells[edge[0]]
            c_two = cells[edge[1]]
            cells[edge[0]] = c_two
            for i in range(0, self.w):
                for j in range(0, self.h):
                    self.read_num += 1
                    if cells[i,j] == c_one:
                        cells[i,j] = c_two
            
            # check if all cells are equal
            check = cells[0,0]
            result = True
            for x in cells.reshape(self.w * self.h):
                self.read_num += 1
                if x != check:
                    result = False
                    break
            if result == True:
                break
        
        self.end_time = time.time()
    
    
class Prims(MazeBase):
    def __init__(self, w, h):
        super().__init__(w, h)
        
    def generate(self):
        self.start_time = time.time()
        start_tuple = (random.randint(0, self.w - 1), random.randint(0, self.h - 1))
        curr_edges = self._get_possible_edges(start_tuple)
        
        while len(curr_edges) != 0:
            self.read_num += 1
            random.shuffle(curr_edges)
            
            # add new edge to grid
            edge = curr_edges.pop()
            self._add_edge(edge)
            
            # define start and end points
            start, dest = edge
            
            # remove edges with same destination
            self.read_num += len(curr_edges)
            curr_edges = [edge for edge in curr_edges if edge[1] != dest]
            
            # get edges to add
            curr_edges += self._get_possible_edges(dest)
        
        self.end_time = time.time()
        
class RecursiveBacktrack(MazeBase):
    def __init__(self, w, h):
        super().__init__(w, h)
        
    def generate(self):
        self.start_time = time.time()
        start_tuple = (random.randint(0, self.w - 1), random.randint(0, self.h - 1))
        self.__carve_path(start_tuple)
        self.end_time = time.time()
        
    def __carve_path(self, coord):
        edges = self._get_possible_edges(coord)
        random.shuffle(edges)
        for edge in edges:
            self.read_num += 1
            if self.grid[edge[1]] != 0:
                continue
            self._add_edge(edge)
            self.__carve_path(edge[1])   

def get_gen(name):
    gen_types = {
        "kruskals": Kruskals,
        "prims": Prims,
        "recursive_backtrack": RecursiveBacktrack
    }
    
    if name not in gen_types:
        print("type not supported")
        quit()
        
    return gen_types[name]