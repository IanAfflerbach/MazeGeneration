import numpy as np
import utilities as util
import time
from utilities import DIRECTIONS

class SolverBase:
    def __init__(self, grid):
        self.grid = grid
        self.w, self.h, self.l, self.t = np.shape(self.grid)
        self.start_point = (0, 0, 0, 0)
        self.end_point = (self.w - 1, self.h - 1, self.l - 1, self.t - 1)
        self.path = []
        self.path_array = []
        self.read_num = 0
        self.write_num = 0
        self.start_time = 0
        self.end_time = 0
        return
        
    def get_stats(self):
        return self.read_num, self.write_num, self.end_time - self.start_time
        
    def solve(self):
        print("Solving!")
        return


class RecursiveDFS(SolverBase):
    def __init__(self, grid):
        super().__init__(grid)
        
    def solve(self):
        self.start_time = time.time()
        self.visited_points = np.zeros((self.w, self.h, self.l, self.t), dtype=int)        
        result = self.__move(self.start_point)
        self.end_time = time.time()
        
        if result == -1:
            print("ERROR: maze is disconnected")
        
    def __move(self, point):
        x, y, z, t = point
        self.visited_points[x, y, z, t] = 1
        
        if (point == self.end_point):
            return 1
        
        result = -1        
        if result == -1:
            result = self.__check_point((x, y, z, t), (x+1, y, z, t), DIRECTIONS["E"])
        if result == -1:
            result = self.__check_point((x, y, z, t), (x-1, y, z, t), DIRECTIONS["W"])
        if result == -1:
            result = self.__check_point((x, y, z, t), (x, y+1, z, t), DIRECTIONS["N"])
        if result == -1:
            result = self.__check_point((x, y, z, t), (x, y-1, z, t), DIRECTIONS["S"])
        if result == -1:
            result = self.__check_point((x, y, z, t), (x, y, z+1, t), DIRECTIONS["F"])
        if result == -1:
            result = self.__check_point((x, y, z, t), (x, y, z-1, t), DIRECTIONS["B"])
        if result == -1:
            result = self.__check_point((x, y, z, t), (x, y, z, t+1), DIRECTIONS["C"])
        if result == -1:
            result = self.__check_point((x, y, z, t), (x, y, z, t-1), DIRECTIONS["R"])
        
        return result
        
    def __check_point(self, start, dest, direct):
        result = -1
        
        if self.grid[start] & direct != 0x0 and self.visited_points[dest] == 0:
            self.read_num += 1
            self.__add_path(start, dest)
            result = self.__move(dest)
            if result == -1:
                self.__pop_path()
                
        return result
        
    def __add_path(self, start, dest):
        self.write_num += 1
        self.path.append((start, dest))
        self.path_array.append(np.copy(self.path))
        
    def __pop_path(self, ):
        self.write_num += 1
        self.path.pop()
        self.path_array.append(np.copy(self.path))


class BFS(SolverBase):
    def __init__(self, grid):
        super().__init__(grid)
        
    def solve(self):
        self.start_time = time.time()
        self.visited_points = np.zeros((self.w, self.h, self.l, self.t), dtype=int)
        path_queue = [[self.start_point]]
        
        while True:
            curr_path = path_queue.pop(0)
            self.visited_points[curr_path[-1]] = 1
            conn_points = self.__get_connected_points(curr_path[-1])
            
            result = -1
            for p in conn_points:
                new_path = curr_path.copy()
                new_path.append(p)
                path_queue.append(new_path)
                
                if p == self.end_point:
                    self.__create_final_path(new_path)
                    result = 1  
            self.__add_path_queue_to_array(path_queue)
            if result == 1:
                break
            
        self.end_time = time.time()
        return
        
    def __get_connected_points(self, p):
        x, y, z, t = p
        conn_points = []
        self.read_num += 6
        if self.grid[x, y, z, t] & DIRECTIONS["E"] != 0x0 and self.visited_points[x+1, y, z, t] == 0:
            conn_points.append((x+1, y, z, t))
            self.write_num += 1
        if self.grid[x, y, z, t] & DIRECTIONS["W"] != 0x0 and self.visited_points[x-1, y, z, t] == 0:
            conn_points.append((x-1, y, z, t))
            self.write_num += 1
        if self.grid[x, y, z, t] & DIRECTIONS["N"] != 0x0 and self.visited_points[x, y+1, z, t] == 0:
            conn_points.append((x, y+1, z, t))
            self.write_num += 1
        if self.grid[x, y, z, t] & DIRECTIONS["S"] != 0x0 and self.visited_points[x, y-1, z, t] == 0:
            conn_points.append((x, y-1, z, t))
            self.write_num += 1   
        if self.grid[x, y, z, t] & DIRECTIONS["F"] != 0x0 and self.visited_points[x, y, z+1, t] == 0:
            conn_points.append((x, y, z+1, t))
            self.write_num += 1 
        if self.grid[x, y, z, t] & DIRECTIONS["B"] != 0x0 and self.visited_points[x, y, z-1, t] == 0:
            conn_points.append((x, y, z-1, t))
            self.write_num += 1   
        if self.grid[x, y, z, t] & DIRECTIONS["C"] != 0x0 and self.visited_points[x, y, z, t+1] == 0:
            conn_points.append((x, y, z, t+1))
            self.write_num += 1       
        if self.grid[x, y, z, t] & DIRECTIONS["R"] != 0x0 and self.visited_points[x, y, z, t-1] == 0:
            conn_points.append((x, y, z, t-1))
            self.write_num += 1              
        
        return conn_points
        
    def __create_final_path(self, path):
        for i in range(1, len(path)):
            self.path.append((path[i-1], path[i]))
            
    def __add_path_queue_to_array(self, queue):
        total_paths = []
        for p in queue:
            for i in range(1, len(p)):
                total_paths.append((p[i-1], p[i]))
                
        self.path_array.append(total_paths)
        return


def get_solv(name):
    solv_types = {
        "recursive_dfs": RecursiveDFS,
        "bfs": BFS
    }
    
    if name not in solv_types:
        print("type not supported")
        quit()
        
    return solv_types[name]