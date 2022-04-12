import numpy as np
import random
import time
import utilities as util
from utilities import DIRECTIONS

class MazeBase:
    def __init__(self, w, h, l, t):
        self.w = w
        self.h = h
        self.l = l
        self.t = t
        self.grid = img = np.zeros([w, h, l, t], dtype=int)
        
        self.step_array = []
        self.start_time = 0
        self.end_time = 0
        return
        
    def generate(self):
        self.grid[:,:,:,:] = util.get_open_room()
        
    def get_stats(self):
        return self.end_time - self.start_time


    def _init_edge_tuples(self):
        self.edges = []
        for i in range(0, self.w-1):
            for j in range(0, self.h):
                for k in range(0, self.l):
                    for t in range(0, self.t):
                        self.edges.append(((i,j,k,t), (i+1,j,k,t)))
        for i in range(0, self.w):
            for j in range(0, self.h-1):
                for k in range(0, self.l):
                    for t in range(0, self.t):
                        self.edges.append(((i,j,k,t), (i,j+1,k,t)))
        for i in range(0, self.w):
            for j in range(0, self.h):
                for k in range(0, self.l-1):
                    for t in range(0, self.t):
                        self.edges.append(((i,j,k,t), (i,j,k+1,t)))
        for i in range(0, self.w):
            for j in range(0, self.h):
                for k in range(0, self.l):
                    for t in range(0, self.t-1):
                        self.edges.append(((i,j,k,t), (i,j,k,t+1)))

       
    def _add_edge(self, edge):
        l, g = edge
        if l[0] == g[0] and l[1] == g[1] and l[3] == g[3]:
            if l[2] > g[2]:
                g, l = edge
            x = l[0]
            y = l[1]
            t = l[3]
            assert (self.grid[x,y,l[2],t] & DIRECTIONS["F"]) == 0x0, "edge {} already exists".format(edge)            
            
            self.grid[x,y,l[2],t] ^= DIRECTIONS["F"]
            self.grid[x,y,g[2],t] ^= DIRECTIONS["B"]
        elif l[1] == g[1] and l[2] == g[2] and l[3] == g[3]:
            if l[0] > g[0]:
                g, l = edge
            y = l[1]
            z = l[2]
            t = l[3]
            assert (self.grid[l[0],y,z,t] & DIRECTIONS["E"]) == 0x0, "edge {} already exists".format(edge)  
            
            self.grid[l[0],y,z,t] ^= DIRECTIONS["E"]
            self.grid[g[0],y,z,t] ^= DIRECTIONS["W"]
        elif l[2] == g[2] and l[0] == g[0] and l[3] == g[3]:
            if l[1] > g[1]:
                g, l = edge
            x = l[0]
            z = l[2]
            t = l[3]
            assert (self.grid[x,l[1],z,t] & DIRECTIONS["N"]) == 0x0, "edge {} already exists".format(edge)  
            
            self.grid[x,l[1],z,t] ^= DIRECTIONS["N"]
            self.grid[x,g[1],z,t] ^= DIRECTIONS["S"]
        elif l[2] == g[2] and l[0] == g[0] and l[1] == g[1]:
            if l[3] > g[3]:
                g, l = edge
            x = l[0]
            y = l[1]
            z = l[2]
            assert (self.grid[x,y,z,l[3]] & DIRECTIONS["C"]) == 0x0, "edge {} already exists".format(edge)  
            
            self.grid[x,y,z,l[3]] ^= DIRECTIONS["C"]
            self.grid[x,y,z,g[3]] ^= DIRECTIONS["R"]
            
        self.step_array.append(np.copy(self.grid))
    
    def _get_possible_edges(self, coord):
        x, y, z, t = coord
        edges = []
        
        if x != 0 and self.grid[x-1,y,z,t] == 0:
            edges.append(((x, y, z, t), (x-1, y, z, t)))
        if x != self.w - 1 and self.grid[x+1,y,z,t] == 0:
            edges.append(((x, y, z, t), (x+1, y, z, t)))
        
        if y != 0 and self.grid[x,y-1,z,t] == 0:
            edges.append(((x, y, z, t), (x, y-1, z, t)))
        if y != self.h - 1 and self.grid[x,y+1,z, t] == 0:
            edges.append(((x, y, z, t), (x, y+1, z, t)))
            
        if z != 0 and self.grid[x,y,z-1,t] == 0:
            edges.append(((x, y, z, t), (x, y, z-1, t)))
        if z != self.l - 1 and self.grid[x,y,z+1,t] == 0:
            edges.append(((x, y, z, t), (x, y, z+1, t)))
            
        if t != 0 and self.grid[x,y,z,t-1] == 0:
            edges.append(((x, y, z, t), (x, y, z, t-1)))
        if t != self.t - 1 and self.grid[x,y,z,t+1] == 0:
            edges.append(((x, y, z, t), (x, y, z, t+1)))
    
        return edges


class Kruskals(MazeBase):
    def __init__(self, w, h, l, t):
        super().__init__(w, h, l, t)
        
    def generate(self):
        self.start_time = time.time()
        self._init_edge_tuples()
        cells = np.arange(self.w * self.h * self.l * self.t).reshape(self.w, self.h, self.l, self.t)
        
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
                    for k in range(0, self.l):
                        for g in range(self.t):
                            if cells[i,j,k,g] == c_one:
                                cells[i,j,k,g] = c_two
            
            # check if all cells are equal
            check = cells[0,0,0,0]
            result = True
            for x in cells.reshape(self.w * self.h * self.l * self.t):
                if x != check:
                    result = False
                    break
            if result == True:
                break
        
        self.end_time = time.time()


class Prims(MazeBase):
    def __init__(self, w, h, l, t):
        super().__init__(w, h, l, t)
        
    def generate(self):
        self.start_time = time.time()
        start_tuple = (random.randint(0,self.w-1), random.randint(0,self.h-1), random.randint(0,self.l-1), random.randint(0,self.t-1))
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
    def __init__(self, w, h, l, t):
        super().__init__(w, h, l, t)
        
    def generate(self):
        self.start_time = time.time()
        start_tuple = (random.randint(0,self.w-1), random.randint(0,self.h-1), random.randint(0,self.l-1), random.randint(0,self.t-1))
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