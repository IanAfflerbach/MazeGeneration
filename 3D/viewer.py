import numpy as np
import cv2
import argparse

import utilities as util

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, help='maze file')
args = parser.parse_args()


def main():
    grid = util.import_txt_file(args.file)
    img = util.create_viewer_image(grid)
    resized = cv2.resize(img, (200,600), interpolation = cv2.INTER_AREA)

    cv2.imshow('Maze', resized)
    cv2.waitKey(0)
    

if __name__ == "__main__":
    main()