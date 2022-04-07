import numpy as np
import utilities as util
import time
from utilities import DIRECTIONS

class SolverBase:
    def __init__(self, grid):
        self.grid = grid
        self.w, self.h = np.shape(self.grid)
        self.start_point = (0, 0)
        self.end_point = (self.w - 1, self.h - 1)
        self.path = []
        self.path_array = []
        self.path_search_flag = True
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
        self.visited_points = np.zeros((self.w, self.h), dtype=int)        
        result = self.__move(self.start_point)
        self.end_time = time.time()
        
        if result == -1:
            print("ERROR: maze is disconnected")
        
    def __move(self, point):
        x, y = point
        self.visited_points[x, y] = 1
        
        if (point == self.end_point):
            return 1
        
        result = -1
        if result == -1:
            result = self.__check_point((x, y), (x+1, y), DIRECTIONS["S"])
        if result == -1:
            result = self.__check_point((x, y), (x-1, y), DIRECTIONS["N"])
        if result == -1:
            result = self.__check_point((x, y), (x, y+1), DIRECTIONS["E"])
        if result == -1:
            result = self.__check_point((x, y), (x, y-1), DIRECTIONS["W"])
        
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
        self.visited_points = np.zeros((self.w, self.h), dtype=int)
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
        x, y = p
        conn_points = []
        self.read_num += 4
        if self.grid[x, y] & DIRECTIONS["S"] != 0x0 and self.visited_points[x+1, y] == 0:
            conn_points.append((x+1, y))
            self.write_num += 1
        if self.grid[x, y] & DIRECTIONS["N"] != 0x0 and self.visited_points[x-1, y] == 0:
            conn_points.append((x-1, y))
            self.write_num += 1
        if self.grid[x, y] & DIRECTIONS["E"] != 0x0 and self.visited_points[x, y+1] == 0:
            conn_points.append((x, y+1))
            self.write_num += 1
        if self.grid[x, y] & DIRECTIONS["W"] != 0x0 and self.visited_points[x, y-1] == 0:
            conn_points.append((x, y-1))
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


class DeadEndFilling(SolverBase):
    def __init__(self, grid):
        super().__init__(grid)
        self.tmp_grid = np.copy(self.grid)
        self.x_grid = np.zeros(np.shape(self.grid))
        self.x_grid_array = []
        self.path_search_flag = False
        
    def solve(self):
        self.start_time = time.time()
        while True:
            dead_ends = self.__get_deadends()
            if len(dead_ends) == 0:
                break
            self.__x_out_points(dead_ends)
            
        self.__get_path_from_open_cells()
        self.end_time = time.time()
        
    def __get_deadends(self):
        ends = []
        
        for i in range(self.w):
            for j in range(self.h):
                val = self.tmp_grid[i,j]
                check = val == DIRECTIONS["N"] or val == DIRECTIONS["S"]
                check = check or val == DIRECTIONS["E"] or val == DIRECTIONS["W"]
                check = check and (i, j) != self.start_point and (i, j) != self.end_point
                
                if check:
                    ends.append((i, j))
    
        return ends
    
    def __x_out_points(self, ends):
        for e in ends:
            x, y = e
            self.x_grid[x, y] = 0x1
            val = self.tmp_grid[x, y]
            if val == DIRECTIONS["N"]:
                self.tmp_grid[x, y] = 0x0
                self.tmp_grid[x-1, y] ^= DIRECTIONS["S"]
            if val == DIRECTIONS["S"]:
                self.tmp_grid[x, y] = 0x0
                self.tmp_grid[x+1, y] ^= DIRECTIONS["N"]
            if val == DIRECTIONS["E"]:
                self.tmp_grid[x, y] = 0x0
                self.tmp_grid[x, y+1] ^= DIRECTIONS["W"]
            if val == DIRECTIONS["W"]:
                self.tmp_grid[x, y] = 0x0
                self.tmp_grid[x, y-1] ^= DIRECTIONS["E"]
        self.x_grid_array.append(np.copy(self.x_grid))
    
    def __get_path_from_open_cells(self):
        i, j = (0, 0)
        while True:
            val = self.tmp_grid[i, j]
            if val == DIRECTIONS["S"]:
                self.path.append(((i, j), (i+1, j)))
                self.tmp_grid[i+1, j] ^= DIRECTIONS["N"]
                i = i+1
            if val == DIRECTIONS["N"]:
                self.path.append(((i, j), (i-1, j)))
                self.tmp_grid[i-1, j] ^= DIRECTIONS["S"]
                i = i-1
            if val == DIRECTIONS["E"]:
                self.path.append(((i, j), (i, j+1)))
                self.tmp_grid[i, j+1] ^= DIRECTIONS["W"]
                j = j+1
            if val == DIRECTIONS["W"]:
                self.path.append(((i, j), (i, j-1)))
                self.tmp_grid[i, j-1] ^= DIRECTIONS["E"]
                j = j-1
                
            if (i, j) == self.end_point:
                break


def get_solv(name):
    solv_types = {
        "recursive_dfs": RecursiveDFS,
        "bfs": BFS,
        "deadend_filling": DeadEndFilling
    }
    
    if name not in solv_types:
        print("type not supported")
        quit()
        
    return solv_types[name]