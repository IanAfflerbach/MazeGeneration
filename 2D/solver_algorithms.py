import numpy as np
import utilities as util
from utilities import DIRECTIONS

class SolverBase:
    def __init__(self, grid):
        self.grid = grid
        self.w, self.h = np.shape(self.grid)
        self.start_point = (0, 0)
        self.end_point = (self.w - 1, self.h - 1)
        self.path = []
        return
        
    def solve(self):
        print("Solving!")
        return
        
        
class RecursiveDFS(SolverBase):
    def __init__(self, grid):
        super().__init__(grid)
        
    def solve(self):
        self.visited_points = np.zeros((self.w, self.h), dtype=int)        
        result = self.__move(self.start_point)
        
        if result == -1:
            print("ERROR: maze is disconnected")
        
    def __move(self, point):
        x, y = point
        self.visited_points[x, y] = 1
        
        if (point == self.end_point):
            return 1
        
        result = -1
        if result == -1 and self.grid[x, y] & DIRECTIONS["S"] != 0x0 and self.visited_points[x + 1, y] == 0:
            self.path.append(((x, y), (x + 1, y)))
            result = self.__move((x + 1, y))
            if result == -1:
                self.path.pop()
        if result == -1 and self.grid[x, y] & DIRECTIONS["N"] != 0x0 and self.visited_points[x - 1, y] == 0:
            self.path.append(((x, y), (x - 1, y)))
            result = self.__move((x - 1, y))
            if result == -1:
                self.path.pop()
        if result == -1 and self.grid[x, y] & DIRECTIONS["E"] != 0x0 and self.visited_points[x, y + 1] == 0:
            self.path.append(((x, y), (x, y + 1)))
            result = self.__move((x, y + 1))
            if result == -1:
                self.path.pop()
        if result == -1 and self.grid[x, y] & DIRECTIONS["W"] != 0x0 and self.visited_points[x, y - 1] == 0:
            self.path.append(((x, y), (x, y - 1)))
            result = self.__move((x, y - 1))
            if result == -1:
                self.path.pop()
        
        return result
        