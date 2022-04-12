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
        self.step_array.append(np.copy(self.grid))
        self.start_time = 0
        self.end_time = 0
        return
        
    def generate(self):
        self.grid[:,:] = util.get_open_room()
            
    def display_data_grid(self):
        print(self.grid)
        
    def get_stats(self):
        return self.end_time - self.start_time
       
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
        
        self.end_time = time.time()
    
    
class Prims(MazeBase):
    def __init__(self, w, h):
        super().__init__(w, h)
        
    def generate(self):
        self.start_time = time.time()
        start_tuple = (random.randint(0, self.w - 1), random.randint(0, self.h - 1))
        curr_edges = self._get_possible_edges(start_tuple)
        
        while len(curr_edges) != 0:
            random.shuffle(curr_edges)
            
            # add new edge to grid
            edge = curr_edges.pop()
            self._add_edge(edge)
            
            # define start and end points
            start, dest = edge
            
            # remove edges with same destination
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
            if self.grid[edge[1]] != 0:
                continue
            self._add_edge(edge)
            self.__carve_path(edge[1])   
            
         
class HuntKill(MazeBase):
    def __init__(self, w, h):
        super().__init__(w, h)
        
    def generate(self):
        self.start_time = time.time()
        x, y = random.randint(0, self.w-1), random.randint(0, self.h-1)
        while (x, y) != (-1, -1):
            self.__walk((x, y))
            x, y = self.__hunt()
        self.end_time = time.time()
    
    def __walk(self, coord):
        edges = self._get_possible_edges(coord)
        if len(edges) == 0:
            return
        random.shuffle(edges)
        self._add_edge(edges[0])
        self.__walk(edges[0][1]) 
        
    def __hunt(self):
        for i in range(self.w):
            for j in range(self.h):
                if self.grid[i, j] != 0x0:
                    continue
                if (i != 0) and self.grid[i-1,j] != 0x0:
                    self._add_edge(((i,j),(i-1,j)))
                    return (i,j)
                if (j != 0) and self.grid[i,j-1] != 0x0:
                    self._add_edge(((i,j),(i,j-1)))
                    return (i,j)
                if (i != self.w - 1) and self.grid[i+1,j] != 0x0:
                    self._add_edge(((i,j),(i+1,j)))
                    return (i,j)
                if (j != self.h - 1) and self.grid[i,j+1] != 0x0:
                    self._add_edge(((i,j),(i,j+1)))
                    return (i,j)
              
        return (-1, -1)


class Ellers(MazeBase):
    def __init__(self, w, h):
        super().__init__(w, h)
        
    def generate(self):
        self.start_time = time.time()
        
        # init first row
        row_sets = list(range(self.w))
        next_set_num = self.w
        
        for i in range(1, self.w):
            # merge row and drip next row
            row_sets = self.__random_cell_merge(row_sets, i-1)
            next_sets = self.__random_drip(row_sets, i-1)
            for j in range(self.w):
                if next_sets[j] == -1:
                    next_sets[j] = next_set_num
                    next_set_num += 1
            row_sets = next_sets
            
        self.__final_row_merge(row_sets)
        self.end_time = time.time()
        
    def __random_cell_merge(self, row, ind):
        for i in range(1, len(row)):
            if row[i] != row[i-1] and random.randint(0,1) == 1:
                new, old = min(row[i], row[i-1]), max(row[i], row[i-1])
                row[i] = row[i-1] = new
                row = [new if x == old else x for x in row]
                self._add_edge(((i-1, ind), (i, ind)))
        return row
        
    def __final_row_merge(self, row):
        for i in range(1, len(row)):
            if row[i] != row[i-1]:
                new, old = min(row[i], row[i-1]), max(row[i], row[i-1])
                row[i] = row[i-1] = new
                row = [new if x == old else x for x in row]
                self._add_edge(((i-1, self.h-1), (i, self.h-1)))
        
    def __random_drip(self, row, ind):
        next_row = [-1 for i in range(len(row))]
        
        for x in np.unique(np.array(row)):
            indices = [j for j in range(len(row)) if row[j] == x]
            num_drip = random.randint(1, len(indices))
            
            random.shuffle(indices)
            for j in range(num_drip):
                next_row[indices[j]] = x
                self._add_edge(((indices[j], ind), (indices[j], ind + 1)))
                
        return next_row
    

def get_gen(name):
    gen_types = {
        "kruskals": Kruskals,
        "prims": Prims,
        "recursive_backtrack": RecursiveBacktrack,
        "hunt_and_kill": HuntKill,
        "ellers": Ellers
    }
    
    if name not in gen_types:
        print("type not supported")
        quit()
        
    return gen_types[name]