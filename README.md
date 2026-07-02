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
|Shaayan Nadir|Documentation and Design|
|Ziyad Farrukh|Engineering|
|Syed Taha Ahmed|Coding and Logic|

\---

## Project Overview

Team Downforce is a robotics team from Karachi, Pakistan, competing in the WRO 2026 Future Engineers category. Our challenge is to design, build, and program a fully autonomous self-driving car capable of completing laps on a dynamic racetrack, detecting and responding to traffic signs, and performing parallel parking — all without any human input during the run.

Our vehicle is built on an **MBOT2 chassis** equipped with a high-precision encoder motor for reliable distance and speed control. For visual sensing and AI-based decision making, we use an **AI Smart Camera**, which handles color detection for the red and green traffic sign pillars. Our code is written in **Scratch (block-based programming)** using .mblock files, making our solution accessible, readable, and easy to modify and debug.

\---

## Vehicle Design

### Chassis \& Mechanics

* **Chassis:** YFROBOT (car-type steering chassis)
* **Drive Motor:** Encoder motor — provides precise speed and distance feedback
* **Steering:** Servo-based Ackermann steering system
* **Drive System:** Rear-wheel system with an axel
* **Power Supply:** 3.7 V Lithium (2500 mAh battery capacity)
* **Controller:** Dual core ESP32-S3 processor

### Sensing \& Vision

* **AI Camera:** XTOOL Education AI Camera 2.0 (model: MMA-K001-001) — used for detecting red and green traffic sign pillars
* **Additional Sensors:** Two ultrasonic sensors

### Vehicle Dimensions

* **Length:** 25cm
* **Width:** 20cm
* **Height:** 11.5cm
* **Weight:** 900g

All dimensions are within the WRO 2026 Future Engineers maximum specification of 30×20×30 cm.

\---

## Code Structure \& How It Works

Our code is written entirely in **Makeblock (block-based programming)** and saved as **.mblock files**.



### File Index

|File|Description|
|-|-|
|`S2\_11.4.mblock`|Code completed on the second team session, scheduled on 11/4/26. Covers basic movement around the track using the ultrasonic sensor for wall detection. Started to incorporate the CyberPi's inbuilt gyroscope for more accurate turning|
|`S3\_18.4.mblock`|Code completed on the third team session, scheduled on 18/4/26. Incorporates acceleration and deceleration code blocks to minimize errors on the straight sections|
|`S4\_25.4.mblock`|Code completed on the fourth team session, scheduled on 25/4/26. Uses the CyberPi's gyroscope for turning by turning 90 degrees relative to the previous position for each corner|
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

**Why Block-Based Programming?**
Our team chose Scratch because it allows rapid development and easy debugging of logic flows. The visual block structure makes it straightforward for all team members to understand, modify, and test the code collaboratively. As noted in WRO guidelines, there are no restrictions on programming language — block-based coding is fully accepted.

\---

### Challenges \& Solutions

|Challenge|How We Solved It|
|-|-|
|Our original custom Ackermann steering design was unreliable and had too large of a turn radius to be maneuverable enough to complete the challenges.|Upgrade the chassis for maximum stability and use a new design for the Ackermann steering which allows for more movement capabilities.|
|Bumps in the challenge mat change robots orientation.|Use the CyberPi's inbuilt gyroscope for turning. At every corner, turn 90 degrees relative to current position, and reset yaw angle after every turn|
|Immediately moving at maximum rpm and instantaneously stopping causes the robot to jolt and subsequently skid, which causes an offset in the orientation of the robot. This makes the turns of the robot inaccurate and cause it to collide it with the center wall, usually by the third round|Develop code to accelerate and decelerate on the straights to prevent offsets to the robots orientation.|

\---

## Photos

Photos of the vehicle from all sides, top, and bottom are available in the `/photos/` folder of this repository.

|View|File|
|-|-|
|Front|`/photos/front.jpeg`|
|Rear|`/photos/rear.jpeg`|
|Left Side|`/photos/left.jpeg`|
|Right Side|`/photos/right.jpeg`|
|Top|`/photos/top.jpeg`|
|Bottom|`/photos/bottom.jpeg`|
|Team Photo|`/photos/team.jpeg`|

\---

## Resources \& References

* [WRO 2026 Future Engineers General Rules](https://wro-association.org/wp-content/uploads/WRO-2026-Future-Engineers-Self-Driving-Cars-General-Rules.pdf)
* [WRO Future Engineers Getting Started Guide](https://world-robot-olympiad-association.github.io/future-engineers-gs/)
* [WRO GitHub Template Repository](https://github.com/World-Robot-Olympiad-Association/wro2022-fe-template)

\---

*This repository will remain public for a minimum of 12 months after the competition as required by WRO 2026 rules.*

*World Robot Olympiad® and the WRO logo are trademarks of the World Robot Olympiad Association Ltd.*

