import time

from djitellopy import tello
from time import sleep

drone = tello.Tello()
drone.connect()
print(drone.get_battery())
print(drone.is_flying)
drone.takeoff()
print(drone.is_flying)
time.sleep(1)
print(drone.get_height(),"height")
print(drone.get_pitch(),"pitch")
print(drone.get_yaw(),"yaw")
drone.land()

# drone.takeoff()
# drone.send_rc_control(left/right,forward/backward,up/down,yaw) values between -100 to 100
# sleep(2)
# drone.land()
