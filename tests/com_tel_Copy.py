import serial
import time

tel = serial.Serial('COM5', 9600, timeout=2)
time.sleep(0.5)
tel.write(b'V')
if tel.read(2)==b'\x05#':
    print(f"Connected to the scope.")
else:
    print("Error: Unable to connect to the scope.")

def move(direction, vitesse, duree):
    cmd = None
    if direction == 'right':
        cmd = b'\x50\x03\x10\x02' + bytes([vitesse]) + b'\x00\x00\x00'
    elif direction == 'left':
        cmd = b'\x50\x03\x10\x03' + bytes([vitesse]) + b'\x00\x00\x00'
    elif direction == 'up':
        cmd = b'\x50\x03\x11\x03' + bytes([vitesse]) + b'\x00\x00\x00'
    elif direction == 'down':
        cmd = b'\x50\x03\x11\x02' + bytes([vitesse]) + b'\x00\x00\x00'

    if cmd:
        tel.write(cmd)
        time.sleep(duree)
        tel.write(cmd[:4] + b'\x00\x00\x00\x00')

#move('up',9,1)
tel.reset_input_buffer()
tel.write(b'\x50\x03\x10\x02\x09\x00\x00\x00')
response = tel.read(1) 
print(f"Réponse raquette: {response}")
time.sleep(1)

tel.close()