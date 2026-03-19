#for Linux:         source .venv/bin/activate
#for Windows:       .venv/Scripts/activate

import com_apn
import com_tel
import functions as f
import time
import cv2

def test():
    global g_thr,g_ker
    thr = 255
    ker = 0
    img = com_apn.capture_LV()
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
            elif not (1 <= ker <= 640):
                print('Object Size value error ! Pls enter a number between 20 and 640.')
            else:
                img_clean=f.clean2(img,thr,ker)
                f.analyze2(img_clean,img)

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
            img = com_apn.capture_LV()
            positions = []
            img_clean = f.clean(img,g_thr,g_ker)
            pla_pos = f.analyze(img_clean)
            positions.append(pla_pos)
            time.sleep(refresh_time)

            for a in range(duration-1):
                print('')
                img = com_apn.capture_LV()
                img_clean = f.clean(img,g_thr,g_ker)
                pla_pos = f.analyze(img_clean)
                positions.append(pla_pos)
                com_tel.calculate_speed(positions,refresh_time)
                com_tel.move(0,0)
                time.sleep(refresh_time)


test()
follow()