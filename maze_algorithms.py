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
        if edge[0][0] == edge[1][0]:
            row = edge[0][0]
            self.grid[row,edge[0][1]] ^= DIRECTIONS["E"]
            self.grid[row,edge[1][1]] ^= DIRECTIONS["W"]
        elif edge[0][1] == edge[1][1]:
            col = edge[0][1]
            self.grid[edge[0][0],col] ^= DIRECTIONS["S"]
            self.grid[edge[1][0],col] ^= DIRECTIONS["N"]
        
    def display_data_grid(self):
        print(self.grid)

class KruskalsMaze(MazeBase):
    def __init__(self, w, h):
        super().__init__(w, h)
        
    def generate(self, output_steps):
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
            if output_steps != None:
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
        
        if output_steps:
            return step_array
    