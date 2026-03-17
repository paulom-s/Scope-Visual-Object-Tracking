import time
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

def move(direction,speed):
    if direction=='up' or direction==1:
        ser.write(bytes([80, 2, 17, 36, speed, 0, 0, 0]))
    elif direction=='down' or direction==2:
        ser.write(bytes([80, 2, 17, 37, speed, 0, 0, 0]))
    elif direction=='left' or direction==3:
        ser.write(bytes([80, 2, 16, 37, speed, 0, 0, 0]))
    elif direction=='right' or direction==4:
        ser.write(bytes([80, 2, 16, 36, speed, 0, 0, 0]))

    ser.read(1)
    time.sleep(5)

    if direction=='up' or direction=='down' or direction==1 or direction==2:
        ser.write(bytes([80, 2, 17, 36, 0, 0, 0, 0]))
    else:
        ser.write(bytes([80, 2, 16, 36, 0, 0, 0, 0]))
    
    ser.read(1)

move('right',9)

ser.close()