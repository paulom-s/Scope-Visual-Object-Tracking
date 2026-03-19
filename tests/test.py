
def def_var():
    duration = 0
    refresh_time = 0
    while not (15<=duration<=7200) or not (3<=iteration):
        duration,refresh_time = input('Tracking Duration and Refresh Time ? (XXX,XX in seconds)').split(',')
        refresh_time = float(refresh_time)
        duration = float(duration)
        if duration < 15:
            print('Pls, select a Duration >= 15.')
        elif duration > 7200:
            print('Pls, select a Duration <= 7200.')
        else:
            if refresh_time >= 5:
                refresh_time = round(refresh_time/2.5,0)*2.5
                refresh_time = float(refresh_time)
            else:
                refresh_time = round(refresh_time/0.5,0)*0.5
                refresh_time = float(refresh_time)
                if refresh_time == 0:
                    refresh_time = 0.5
            
            iteration = round(duration/refresh_time,0)
            iteration = int(iteration)
            if iteration < 3:
                print('Pls, select a Duration wich is at least 3x the Refresh Time.')
    
    pixel_size = 0
    focal = 0
    while not (0.5<=pixel_size<=6) or not (15<=focal<=3000):
        pixel_size,focal = input('Pixel Size (um) and Focal Length (mm) ? (X.X,XXXX)').split(',')
        pixel_size = float(pixel_size)
        focal = float(focal)
        focal = int(round(focal,0))
        if pixel_size<0.5:
            print('Pls, select a Pixel Size >= 0.5 um.')
        elif pixel_size>6:
            print('Pls, select a Pixel Size <= 6 um.')
        else:
            if focal<15:
                print('Pls, select a Focal Length >= 15 mm.')
            elif pixel_size>6:
                print('Pls, select a Focal Length <= 3000 mm.')
    
    return pixel_size,focal,iteration,refresh_time       

print(def_var())
