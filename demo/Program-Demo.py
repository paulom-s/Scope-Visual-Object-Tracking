#for Linux:         source .venv/bin/activate
#for Windows:       .venv/Scripts/activate

#import com_apn
#import com_tel
#import functions as f
import time
import cv2
import numpy as np
import sys

img=cv2.imread(r'data/Camera_Output/test_1234.jpg')

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
    else:
        print('Error: No object detected !')
        sys.exit()

def analyze2(img,img_prev):
    img_prev = img_prev.copy()
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

def test():
    global g_thr,g_ker
    thr = 255
    ker = 0
    print('Downloading Live View...')
    print('Live view image. Press any key to continue...')
    cv2.imshow('Preview',img)
    cv2.waitKey(0)
    while True:
        g_thr = thr
        g_ker = ker
        answer=input('Threshold and Object Size (xxx,xxx) ? (enter "-1" to confirm)')
        time.sleep(0.5)
        if answer=='-1':
            cv2.destroyWindow('Preview')
            break
        else:
            thr,ker=answer.split(',')
            thr = int(thr)
            ker = int(ker)
            ker = round(ker/10)
            ker = int(ker)
            if ker > 10 :
                ker = 10
            if not (0 <= thr <= 255):
                print('Threshold value error ! Pls enter a number between 0 and 255.')
            elif not (2 <= ker <= 640):
                print('Object Size value error ! Pls enter a number between 15 and 640.')
            else:
                img_clean=clean2(img,thr,ker)
                analyze2(img_clean,img)

def follow():
    global positions

    duration,refresh_time = input('Tracking Duration and Refresh Time ? (XXX,XX in seconds)').split(',')
    refresh_time = float(refresh_time)
    duration = float(duration)
    if duration < 15:
        print('Pls, select a Duration >= 15.')
        follow()
    elif duration > 7200:
        print('Pls, select a Duration <= 7200.')
        follow()
    else:
        if refresh_time >= 5:
            refresh_time = round(refresh_time/2.5,0)*2.5
            refresh_time = float(refresh_time)
        else:
            refresh_time = round(refresh_time/0.5,0)*0.5
            refresh_time = float(refresh_time)
            if refresh_time == 0:
                refresh_time = 0.5
        duration = round(duration/refresh_time,0)
        duration = int(duration)
        if duration < 3:
            print('Pls, select a Duration wich is at least 3x the Refresh Time.')
            follow()

        else:
            print('Downloading Live View...')
            img_clean = clean(img,g_thr,g_ker)
            analyze(img_clean)
            time.sleep(refresh_time)

            for a in range(duration-1):
                print('')
                print('Downloading Live View...')
                print('Thinking...')
                print('Correcting...')
                time.sleep(refresh_time)


test()
follow()