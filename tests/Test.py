import nexstar
import time

mount = nexstar.NexstarHandController('/dev/ttyUSB0')

def calculate_speed():
    print('Thinking...')

def stop():
    print('Stopping mount...')
    move(0,0)

def move(v_az, v_alt):
    print('Correcting...')
    if v_az > 3.5 or v_alt > 3.5:
        stop()
    else:
        mount.slew_variable(nexstar.NexstarDeviceId.AZM_RA_MOTOR, v_az)
        mount.slew_variable(nexstar.NexstarDeviceId.ALT_DEC_MOTOR, v_alt)

x = input('Az and Alt speed ? (X,X with maximum 3.5)')
x.split(',')
az = float(x[0])
alt = float(x[1])
move(az,alt)
time.sleep(2)
stop()