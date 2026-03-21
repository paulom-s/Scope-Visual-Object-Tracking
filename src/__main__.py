# source .venv/bin/activate

import Dependencies.com_apn as com_apn
import Dependencies.com_scope as com_scope
import Dependencies.functions as f
import time
import cv2

def init():
    global g_thr,g_ker
    thr = 255
    ker = 0
    img = com_apn.capture_LV()
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
            
    return pixel_size,focal,iteration,refresh_time,mirror

def def_pixel_scale(pixel_size,focal):
    pixel_scale = ((206.265 * pixel_size) / focal) / 3600
    return pixel_scale

def follow(pixel_scale,iteration,refresh_time,mirror):
    positions = []
    v_az = 0
    v_alt = 0
    print('')
    img = com_apn.capture_LV()
    cv2.imshow('Preview',img)
    cv2.waitKey(1)
    img_clean = f.clean(img,g_thr,g_ker)
    pla_pos = f.analyze(img_clean)
    positions.append(pla_pos)
    c_az,c_alt = com_scope.calculate_correction(pixel_scale,refresh_time,positions)
    com_scope.move(v_az,v_alt,c_az,c_alt,0,mirror)
    time.sleep(refresh_time)

    for a in range(iteration-1):
        print('')
        img = com_apn.capture_LV()
        cv2.imshow('Preview',img)
        cv2.waitKey(1)
        img_clean = f.clean(img,g_thr,g_ker)
        pla_pos = f.analyze(img_clean)
        positions.append(pla_pos)
        v_az, v_alt = com_scope.calculate_speed(pixel_scale,refresh_time,positions,c_az,c_alt)
        c_az,c_alt = com_scope.calculate_correction(pixel_scale,refresh_time,positions)
        com_scope.move(v_az,v_alt,c_az,c_alt,0,mirror)
        time.sleep(refresh_time)

    com_scope.stop()
        
init()
pixel_size,focal,iteration,refresh_time,mirror = def_var()
pixel_scale = def_pixel_scale(pixel_size,focal)
follow(pixel_scale,iteration,refresh_time,mirror)