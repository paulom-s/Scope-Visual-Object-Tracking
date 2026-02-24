#for Linux:         source .venv/bin/activate
#for Windows:       .venv/Scripts/activate

#import com_apn
#import com_tel
import functions_demo as f
import time
import cv2

img=cv2.imread(r'data/Camera_Output/test_1234.jpg')

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
        answer=input('Threshold and H.P. Correction (xxx,x) ? (enter "-1" to confirm)')
        time.sleep(0.5)
        if answer=='-1':
            cv2.destroyWindow('Preview')
            break
        else:
            thr,ker=answer.split(',')
            thr = int(thr)
            ker = int(ker)
            if not (0 <= thr <= 255):
                print('Threshold value error ! Pls enter a number between 0 and 255.')
            elif not (1 <= ker <= 20):
                print('Hot pixels corrector value error ! Pls enter a number between 1 and 20.')
            else:
                img_clean=f.clean2(img,thr,ker)
                f.analyze2(img_clean,img)

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
        img_clean = f.clean(img,g_thr,g_ker)
        pla_pos = f.analyze(img_clean)
        positions.append(pla_pos)
        time.sleep(5)

        for a in range(duration):
            print('')
            print('Downloading Live View...')
            img_clean = f.clean(img,g_thr,g_ker)
            pla_pos = f.analyze(img_clean)
            positions.append(pla_pos)
            print('Thinking...')
            print('Correcting...')
            time.sleep(5)


test()
follow(input('Tracking duration (in seconds) ?'))