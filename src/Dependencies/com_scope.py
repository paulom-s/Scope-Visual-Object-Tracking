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
    move(0,0,1,0)

def move(v_az,v_alt,stopping,mirror):
    if stopping == 0:
        print('Correcting...')
    if abs(v_az) > 3 or abs(v_alt) > 3:
        stop()
        print('Error : Speed > 3')
    else:
        if mirror == 1:
            mount.slew_variable(nexstar.NexstarDeviceId.AZM_RA_MOTOR, -v_az)
            mount.slew_variable(nexstar.NexstarDeviceId.ALT_DEC_MOTOR, v_alt)
        else:
            mount.slew_variable(nexstar.NexstarDeviceId.AZM_RA_MOTOR, -v_az)
            mount.slew_variable(nexstar.NexstarDeviceId.ALT_DEC_MOTOR, -v_alt)