# Downforce Software Flowcharts

[← Software README](README.md) · [← Main README](../README.md)

These flowcharts explain the Python revisions in the project. **V4 is the final physical robot**; V5 and V6 refer to *software revisions*. V6 covers state-driven navigation and lap counting, while the earlier V5 program documents Open and Obstacle Challenge routines.

GitHub renders these Mermaid flowcharts directly in Markdown, so they stay legible and editable without uploading separate pictures.

## 1. Overall program map — Python V6

```mermaid
flowchart TD
    A([Program begins]) --> B[Initialize straight steering and ultrasonic brightness]
    B --> C{Button input}
    C -->|A| D[Start navigation handler]
    C -->|A| E[Start line counter handler]
    C -->|B| F[Stop motor / center servo / reset yaw and count]
    C -->|Up| G[Display ultrasonic readings]
    D --> H[Determine track direction: state_1]
    H --> I[Yaw-guided corner: state_2_alt]
    I --> J{Line count >= 12?}
    J -->|No| K[Wall-following: state_3]
    K --> I
    J -->|Yes| L[Set blue LEDs and command straight movement]
    L --> M([Navigation handler returns])
    E --> N[Count ground-mark transitions until 12]
    N --> O([Line counter ends])
```

**Program behavior:** V6 registers separate Button A handlers for navigation and lap counting. Its final navigation branch commands `mbot2.straight(50)` and returns. The source includes an indentation error in `line()`; the flowchart represents the control steps expressed by the code.

## 2. Direction selection — V6 `state_1()`

```mermaid
flowchart TD
    A([Enter state_1]) --> B[Center servo, move forward at 30]
    B --> C{Left or right ultrasonic > 120?}
    C -->|No| C
    C -->|Yes| D{Left reading > 120?}
    D -->|Yes| E[dir = -1; main = left; opposite = right]
    D -->|No| F[dir = +1; main = right; opposite = left]
    E --> G[Stop motor; pause 1 second]
    F --> G
    G --> H[Drive forward at 50]
    H --> I{Front distance < 50?}
    I -->|No| I
    I -->|Yes| J([Exit state_1])
```

This is the direction-selection logic and threshold values **as written in V6**. Port mapping in this revision is left=3, front=2, right=1, unlike earlier revisions.

## 3. Corner navigation and wall following — V6

```mermaid
flowchart TD
    A([Start state_2_alt]) --> B[Reset yaw; steer 90 + 30*dir; drive at 50]
    B --> C{Yaw reached direction-dependent 60-degree condition?}
    C -->|No| C
    C -->|Yes| D[Stop motor; center servo; resume driving]
    D --> E([Start state_3])
    E --> F{Front distance >= 50?}
    F -->|No| K[Center steering; exit wall-following]
    F -->|Yes| G[Read opposite-side wall distance]
    G --> H{Distance band}
    H -->|Below 22.5| I1[Steering = 90 + 10*dir]
    H -->|22.5 to below 25| I2[Steering = 90 + 5*dir]
    H -->|25 to below 27.5| I3[Steering = 90]
    H -->|27.5 to below 30| I4[Steering = 90 - 5*dir]
    H -->|30 or above| I5[Steering = 90 - 10*dir]
    I1 --> J[Set servo; pause 0.05 s]
    I2 --> J
    I3 --> J
    I4 --> J
    I5 --> J
    J --> F
```

The turn stops when the yaw condition in the `while` statement becomes false. The yaw condition controls when this software turn phase ends. The bands are ultrasonic reading thresholds from the source.

## 4. Blue-marking line counter — V6 `line()`

```mermaid
flowchart TD
    A([Button A line handler]) --> B[Reset sublevel to 0]
    B --> C{sublevel < 12?}
    C -->|No| Z([Counting complete])
    C -->|Yes| D{RGB line status == 0?}
    D -->|No| D
    D -->|Yes| E{RGB line status != 0?}
    E -->|No| E
    E -->|Yes| F[Increment sublevel by 1]
    F --> G[Attempt to display counter]
    G --> C
```

The two wait phases detect entering and leaving a marking, preventing repeated counts while continuously seeing the same status. The wait loops contain no timeout. The display statements in V6 have an indentation error; the chart shows the line-crossing algorithm.

## 5. Historical Open Challenge — Python V5 `open()`

```mermaid
flowchart TD
    A([Start historical open routine]) --> B[Initialize steering, history, timer, lap counter]
    B --> C[Read left, front, right ultrasonic]
    C --> D[Calculate wall-based steering correction]
    D --> E[Smooth steering command]
    E --> F{Front distance between 0 and 10?}
    F -->|Yes| G[Reverse with counter-steering for up to 1.5 s]
    F -->|No| H[Apply steering]
    G --> H
    H --> I[Check RGB line transition and update lap count]
    I --> J{Count >= 12?}
    J -->|No| C
    J -->|Yes| K[Start/inspect finish timer]
    K --> L{Elapsed >= 2.5 seconds?}
    L -->|No| C
    L -->|Yes| M[Stop motor, set steering, stop program]
```

This is the **Python V5** stopping algorithm, which uses a 2.5-second finishing interval.

## 6. Historical Obstacle Challenge — Python V5 `obst()`

```mermaid
flowchart TD
    A([Start historical obstacle routine]) --> B[Enable AI camera mode]
    B --> C[Initialize and execute hard-coded starting maneuver]
    C --> D[Drive and read three ultrasonic sensors]
    D --> E[Compute wall-following steering]
    E --> F[Read camera object x coordinate and apparent height]
    F --> G{Object height >= 0?}
    G -->|No| H[Camera correction = 0]
    G -->|Yes| I[Compute target x from object height]
    I --> J[Camera correction = 0.25 times target-x error]
    H --> K{Camera-reported color}
    J --> K
    K -->|Color code 1| L[Subtract camera correction]
    K -->|Other color| M[Add camera correction]
    L --> N[Clamp steering and smooth command]
    M --> N
    N --> O[Set steering; update line count and finish logic]
    O --> D
```

This flowchart summarizes the Python V5 detection-and-steering loop. The V6 program uses a different state-driven navigation structure and has no equivalent Smart Camera obstacle routine.

## 7. Mathematical steering in the V6 source

```mermaid
flowchart TD
    A([Left distance dl, right distance dr]) --> B{Both nonzero?}
    B -->|No| X[Division may fail: no guard shown in V6]
    B -->|Yes| C[Compute signed distance ratio Q]
    C --> D[Subtract sign of Q]
    D --> E[Apply nonlinear tanh transform using p=2 and k=1]
    E --> F[Scale by ang_range=40; offset by str_ang=90]
    F --> G([Calculated servo command])
```

The zero-reading guard is shown as a **potential error**, not an implemented recovery mechanism. The V6 `calc_angle()` function is called by `state_3_alt()`, which is defined but **not called from its Button A main navigation loop**. The active V6 `state_3()` instead uses fixed distance bands.

---

### How to maintain these diagrams

If your partner changes the robot's software, update the relevant Mermaid blocks from the new verified source. These flowcharts are text-based: on GitHub, select **Edit file** and change the nodes or arrows in `code/flowcharts.md`. Do not relabel a historical algorithm as final V4 behavior without confirming that the actual current program uses it.
