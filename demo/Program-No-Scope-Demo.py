# source .venv/bin/activate

#import com_apn
#import com_tel
import Dependencies.functions_no_scope as f
import time
import cv2

img = cv2.imread(r'data/Camera_Output/test_analyzing.jpg')

def init():
    global g_thr,g_ker
    thr = 255
    ker = 0
    print('Downloading LiveView...')
    print('Live view image. Press any key to continue...')
    cv2.imshow('Preview',img)
    cv2.waitKey(0)
    answer = 0
    while not answer == '-1':
        g_thr = thr
        g_ker = ker
        answer=input('Threshold and Object Size (xxx,xxx) ? (enter "-1" to confirm)')
        if not answer == '-1':
            thr,ker=answer.split(',')
            thr = int(thr)
            ker = int(ker)
            ker = round(ker/10)
            ker = int(ker)
            if ker > 10 :
                ker = 10
            if not (0 <= thr <= 255):
                print('Threshold value error ! Pls enter a number between 0 and 255.')
            elif not (1 <= ker <= 640):
                print('Object Size value error ! Pls enter a number between 20 and 640.')
            else:
                img_clean=f.clean2(img,thr,ker)
                f.analyze2(img_clean,img)
    cv2.destroyWindow('Preview')

def def_var():
    duration = 0
    refresh_time = 0
    while not (15<=duration<=7200) or not (3<=iteration):
        duration,refresh_time = input('Tracking Duration and Refresh Time ? (XXX,XX in seconds)').split(',')
        refresh_time = float(refresh_time)
        duration = float(duration)
        if duration < 15:
            print('Pls, select a Duration >= 15.')
        elif duration > 7200:
            print('Pls, select a Duration <= 7200.')
        else:
            if refresh_time >= 5:
                refresh_time = round(refresh_time/2.5,0)*2.5
                refresh_time = float(refresh_time)
            else:
                refresh_time = round(refresh_time/0.5,0)*0.5
                refresh_time = float(refresh_time)
                if refresh_time == 0:
                    refresh_time = 0.5
            
            iteration = round(duration/refresh_time,0)
            iteration = int(iteration)
            if iteration < 3:
                print('Pls, select a Duration wich is at least 3x the Refresh Time.')
    
    pixel_size = 0
    focal = 0
    while not (0.5<=pixel_size<=6) or not (15<=focal<=3000):
        pixel_size,focal = input('Pixel Size (um) and Focal Length (mm) ? (X.X,XXXX)').split(',')
        pixel_size = float(pixel_size)
        focal = float(focal)
        focal = int(round(focal,0))
        if pixel_size<0.5:
            print('Pls, select a Pixel Size >= 0.5 um.')
        elif pixel_size>6:
            print('Pls, select a Pixel Size <= 6 um.')
        else:
            if focal<15:
                print('Pls, select a Focal Length >= 15 mm.')
            elif pixel_size>6:
                print('Pls, select a Focal Length <= 3000 mm.')
    
    mirror = -1
    while mirror != 0 and mirror != 1:
        mirror = input('Vertically Mirror Image ? (Yes = 1, No = 0)')
        mirror = int(mirror)
        if not mirror == 0 or mirror == 1:
            print('Pls, select 0 for "No" or 1 for "Yes".')
            
    return iteration,refresh_time

def follow(iteration,refresh_time):
    print('Downloading LiveView...')
    img_clean = f.clean(img,g_thr,g_ker)
    pla_pos = f.analyze(img_clean)
    time.sleep(refresh_time)

    for a in range(iteration-1):
        print('')
        print('Downloading LiveView...')
        print('Cleaning...')
        print('Analyzing...')
        print('Thinking...')
        print('Correcting...')
        time.sleep(refresh_time)

    print('')
    print("Stopping mount...")
            
init()
iteration,refresh_time = def_var()
follow(iteration,refresh_time)