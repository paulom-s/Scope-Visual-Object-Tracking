# source .venv/bin/activate

import time
import Dependencies.com_scope as com_scope

v_az,v_alt = input('Az and Alt speed ? (X.X,X.X with maximum 3)').split(',')
v_az = float(v_az)
v_alt = float(v_alt)
duration = input('Movement duration ? (XX in s)')
duration = float(duration)
com_scope.move(v_az,v_alt,0)
time.sleep(duration)
com_scope.stop()