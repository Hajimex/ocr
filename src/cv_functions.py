# coding: utf-8
import numpy as np
import cv2
from scipy import ndimage
from PIL import Image
import os
import urllib
import tinys3
import uuid

def anchor_match(img,anc_img):
    img_edges = cv2.Canny(img,100,200,apertureSize = 3)
    anc_edges = cv2.Canny(anc_img,100,200,apertureSize = 3)

    result = cv2.matchTemplate(img_edges,anc_edges,cv2.TM_CCOEFF_NORMED)
    
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    return max_val, max_loc

def resize_by_ratio(width,original_width,img):
    ratio = width*1.0/original_width
    if ratio > 1.0:
        interpolation = cv2.INTER_CUBIC
    else:
        interpolation = cv2.INTER_AREA
    
    height, width, _ = img.shape
    img_resize = cv2.resize(img,(int(width*ratio),int(height*ratio)),interpolation=interpolation)
    return img_resize,ratio

def similarity(img,formats):
    req = urllib.urlopen(img)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr,-1)
    
    res = {}
    for f in formats:
        anc_req = urllib.urlopen(f["anchor_url"])
        anc_arr = np.asarray(bytearray(anc_req.read()), dtype=np.uint8)
        anc_img = cv2.imdecode(anc_arr,-1)
        anc_img_resize, ratio = resize_by_ratio(width,f["format_size"]["width"],anc_img)
        if ratio > 2.0 or ratio < 0.66:
            res[f["anchor_url"]] = None
        else: 
            anc_similarity, anc_xy = anchor_match(img,anc_img_resize)
            res[f["anchor_url"]] = anc_similarity

    return res

def angle_fix(img):

    edges = cv2.Canny(img,100,200,apertureSize = 3)

    minLineLength = 800
    maxLineGap = 50
    threshold = 150
    lines = cv2.HoughLinesP(edges,1,np.pi/360,threshold=threshold,minLineLength=minLineLength,maxLineGap=maxLineGap)
            
    angle = 0
    horizon_lines = 0
    diff = 10
    for x in range(0, len(lines)):
        for x1,y1,x2,y2 in lines[x]:
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
            deg = np.rad2deg(np.arctan2(x2 - x1, y2 - y1))-90
            if deg > diff and deg < diff:
                angle += deg
                horizon_lines += 1

    angle = angle/horizon_lines

    img = ndimage.interpolation.rotate(img, -1 * angle, reshape=False)

    return img

def make_transparent(crop):

    tmp = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    _, tmp = cv2.threshold(tmp, 200, 255, cv2.THRESH_BINARY)
    alpha = cv2.bitwise_not(tmp)
    b, g, r = cv2.split(crop)
    rgba = [b,g,r, alpha]
    trsp = cv2.merge(rgba,4)
    
    file_name = "trsp_" + str(uuid.uuid4()) + ".png"

    cv2.imwrite(file_name, trsp)

    return file_name

def s3_upload(file_name,aws_ID,aws_key,aws_bucket):
    conn = tinys3.Connection(aws_ID,aws_key,tls=True)
    f = open(file_name,'rb')
    r = conn.upload(file_name,f,aws_bucket)
    url = r.url

    return url

def detect_blob(img,aws_ID,aws_key,aws_bucket):
    # 1. imgを読み込む
    req = urllib.urlopen(img)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr,-1)

    # 2. blobを見つける (1 or n)
    edges = cv2.Canny(img,100,200,apertureSize = 3)
    image, contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 3. blobsの数だけcropして、透過する。そしてアップロードする
    file_names = []
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        if (w > 50 and w < 300) and (h > 50 and h < 300):
            crop = img[y:y+h,x:x+w]
            file_name = make_transparent(crop)
            file_names.append(file_name)

    # 4. S3にアップロードしてURLを返す
    urls = []
    for file_name in file_names:
        url = s3_upload(file_name,aws_ID,aws_key,aws_bucket)
        urls.append(url)
        os.remove(file_name)

    return urls

