# WRO 2026 Future Engineers — Team Downforce

## Team Information

**Team Name:** Downforce
**Category:** WRO Future Engineers — Self-Driving Car Challenge
**Season:** 2026
**Country:** Pakistan
**City:** Karachi
**Number of Team Members:** 3
**Coach:** Bilal Hassan

### Team Members

|Name|Role|
|-|-|
|Shaayan Nadir|Documentation|
|Ziyad Farrukh|Code and Design|
|Syed Taha Ahmed|Documentation and Design|

\---

## Project Overview

Team Downforce is a robotics team from Karachi, Pakistan, competing in the WRO 2026 Future Engineers category. Our challenge is to design, build, and program a fully autonomous self-driving car capable of completing laps on a dynamic racetrack, detecting and responding to traffic signs, and performing parallel parking — all without any human input during the run.

Our vehicle is built on an **MBOT2 chassis** equipped with a high-precision encoder motor for reliable distance and speed control. For visual sensing and AI-based decision making, we use an **AI Smart Camera**, which handles color detection for the red and green traffic sign pillars. Our code is written in **Python (text-based programming)**.

\---

## Vehicle Design

### Chassis \& Mechanics

* **Chassis:** YFROBOT (car-type steering chassis)
* **Drive Motor:**  180 Optical Encoder Motor for mBot2 — provides precise speed and distance feedback
* **Steering:** Servo-based Ackermann steering system
* **Drive System:** Rear-wheel system with an axel
* **Power Supply:** 3.7 V Lithium (2500 mAh battery capacity) + 6 V external battery pack(4 AA batteries) to power the servo, with a common ground between the two supplies
* **Controller:** mBot2 Shield - Dual core ESP32-S3 processor

\---

### Sensing \& Vision

* **AI Camera:** XTOOL Education AI Camera 2.0 (model: MMA-K001-001) — used for detecting red and green traffic sign pillars
* **Ultrasonic Sensor:** Three Ultrasonic Sensor 2s (Makeblock) - used for detecting robots distance from front, right and left walls
* **Color Sensor:** Quad RGB Sensor (Makeblock) - used for detecting blue lines to track how many rounds the robot has completed
* **Ranging Sensor:** One Ranging Sensor (Makeblock) - used as a connecting bridge to link color sensor to mBot2 Shield

\---

### Vehicle Dimensions

* **Length:** 25cm
* **Width:** 20cm
* **Height:** 11.5cm
* **Weight:** 900g

All dimensions are within the WRO 2026 Future Engineers maximum specification of 30×20×30 cm.

\---

## Code Structure \& How It Works

Our code is written both in **Makeblock (block-based programming)** and **Python (text-based programming)**.



### File Index

|File|Description|
|-|-|
|`S2_11.4.mblock`|Code completed on the second team session, scheduled on 11/4/26. Covers basic movement around the track using the ultrasonic sensor for wall detection. Started to incorporate the CyberPi's inbuilt gyroscope for more accurate turning|
|`S3_18.4.mblock`|Code completed on the third team session, scheduled on 18/4/26. Incorporates acceleration and deceleration code blocks to minimize errors on the straight sections|
|`S4_25.4.mblock`|Code completed on the fourth team session, scheduled on 25/4/26. Uses the CyberPi's gyroscope for turning by turning 90 degrees relative to the previous position for each corner|
|`WRO26v1.py`|First iteration of lane-sensing algorithm. Uses inputs from ultrasonic sensors on the right and left side to decide how much to steer.|
|`WRO26v2.py`|Fine-tuned the lane-sensing algorithm by transforming the sigmoid function to make the robot's movement smoother on the straight sections.|
|`WRO26v3.py`|Started tracking lap progress by counting how many blue lines the color sensor passed over|
|`WRO26v4.py`|Smoothed out anomalous ultrasonic sensor readings using a Gaussian distribution of a moving average|
|`WRO26v5.py`|Uses front ultrasonic sensor to move backwards if robot gets too close to a wall|
|`/photos/`|Photos of the vehicle from all sides, and the team|
|`/screenshots/`|Screenshots of block code for judge reference|

\---

## Engineering Journey

### Design Decisions

**Why Mbot2 Shield?**

The Mbot2 shield comes with an integrated rechargeable power supply and a variety of ports to connect sensors, motors and servos.

**Why not Lego Mindstorms?**

The Makeblock system utilizes structural aluminum and standard M4 screws, which stand up better to the wear and tear of competitive robotics compared to ABS plastic LEGO bricks. Moreover, the built-in DC motors feature encoders that allow for highly exact, millimeter-by-millimeter movement control

**Why YFROBOT Chassis?**
The YFROBOT provides a stable, car-type Ackermann steering base that closely mimics real-world vehicle behavior. Its rigid frame reduces unwanted vibrations and allows consistent turning radii, which is critical for reliable lap completion.

**Why Encoder Motor?**
Encoder feedback allows the robot to track how far it has travelled with precision, allowing for exact movement.

**Why XTOOL Education AI Camera 2.0?**
The XTOOL Education AI Camera 2.0 provides built-in color and object detection, reducing the processing load on the main controller. It outputs clean, actionable signals that integrate well with our block-based code structure.

\---

### Challenges \& Solutions

|Challenge|How We Solved It|
|-|-|
|Our original custom Ackermann steering design was unreliable and had too large of a turn radius to be maneuverable enough to complete the challenges.|Upgrade the chassis for maximum stability and use a new design for the Ackermann steering which allows for more movement capabilities.|
|Bumps in the challenge mat change robots orientation.|Use the CyberPi's inbuilt gyroscope for turning. At every corner, turn 90 degrees relative to current position, and reset yaw angle after every turn|
|Immediately moving at maximum rpm and instantaneously stopping causes the robot to jolt and subsequently skid, which causes an offset in the orientation of the robot. This makes the turns of the robot inaccurate and cause it to collide it with the center wall, usually by the third round|Develop code to accelerate and decelerate on the straights to prevent offsets to the robots orientation.|
|Lane-sensing algorithm was over-correcting, leading to jerky movements|Transform the sigmoid function by cubing the x, making turning smoother|
|Placement of Encoder Motor on YFROBOT Chassis was faulty, causing the gears between the wheel axle and motor to seperate|Tie rubber bands to Encoder Motor and wheel axle to keep them connected. (Refer to `/photos/rubberband.jpeg`|
|The servo controlling the steering system operates at 6 V, but our controller supplies 3.7 V. The operating voltage was insufficient, hence over a period of time the servo circuitry heated up and stopped working. This problem was due to poor power management. |This was rectified by redesigning the power architecture. Under the new architecture the CyberPi and mBot2 Shield provided only the signal that controlled the servo angles. The power of the servo was provided externally using a 6 V battery pack.  The most important consideration in this design was that the ground(negative) connections from the external source, the CyberPi and the servo had to be connected to form a common ground.|
|The delay in the ultrasonic sensors was causing the robot to start turning too late|Initially we tilted the side ultrasonic sensors to face forwards. However when placed at an angle they gave anomalous readings very frequently, making the algorithm unreliable. (Refer to `/photos/robot\\\\\\\_v2/` pictures). In the end, we moved the side ultrasonic sensors to the front of the robot, perpendicular to the front ultrasonic sensor. (Refer to `/photos/robot\\\\\\\_v3/` pictures)|

\---

## Photos

Photos of the vehicle from all sides, top, and bottom are available in the `/photos/` folder of this repository.

|View|File|
|-|-|
|Front of version 1 of the design|`/photos/robot_v1/front.jpeg`|
|Rear of version 1 of the design|`/photos/robot_v1/rear.jpeg`|
|Left side of version 1 of the design|`/photos/robot_v1/left.jpeg`|
|Right side of version 1 of the design|`/photos/robot_v1/right.jpeg`|
|Top of version 1 of the design|`/photos/robot_v1/top.jpeg`|
|Bottom of version 1 of the design|`/photos/robot_v1/bottom.jpeg`|
|Front of version 2 of the design|`/photos/robot_v2/bottom.jpeg`|
|Left side of version 2 of the design|`/photos/robot_v2/left.jpeg`|
|Right side of version 2 of the design|`/photos/robot_v2/right.jpeg`|
|Top of version 2 of the design|`/photos/robot_v2/top.jpeg`|
|Front of version 3 of the design|`/photos/robot_v3/front.jpeg`|
|Rear of version 3 of the design|`/photos/robot_v3/rear.jpeg`|
|Left side of version 3 of the design|`/photos/robot_v3/left.jpeg`|
|Right side of version 3 of the design|`/photos/robot_v3/right.jpeg`|
|Top of version 3 of the design|`/photos/robot_v3/top.jpeg`|
|Bottom of version 3 of the design|`/photos/robot_v3/bottom.jpeg`|
|Zoomed in phots of rubber bands tying the Encoder motor to the wheel axle housing|`/photos/rubberband.jpeg`|
|Team Photo|`/photos/team.jpeg`|

\---

## Resources \& References

* [WRO 2026 Future Engineers General Rules](https://wro-association.org/wp-content/uploads/WRO-2026-Future-Engineers-Self-Driving-Cars-General-Rules.pdf)
* [WRO Future Engineers Getting Started Guide](https://world-robot-olympiad-association.github.io/future-engineers-gs/)
* [WRO GitHub Template Repository](https://github.com/World-Robot-Olympiad-Association/wro2022-fe-template)

\---

*This repository will remain public for a minimum of 12 months after the competition as required by WRO 2026 rules.*

*World Robot Olympiad® and the WRO logo are trademarks of the World Robot Olympiad Association Ltd.*

