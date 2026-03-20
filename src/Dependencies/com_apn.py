import gphoto2 as gp2
import os
import cv2
import numpy as np

os.system('pkill -f gvfsd-gphoto2')

context = gp2.Context()
cam = gp2.Camera()
cam.init()

def set(param, value):
    config = cam.get_config()
    child = config.get_child_by_name(param)
    child.set_value(value)
    cam.set_config(config)

def capture_LV():
    print('Downloading LiveView...')
    preview = cam.capture_preview()
    img = preview.get_data_and_size()
    img = np.frombuffer(img, dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img

cam.exit()