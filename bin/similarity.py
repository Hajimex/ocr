# coding: utf-8
import argparse
import numpy as np
import cv2
import sys,os
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name + "/src")
import cv_functions
import ocr_functions
import json


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='create a new format type')
    parser.add_argument('-i', type=str, help='image url', required=True)
    parser.add_argument('-p', type=str, help='CLI file path', required=True)
    args = parser.parse_args()
    print("main start")

    #json file
    f = open(args.p, 'r')
    d = json.load(f)

    res = cv_functions.similarity(args.i,d)
    print res
