# source .venv/bin/activate

import cv2
import numpy as np

img=cv2.imread(r'data/Camera_Output/test_analyzing.jpg')

def clean3(img,thr,ker):
    kernel = np.ones((ker,ker), np.uint8)

    cv2.imshow('Preview',img)
    cv2.waitKey(0)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Preview',img_gray)
    cv2.waitKey(0)

    ret, img_bin = cv2.threshold(img_gray,thr, 255, cv2.THRESH_BINARY)
    cv2.imshow('Preview',img_bin)
    cv2.waitKey(0)

    img_clean = cv2.erode(img_bin, kernel, iterations=1)
    cv2.imshow('Preview',img_clean)
    cv2.waitKey(0)

    img_clean = cv2.dilate(img_clean, kernel, iterations=1)
    cv2.imshow('Preview',img_clean)
    cv2.waitKey(0)

    return img_clean

def analyse3(img_clean,img):
    img_prev = img.copy()
    img_clean_prev = img_clean.copy()

    M = cv2.moments(img_clean)
    if M['m00'] != 0:
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])

    img_clean_prev = cv2.cvtColor(img_clean_prev, cv2.COLOR_GRAY2BGR)
    cv2.drawMarker(img_clean_prev, (cX, cY), (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)
    cv2.drawMarker(img_prev, (cX, cY), (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)

    x, y, w, h = cv2.boundingRect(img_clean)
    cv2.rectangle(img_clean_prev, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.rectangle(img_prev, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imshow('Preview',img_clean_prev)
    cv2.waitKey(0)
    cv2.imshow('Preview',img_prev)
    cv2.waitKey(0)

analyse3(clean3(img,50,5),img)