import cv2
import numpy as np

def clean(img,thr,ker):
    print('Cleaning...')
    kernel = np.ones((ker,ker), np.uint8)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img_bin = cv2.threshold(img_gray,thr, 255, cv2.THRESH_BINARY)
    img_clean = cv2.erode(img_bin, kernel, iterations=1)
    img_clean = cv2.dilate(img_clean, kernel, iterations=1)
    return img_clean

def clean2(img,thr,ker):
    kernel = np.ones((ker,ker), np.uint8)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img_bin = cv2.threshold(img_gray,thr, 255, cv2.THRESH_BINARY)
    print('Binary image. Press any key to continue...')
    cv2.imshow('Preview',img_bin)
    cv2.waitKey(0)
    img_clean = cv2.erode(img_bin, kernel, iterations=1)
    img_clean = cv2.dilate(img_clean, kernel, iterations=1)
    print('Cleaned image. Press any key to continue...')
    cv2.imshow('Preview',img_clean)
    cv2.waitKey(0)
    return img_clean

def analyze(img):
    print('Analyzing...')
    M = cv2.moments(img)
    if M['m00'] != 0:
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])
    return((cX,cY))

def analyze2(img,img_prev):
    M = cv2.moments(img)
    if M['m00'] != 0:
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])

        cv2.drawMarker(img_prev, (cX, cY), (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)
        x, y, w, h = cv2.boundingRect(img)
        cv2.rectangle(img_prev, (x, y), (x + w, y + h), (0, 0, 255), 2)
        print('Analyzed image. Press any key to continue...')
        cv2.imshow('Preview',img_prev)
        cv2.waitKey(0)
    else:
        print('Error: No object detected !')