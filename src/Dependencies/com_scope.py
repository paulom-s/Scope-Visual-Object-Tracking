import nexstar

mount = nexstar.NexstarHandController('/dev/ttyUSB0')

def calculate_speed(pixel_scale,refresh_time,positions,c_az,c_alt):
    print('Thinking...')
    v_az = (((positions[-1][0] - positions[-2][0]) * pixel_scale) + (c_az * refresh_time)) / refresh_time
    v_alt = (((positions[-1][1] - positions[-2][1]) * pixel_scale) + (c_alt * refresh_time)) / refresh_time
    return v_az,v_alt

def calculate_correction(pixel_scale,refresh_time,positions):
    c_az = ((positions[-1][0] - 480) * pixel_scale) / refresh_time
    c_alt = ((positions[-1][1] - 320) * pixel_scale) / refresh_time
    return c_az,c_alt

def stop():
    print('')
    print("Stopping mount...")
    move(0,0,0,0,1,0)

def move(v_az,v_alt,c_az,c_alt,stopping,mirror):
    if stopping == 0:
        print('Correcting...')
    if abs(v_az) > 3 or abs(v_alt) > 3:
        stop()
        print('Error : Speed > 3')
    else:
        if mirror == 1:
            mount.slew_variable(nexstar.NexstarDeviceId.AZM_RA_MOTOR, -1 * (-1 * (v_az + c_az)))
            mount.slew_variable(nexstar.NexstarDeviceId.ALT_DEC_MOTOR, -1 * (-1 * (v_alt + c_alt)))
        else:
            mount.slew_variable(nexstar.NexstarDeviceId.AZM_RA_MOTOR, -1 * (-1 * (v_az + c_az)))
            mount.slew_variable(nexstar.NexstarDeviceId.ALT_DEC_MOTOR, -1 * (-1 * (v_alt + c_alt)))