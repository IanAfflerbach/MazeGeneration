import numpy as np
import cv2

def main():
    img = np.zeros([256,256,3])

    img[:,:,0] = np.ones([256,256])
    img[:,:,1] = np.ones([256,256]) * 0.0
    img[:,:,2] = np.ones([256,256])
    
    cv2.imshow('Color image', img)
    cv2.waitKey(0)
    
    # if cv2.waitKey(10) == 27:                     # exit if Escape is hit
    #     break
    return
    
if __name__ == "__main__":
    main()