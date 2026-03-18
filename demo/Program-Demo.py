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
    thr = 0
    ker = 1
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

def follow(duration):
    global positions
    duration = float(duration)
    duration = round(duration/50,1)*10-1
    duration = int(duration)
    if duration<2:
        print('Tracking time too short ! Pls select a number > 12.5')
        follow(input('Tracking duration (in seconds) ?'))
    elif duration>41:
        print('Tracking time too long ! Pls select a number < 212.4')
        follow(input('Tracking duration (in seconds) ?'))
    else:
        print('Downloading Live View...')
        positions = []
        img_clean = clean(img,g_thr,g_ker)
        pla_pos = analyze(img_clean)
        positions.append(pla_pos)
        time.sleep(5)

        for a in range(duration):
            print('')
            print('Downloading Live View...')
            img_clean = clean(img,g_thr,g_ker)
            pla_pos = analyze(img_clean)
            positions.append(pla_pos)
            print('Thinking...')
            print('Correcting...')
            time.sleep(5)


test()
follow(input('Tracking duration (in seconds) ?'))