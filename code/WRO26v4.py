#if divide by zero error: change the sensor/wire
#if it hits a wall, unplug and replug the sensor wire
import event, time, cyberpi, mbot2, mbuild, math


l = 30/90
r = 55/90
spd = 70

ANGLE_AVERAGE_SIZE = 5       #number of previous angles to remember
ANGLE_AVERAGE_SIGMA = 1.625    #larger = flatter/smoother weighting
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
    cyberpi.console.clear()
    cyberpi.console.println("Downforce Robot")
    cyberpi.console.println("L" + str(mbuild.ultrasonic2.get(1)))
    cyberpi.console.println("R" + str(mbuild.ultrasonic2.get(3)))
    cyberpi.console.println("F" + str(mbuild.ultrasonic2.get(2)))
    cyberpi.console.println(str(cyberpi.get_battery()) + "%")


def tsigmoid(x,k):
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
        return 90 - 90*tsigmoid(-q_left, 6.5-(max(min(70,df),10)/(60/5)))
    else:
        return 90 - 90*tsigmoid(q_right, 6.5-(max(min(70,df),10)/(60/5)))


@event.is_press('b')
def stop():
    cyberpi.stop_other()
    mbot2.EM_stop("ALL")
    mbot2.servo_set(90,"all")
    display()
   

@event.is_press('a')
def main():
    global spd, log, angle_history

    #time.sleep(3)
    mbot2.EM_stop("ALL")
    mbot2.servo_set(90,"all")
    mbot2.forward(spd)
    display()

    angle_history = []

    dl = 1
    dr = 1
    df = 1
    sublevel = 0
    detecting = False

    cyberpi.led.show('red black black black black')

    while True:
       
        #display()
       
        try:
            temp = mbuild.ultrasonic2.get(1)
            if temp != 300:
                dl = temp

            temp = mbuild.ultrasonic2.get(2)
            if temp != 300:
                df = temp

            temp = mbuild.ultrasonic2.get(3)
            if temp != 300:
                dr = temp

            a = get_angle(dl, dr, df)
            a = smooth_angle(a)

            mbot2.servo_set(a, "all")

            if not mbuild.quad_rgb_sensor.get_line_sta("all", 1) == 15:
                if not detecting:
                    sublevel += 1
                    cyberpi.led.move(1)
                    detecting == True
            else:
                detecting = False

            if sublevel >= 1000:
                mbot2.EM_stop("ALL")
                mbot2.servo_set(90,"all")
                display()
                cyberpi.stop_all()
           
        except Exception as e:
            cyberpi.console.println(e)

            if isinstance(e, ZeroDivisionError):
                cyberpi.console.println("L" + str(mbuild.ultrasonic2.get(1)))
                cyberpi.console.println("R" + str(mbuild.ultrasonic2.get(3)))
                cyberpi.console.println("F" + str(mbuild.ultrasonic2.get(2)))

        time.sleep(0.02)


display()
