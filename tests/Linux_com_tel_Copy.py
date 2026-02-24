import time
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)

def move(delta_alt, delta_az):
    ser.write(b'z')
    alt_az = ser.read(18)
    print(alt_az)
    alt_az = alt_az.decode()
    print(alt_az)
    alt_az = alt_az.replace('#', '')
    print(alt_az)
    alt_az = alt_az.split(',')
    print(alt_az)
    az = int(alt_az[0], 16)
    alt = int(alt_az[1], 16)
    az = az >> 16
    alt = alt >> 16
    print(alt,az)

    delta_az = int((delta_az * 65536) / 360)
    delta_alt = int((delta_alt * 65536) / 360)
    
    new_az = (az + delta_az) % 65536
    new_alt = (alt + delta_alt) % 65536
    
    cmd = f"b{new_az:04X}{new_alt:04X}#"
    print(cmd)
    cmd = cmd.encode()
    print(cmd)
    ser.write(cmd)

move(10,0)

time.sleep(2)
ser.close()