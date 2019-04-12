# coding: utf-8
from __future__ import print_function
import sys

import requests
import json
import urllib
import numpy as np
import cv2
import base64
import cv_functions

def ocr(image_url, google_api_key, positions=[], original_size=None, anchor_url=None):

    if positions and not original_size:
        raise ValueError("Please specifiy the original size when providing positions")

    req = urllib.urlopen(image_url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr,-1)
    height, width, channels = img.shape

    #1. filter for color, noise
    #*monochrome化する？
    ret1,th1 = cv2.threshold(img,200,255,cv2.THRESH_TRUNC)

    #2. angle fix (be careful to use because of too many magic numbers)
    #img = cv_functions.angle_fix(img)

    #3a. If no positions specified send the whole image to the OCR API
    if not positions:
        ret, img_raw = cv2.imencode(".png", img)
        text, confidence = google_ocr(img_raw, google_api_key)
        return text

    #3b. Crops the positions
    req = urllib.urlopen(anchor_url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    anc_img = cv2.imdecode(arr,-1)

    anc_img_resize, ratio = cv_functions.resize_by_ratio(width,original_size["width"],anc_img)

    # ratio = width*1.0/original_size["width"]

    # Detect the anchor
    if anchor_url:
        if ratio > 2.0 or ratio < 0.66:
            print("WARNING: Please use the similar resolution of the registered document size. {}px * {}px is the registered size."\
                    .format(original_size["width"], original_size["height"]), file=sys.stderr)
        else:
            anc_similarity, anc_xy = cv_functions.anchor_match(img,anc_img_resize)

    images = []
    #crop images and throw them to OCR API
    for pos in positions:

        x1 = int(anc_xy[0] + pos["x1"]*ratio)
        x2 = int(anc_xy[0] + pos["x2"]*ratio)
        y1 = int(anc_xy[1] + pos["y1"]*ratio)
        y2 = int(anc_xy[1] + pos["y2"]*ratio)

        crop = th1[y1:y2,x1:x2]
        ret, img_raw = cv2.imencode(".png",crop)
        images.append(img_raw)


    # OCR（GCP）にかける
    res, confidence = google_ocr(images, google_api_key)
    return res


## Google Cloud APIの場合
def google_ocr(images, api_key):

    if not isinstance(images, list):
        images = [images]

    annotate_requests = [{
      "image": {
        "content": base64.b64encode(img)
      },
      "features":[
        {
          "type":"TEXT_DETECTION",
          "maxResults":1
        }
      ]
    } for img in images]

    #OCR
    url = "https://vision.googleapis.com/v1/images:annotate?key=" + api_key
    request_body = { "requests": annotate_requests }
    r = requests.post(url, json=request_body)
    json_res = r.json()
    confidence = "not provided"
    return json_res, confidence

#original deep learning algorithm #not built yet
def LSTM(img):
	text = "text"
	confidence = "confidence"
	return text, confidence
