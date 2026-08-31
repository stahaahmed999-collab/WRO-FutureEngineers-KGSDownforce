#if divide by zero error: change the sensor/wire
#if it hits a wall, unplug and replug the sensor wire
#charge the robot if below 70%
import event, time, cyberpi, mbot2, mbuild, math


l = 35/90
r = 40/90
spd = 50

ANGLE_AVERAGE_SIZE = 6      #6 number of prev angles
ANGLE_AVERAGE_SIGMA = 3    #3 larger = flatter/smoother weighting
angle_history = []

def smooth_angle(angle):
    global angle_history

    angle_history.append(angle)

    if len(angle_history) > ANGLE_AVERAGE_SIZE:
        angle_history.pop(0)

    weighted_sum = 0
    weight_total = 0

    newest = len(angle_history) - 1

    for i in range(len(angle_history)):
        distance = newest - i

        #gaussian/normal distribution idk what its called
        weight = math.e**(-(distance**2)/(2*ANGLE_AVERAGE_SIGMA**2))

        weighted_sum += angle_history[i] * weight
        weight_total += weight

    return weighted_sum / weight_total


def display():
    cyberpi.display.rotate_to(-90)
    cyberpi.console.clear()
    cyberpi.console.println("Downforce Robot")
    cyberpi.console.println("L" + str(mbuild.ultrasonic2.get(1)))
    cyberpi.console.println("R" + str(mbuild.ultrasonic2.get(3)))
    cyberpi.console.println("F" + str(mbuild.ultrasonic2.get(2)))
    cyberpi.console.println(str(cyberpi.get_battery()) + "%")


def tsig(x,k):
    global l, r
    if x < 0:
        return (2*l / (1 + math.e**((-k*abs(x)**3)/x))) - l
    elif x == 0:
        return 0
    elif x > 0:
        return (2*r / (1 + math.e**((-k*abs(x)**3)/x))) - r


def get_angle(dl, dr, df):
    q_right = (dl / dr) - 1
    q_left = (dr / dl) - 1
    if q_left > q_right:
        return 90 - 90*tsig(-q_left, 7.5-(max(min(70,df),15)/(60/5))) #6.5 70 10 60/5
    else:
        return 90 - 90*tsig(q_right, 7.5-(max(min(70,df),15)/(60/5))) #6.5 70 10 60/5


@event.is_press('b')
def stop():
    cyberpi.stop_other()
    mbot2.EM_stop("ALL")
    mbot2.servo_set(85,"all")
    display()

def open():
    angle_history = []
   
    cyberpi.timer.reset()

    dl = 1
    dr = 1
    df = 1
    sublevel = 0
    detecting = False
    completed = False

    cyberpi.led.show('red black black black black')
   
    mbot2.forward(spd)

    while True:
       
        #display()
       
        try:
           
            temp = mbuild.ultrasonic2.get(1)
            #if temp != 300:
            dl = temp
            temp = mbuild.ultrasonic2.get(2)
            #if temp != 300:
            df = temp
            temp = mbuild.ultrasonic2.get(3)
            #if temp != 300:
            dr = temp
            time.sleep(0.05)
           
            a = get_angle(dl, dr, df) - 5
            a = smooth_angle(a)

            if 0 < df <= 10:
                cyberpi.timer.reset()
                mbot2.servo_set(-a + 180, "all")
                mbot2.backward(spd)
                while cyberpi.timer.get() <= 1.5:
                    if mbuild.quad_rgb_sensor.get_line_sta("all", 1) != 15:
                        if not detecting:
                            sublevel -= 1
                            cyberpi.led.move(-1)
                            detecting = True
                    else:
                        detecting = False
                    time.sleep(0.02)
                mbot2.forward(spd)

            mbot2.servo_set(a, "all")

            if mbuild.quad_rgb_sensor.get_line_sta("all", 1) != 15:
                if not detecting:
                    sublevel += 1
                    cyberpi.led.move(1)
                    detecting = True
            else:
                detecting = False

            if sublevel >= 12:
                if not completed:
                    completed = True
                    cyberpi.timer.reset()
                if completed and cyberpi.timer.get() >= 2.5:
                    mbot2.EM_stop("ALL")
                    mbot2.servo_set(85,"all")
                    display()
                    cyberpi.stop_all()
           
        except Exception as e:
            cyberpi.console.println(e)

            if isinstance(e, ZeroDivisionError):
                cyberpi.console.println("L" + str(mbuild.ultrasonic2.get(1)))
                time.sleep(0.05)
                cyberpi.console.println("R" + str(mbuild.ultrasonic2.get(3)))
                time.sleep(0.05)
                cyberpi.console.println("F" + str(mbuild.ultrasonic2.get(2)))

def obst():
    mbuild.ai_camera.ai_camera_set_func_switch(3, 1)
   
    angle_history = []
   
    cyberpi.timer.reset()

    dl = 1
    dr = 1
    df = 1
    sublevel = 0
    detecting = False
    completed = False
    
    mbot2.servo_set(85,"all")
    if mbuild.ultrasonic2.get(1) > mbuild.ultrasonic2.get(3):
        #left
        direction = 0
        mbot2.servo_set(45,"all")
    else:
        #right
        direction = 1
        mbot2.servo_set(120,"all")
    mbot2.straight(13)
    if direction == 0:
      mbot2.servo_set(120,"all")
    else:
      mbot2.servo_set(45,"all")
    mbot2.straight(-11)
    if direction == 0:
      mbot2.servo_set(45,"all")
    else:
      mbot2.servo_set(120,"all")
    mbot2.straight(20)
    if direction == 0:
      mbot2.servo_set(120,"all")
    else:
      mbot2.servo_set(45,"all")
    mbot2.straight(13)
    mbot2.servo_set(85,"all")

    cyberpi.led.show('red black black black black')

    time.sleep(5)

    mbot2.forward(spd)

    while True:
    
        #display()
       
        try:
        
            temp = mbuild.ultrasonic2.get(1)
            #if temp != 300:
            dl = temp
            temp = mbuild.ultrasonic2.get(2)
            #if temp != 300:
            df = temp
            temp = mbuild.ultrasonic2.get(3)
            #if temp != 300:
            dr = temp
            time.sleep(0.05)
           
            a = get_angle(dl, dr, df) - 5
           
            x = mbuild.ai_camera.ai_camera_color_spatial_attribute_get(6, 1, 1)
            h = mbuild.ai_camera.ai_camera_color_spatial_attribute_get(6, 4, 1)

            if h >= 0:
                #mbot2.EM_stop()
                #cyberpi.stop_all()
                min_height = 50
                max_height = 225

                if h < min_height:
                    target_x = 160
                elif h > max_height:
                    target_x = 300
                else:
                    target_x = 160 + ((h - min_height) / (max_height - min_height)) * 140

                error = target_x - x
                camera_correction = error * 0.25

            else:
                camera_correction = 0
            if mbuild.ai_camera.ai_camera_color_color_get(6, 1) == 1:
                a = a - camera_correction
            else:
                a = a + camera_correction
            a = max(85 - 90*r, min(85 + 90*l, a))
            a = smooth_angle(a)
            mbot2.servo_set(a, "all")

            #if 0 < df <= 10:
            #    cyberpi.timer.reset()
            #    mbot2.servo_set(-a + 180, "all")
            #    mbot2.backward(spd)
            #    while cyberpi.timer.get() <= 1.5:
            #        if mbuild.quad_rgb_sensor.get_line_sta("all", 1) != 15:
            #           if not detecting:
            #                sublevel -= 1
            #                cyberpi.led.move(-1)
            #                detecting = True
            #        else:
            #            detecting = False
            #        time.sleep(0.02)
            #    mbot2.forward(spd)           

            if mbuild.quad_rgb_sensor.get_line_sta("all", 1) != 15:
                if not detecting:
                    sublevel += 1
                    cyberpi.led.move(1)
                    detecting = True
            else:
                detecting = False

            if sublevel >= 12:
                if not completed:
                    completed = True
                    cyberpi.timer.reset()
                if completed and cyberpi.timer.get() >= 4:
                    mbot2.EM_stop("ALL")
                    mbot2.servo_set(85,"all")
                    display()
                    cyberpi.stop_all()
           
        except Exception as e:
            cyberpi.console.println(e)

            if isinstance(e, ZeroDivisionError):
                cyberpi.console.println("L" + str(mbuild.ultrasonic2.get(1)))
                time.sleep(0.05)
                cyberpi.console.println("R" + str(mbuild.ultrasonic2.get(3)))
                time.sleep(0.05)
                cyberpi.console.println("F" + str(mbuild.ultrasonic2.get(2)))

@event.is_press('a')
def main():
    global spd, log, angle_history

    #time.sleep(3)
    mbot2.EM_stop("ALL")
    mbot2.servo_set(85,"all")
   
    display()
    time.sleep(0.05)
    
    if mbuild.ultrasonic2.get(2) >= 15:
        open()
    else:
        obst()
    
    #open()


display()
