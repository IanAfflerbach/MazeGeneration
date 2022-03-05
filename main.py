import numpy as np
import cv2

import maze_algorithms as mazes
import utilities as util

def main():
    maze = mazes.KruskalsMaze(5, 5)
    maze_steps = maze.generate(True)
    
    for m in maze_steps:
        img = util.convert_maze_to_image_array(m)
        resized = cv2.resize(img, (600,600), interpolation = cv2.INTER_AREA)
        
        cv2.imshow('test', resized)
        cv2.waitKey(0)
    
if __name__ == "__main__":
    main()
    
    
'''
img = np.zeros([256,256,3])

img[:,:,0] = np.ones([256,256])
img[:,:,1] = np.ones([256,256]) * 0.0
img[:,:,2] = np.ones([256,256])

cv2.imshow('Color image', img)
cv2.waitKey(0)
'''