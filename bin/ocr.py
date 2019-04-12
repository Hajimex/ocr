# coding: utf-8
from __future__ import print_function

import argparse
import sys,os
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name + "/src")

import ocr_functions
import json

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Does ocr a picture to a text')
  parser.add_argument('-i', type=str, help='image url', required=True)
  parser.add_argument('-k', type=str, help='api key', default=os.getenv('GOOGLE_API_KEY'))
  parser.add_argument('-p', type=str, help='text area relative_positions', default='[]')
  parser.add_argument('-s', type=str, help='image original size')
  parser.add_argument('-a', type=str, help='anchor url')

  # for future usage
  # parser.add_argument('-c', type=str, help='character type', required=True)
  # parser.add_argument('-d', type=bool, help='use dictionary or not', required=True)

  args = parser.parse_args()
  args.p = json.loads(args.p)
  if args.s:
    args.s = json.loads(args.s)

  res = ocr_functions.ocr(args.i, args.k, anchor_url=args.a, original_size=args.s, positions=args.p)
  print(json.dumps(res))
