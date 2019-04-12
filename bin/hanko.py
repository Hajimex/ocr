
# coding: utf-8
import sys,os
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name + "/src")
import cv_functions
import argparse
import cv2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='create a new format type')
    parser.add_argument('-i', type=str, help='image url', required=True)
    parser.add_argument('-k', type=str, help='AWS Access Key ID', required=True)
    parser.add_argument('-s', type=str, help='AWS Secret Access Key', required=True)
    parser.add_argument('-b', type=str, help='AWS S3 bucket', required=True)
    args = parser.parse_args()

    print("main start")
    res = cv_functions.detect_blob(args.i,args.k,args.s,args.b)

    print res