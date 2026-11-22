import math
import time
import cyberpi
import event
import mbot2
import mbuild

LEFT_SENSOR = 3
FRONT_SENSOR = 2
RIGHT_SENSOR = 1
DETECTION_DISTANCE = 120
FRONT_STOP_DISTANCE = 50

spd = 50
oppsensor = 0
mainsensor = 0
dir = 0
sublevel = 0

k = 1
p = 2
str_ang = 90
ang_range = 40

def sgn(x):
    if x == 0:
        return 0
    return math.fabs(x) / x

def calc_angle(dl, dr):
    Q = max(dl / dr, dr / dl) * sgn(dl - dr)
    Q -= sgn(Q)
    R = math.tanh((Q**p * sgn(Q)) / k)
    R = str_ang + ang_range * R
    return R

def state_1():
    global oppsensor, mainsensor, dir

    mbot2.servo_set(str_ang, "all")
    mbot2.forward(30)
    
    cyberpi.led.off("all")

    while not (
        mbuild.ultrasonic2.get(LEFT_SENSOR) > DETECTION_DISTANCE
        or mbuild.ultrasonic2.get(RIGHT_SENSOR) > DETECTION_DISTANCE
    ):
        time.sleep(0.01)

    if mbuild.ultrasonic2.get(LEFT_SENSOR) > DETECTION_DISTANCE:
        oppsensor = RIGHT_SENSOR
        mainsensor = LEFT_SENSOR
        dir = -1
        cyberpi.led.show("red red black black black")
    else:
        oppsensor = LEFT_SENSOR
        mainsensor = RIGHT_SENSOR
        dir = 1
        cyberpi.led.show("black black black red red")

    mbot2.EM_stop("ALL")
    time.sleep(1)
    mbot2.forward(50)

    while mbuild.ultrasonic2.get(FRONT_SENSOR) >= FRONT_STOP_DISTANCE:
        time.sleep(0.01)


def state_2():
    mbot2.servo_set(str_ang + 30 * dir, "all")
    cyberpi.led.on(255, 255, 0, "all")
    mbot2.forward(50, 1.8)
    mbot2.servo_set(str_ang, "all")
    mbot2.forward(spd)

def state_2_alt():
    cyberpi.reset_yaw()
    mbot2.servo_set(str_ang + 30 * dir, "all")
    cyberpi.led.on(255, 255, 0, "all")
    mbot2.forward(50)
    while (cyberpi.get_yaw() > -60 and dir == 1) or (cyberpi.get_yaw() < 60 and dir == -1):
        pass # cyberpi.display.show_label(cyberpi.get_yaw(), 24, "center", index= 0)
    mbot2.EM_stop("ALL")
    mbot2.servo_set(str_ang, "all")
    mbot2.forward(spd)

def state_3():
    mbot2.forward(spd)
    
    cyberpi.led.on(0, 255, 0, "all")

    while mbuild.ultrasonic2.get(FRONT_SENSOR) >= FRONT_STOP_DISTANCE:
        distance = mbuild.ultrasonic2.get(oppsensor)
        
        angle = str_ang

        if distance < 22.5:
            angle += 10 * dir
        elif distance < 25:
            angle += 5 * dir
        elif distance < 27.5:
            pass
        elif distance < 30:
            angle -= 5 * dir
        else:
            angle -= 10 * dir

        mbot2.servo_set(angle, "all")
        time.sleep(0.05)

    mbot2.servo_set(str_ang, "all")

def state_3_alt():
    mbot2.forward(spd)
    
    cyberpi.led.on(0, 255, 0, "all")
    
    while mbuild.ultrasonic2.get(mainsensor) >= DETECTION_DISTANCE:
        dl = mbuild.ultrasonic2.get(3)
        dr = mbuild.ultrasonic2.get(1)
        
        a = calc_angle(dl, dr)

        mbot2.servo_set(a, "all")
        time.sleep(0.05)

    mbot2.servo_set(str_ang, "all")


def sens_init():
    while True:
        cyberpi.display.show_label(mbuild.ultrasonic2.get(LEFT_SENSOR), 24, "mid_right", index=0)
        time.sleep(0.05)
        cyberpi.display.show_label(mbuild.ultrasonic2.get(FRONT_SENSOR), 24, "top_mid", index=1)
        time.sleep(0.05)
        cyberpi.display.show_label(mbuild.ultrasonic2.get(RIGHT_SENSOR), 24, "mid_left", index=2)
        time.sleep(0.05)


@event.start
def on_start():
    mbot2.servo_set(str_ang, "all")
    mbuild.ultrasonic2.set_bri(100, 'all', 1)
    mbuild.ultrasonic2.set_bri(100, 'all', 2)
    mbuild.ultrasonic2.set_bri(100, 'all', 3)


@event.is_press("a")
def on_button_a():
    
    state_1()
    while True:
        state_2_alt()
        if sublevel >= 12:
            cyberpi.led.on(0, 0, 255, "all")
            mbot2.straight(50)
            return 0
        state_3()

@event.is_press("a")
def line():
    global sublevel
    
    sublevel = 0
    
    while sublevel < 12:
        while mbuild.quad_rgb_sensor.get_line_sta('all', 1) != 0:
            pass
        while mbuild.quad_rgb_sensor.get_line_sta('all', 1) == 0:
            pass
        sublevel += 1
        
cyberpi.console.clear()
        cyberpi.console.println(sublevel)



@event.is_press("b")
def on_button_b():
    global sublevel
    cyberpi.stop_other()
    mbot2.EM_stop("ALL")
    mbot2.servo_set(str_ang, "all")
    cyberpi.reset_yaw()
    sublevel = 0
    mbuild.ultrasonic2.set_bri(100, 'all', 1)
    mbuild.ultrasonic2.set_bri(100, 'all', 2)
    mbuild.ultrasonic2.set_bri(100, 'all', 3)
    


@event.is_press("up")
def on_joystick_up():
    sens_init() 
