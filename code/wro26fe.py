import event, time, cyberpi, mbot2, mbuild, math

l = 40/90
r = 70/90
spd = 100

def tsigmoid(x):
    global l, r
    if x < 0:
        return (2*l / (1 + math.e**(-2*x))) - l
    elif x == 0:
        return 0
    elif x > 0:
        return (2*r / (1 + math.e**(-2*x))) - r

def get_angle():
    q_right = (mbuild.ultrasonic2.get(1) / mbuild.ultrasonic2.get(2)) - 1
    q_left = (mbuild.ultrasonic2.get(2) / mbuild.ultrasonic2.get(1)) - 1
    if q_left > q_right:
        return 90 - 90*tsigmoid(-q_left)
    else:
        return 90 - 90*tsigmoid(q_right)

@event.is_press('b')
def stop():
    cyberpi.stop_other()
    mbot2.EM_stop("ALL")
    mbot2.servo_set(90,"all")
    
@event.is_press('a')
def main():
    global spd
    mbot2.EM_stop("ALL")
    mbot2.servo_set(90,"all")
    mbot2.forward(spd)
    while True:
        cyberpi.display.show_label(mbuild.ultrasonic2.get(1), 18, int(0), int(0), index = 0)
        cyberpi.display.show_label(mbuild.ultrasonic2.get(2), 18, int(0), int(50), index = 0)
        try:
            mbot2.servo_set(get_angle(), "all")
        except Exception as e:
            cyberpi.console.println(e)
        time.sleep(0.3)
