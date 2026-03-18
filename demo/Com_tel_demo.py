import nexstar
import time

mount = nexstar.NexstarHandController('/dev/ttyUSB0')

def stop():
    print('Stopping mount...')
    move(0,0,1)

def move(v_az, v_alt,stopping):
    if stopping == 0:
        print('Moving...')
    if v_az > 3 or v_alt > 3:
        stop()
        print('Error : Speed > 3')
    else:
        mount.slew_variable(nexstar.NexstarDeviceId.AZM_RA_MOTOR, v_az)
        mount.slew_variable(nexstar.NexstarDeviceId.ALT_DEC_MOTOR, v_alt)

x = input('Az and Alt speed ? (X.X,X.X with maximum 3)')
az,alt = x.split(',')
az = float(az)
alt = float(alt)
duration = input('Movement duration ? (XX in s)')
duration = float(duration)
move(az,alt,0)
time.sleep(duration)
stop()