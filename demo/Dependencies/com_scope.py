import nexstar

mount = nexstar.NexstarHandController('/dev/ttyUSB0')

def calculate_speed(pixel_scale,refresh_time,pla_pos):
    print('Thinking...')

    v_az = (pla_pos[0] * pixel_scale) / refresh_time
    v_alt = (pla_pos[1] * pixel_scale) / refresh_time

    return -v_az,-v_alt

def stop():
    print('')
    print("Stopping mount...")
    move(0,0,1)

def move(v_az,v_alt,stopping):
    if stopping == 0:
        print('Correcting...')
    if v_az > 3 or v_alt > 3:
        stop()
        print('Error : Speed > 3')
    else:
        mount.slew_variable(nexstar.NexstarDeviceId.AZM_RA_MOTOR, v_az)
        mount.slew_variable(nexstar.NexstarDeviceId.ALT_DEC_MOTOR, v_alt)