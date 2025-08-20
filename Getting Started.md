# Getting Started with SQARM DRONE

Welcome to the SQARM DRONE project! Follow the steps below to set up your drone, including hardware and software installations, firmware updates, and configuration of your control system.

## 1. Prerequisites

Before getting started, ensure you have the following prerequisites:

### Software:**

- **ROS 2 (Jazzy)**:
  ROS 2 is essential for interfacing with the drone's hardware, managing sensor data, and controlling the flight logic. Make sure you have **ROS 2 Jazzy** installed on your system.
  - Follow the official guide to install **ROS 2 Jazzy**: [ROS 2 Installation Guide](https://docs.ros.org/en/foxy/Installation.html).

- **QGroundControl**:
  QGroundControl is the Ground Control Software used to interface with the drone. It allows for easy configuration, firmware upload, and telemetry.
  - Download and install **QGroundControl** from the official website: [QGroundControl Download](https://qgroundcontrol.com/downloads/).

### Hardware:

- **Pixhawk 4 FMUv2**:
  The **Pixhawk 4** is the primary flight controller for the drone. It is a powerful autopilot system that supports PX4 and ArduPilot firmware.
  
- **Additional Components**:
  - **GPS Module**: UBlox GPS + Compass
  - **ESCs**: 30A OPTO 2-6LiPo/600Hz
  - **Motors**: 880KV Brushless DC Motor
  - **Propellers**: 1045 Propeller Blade
  - **Battery**: 11.1V 5200mAh 3S LiPo Battery
  - **Telemetry**: 433MHz Radio Telemetry
  - **Power Distribution Board**: F450 Frame

### Tools:
- USB cable for Pixhawk connection

## 2. Installing Firmware

### Installing Firmware for Pixhawk 4:
- **ArduPilot Firmware**:
  1. Connect the Pixhawk 4 to your computer via USB.
  2. Open **QGroundControl** and goto vehicle setup -> Firmware
  3. Choose **ArduPilot** as the firmware and following configurations
     1. ChibiOS
     2. Multi-Rotor
     3. fmuv2 - 4.5.7
  4. Follow the on-screen prompts to upload the firmware.
  5. Reboot the device.


> ⚠️ **Notice:**  We are using a unofficial PX4 control board. Therefore official PX4 Pro firmawere had some issues. v1.1.3 onwards it have a CPU load not found error. Therefore use Ardupilot with this hardware. We are tested with v4.5.7 at the time. 

### Firmware Verification:
- Once the firmware is installed, reboot the Pixhawk and check that the correct firmware version is running via the QGroundControl interface.

## 3. Setting up the Control Board

### Connecting the Pixhawk 4:
1. **Connect the Pixhawk 4** to your computer via USB.
2. Use the **QGroundControl** software to communicate with the Pixhawk.
3. **Choose the frame configuration** (Quad-X) in the setup wizard on QGroundControl.


### Setting Up the ESCs and Motors:
1. Ensure that the **ESCs** are correctly connected to the Pixhawk and the motors.
2. Verify that the **motor rotation direction** is correct by manually testing the motors in the QGroundControl software.
<pre>
        ▲ Front
     (D) ⟳  ⟲ (A)
         \   /
          [X]
         /   \
     (C) ⟲  ⟳ (B)
        ▼ Rear
</pre>
## 4. Calibration

### Radio Calibration:
1. Navigate to the **Radio Calibration** section.
2. Move the sticks on your remote control to calibrate the radio.
3. Make sure to use Mode 2.
   
### Sensor Calibration:
1. Calibrate all the sensors.
2. Accelerometer - Rotation : None
3. Compass - Rotation : None
4. Use external compass as priority one. 

### Power Setup
1. Set up battery monitor 1,
   1. Battery Monitor : Analog Voltage and Current
   2. Capacity : ... (5200mAh)
   3. Minimum arming voltage: ... (9v)
   4. Power Sensor: Other
   5. Voltage multipler: 10.1
   6. Amps per volt:17.0 A/V
   7. Amp Offset: 0.0v
2. Then Calibrate the ESC
   
### Safety Setup
1. Setup Battery Failsafe
2. Setup General FailSafe
3. Activate GeoFence while testing
   
### Parameters Configureation
1. Need to enable SR*_** parameters to get data from the PX4 via mavLink
   1. SR0_* → for Telemetry port 1
   2. SR1_* → for Telemetry port 2
   3. SR2_* → for USB (typically)
2. Recomnaded Settings
# Recommended PX4 MAVLink Stream Rates (`SRx_*` Parameters)

| Parameter          | Data Type / Purpose                         | **USB (SR2_*)** | **Telemetry (SR0_*)** |
|-------------------|----------------------------------------------|-----------------|------------------------|
| `SRx_POSITION`     | GPS, global position                        | `10 Hz`         | `2 Hz`                 |
| `SRx_RAW_SENSORS`  | IMU, magnetometer, barometer                | `10 Hz`         | `2 Hz`                 |
| `SRx_RC_CHANNELS`  | RC input channels                           | `10 Hz`         | `2 Hz`                 |
| `SRx_EXT_STATUS`   | EKF, estimator status                       | `2 Hz`          | `1 Hz`                 |
| `SRx_EXTRA1`       | Attitude (quaternion)                       | `20 Hz`         | `5 Hz`                 |
| `SRx_EXTRA2`       | Velocity, heading                           | `10 Hz`         | `2 Hz`                 |
| `SRx_EXTRA3`       | Acceleration, position setpoints, etc.      | `5 Hz`          | `1 Hz`                 |
| `SRx_RAW_CTRL`     | Control inputs (e.g., steering, throttle)   | `10 Hz`         | `5 Hz`                 |
| `SRx_PARAMS`       | System parameters                           | `1 Hz`          | `1 Hz`                 |
| `SRx_ADSB`         | ADS-B traffic (Automatic Dependent Surveillance-Broadcast) | `1 Hz`          | `1 Hz`                 |

> 📝 Replace `SRx_*` with the appropriate stream ID:
> - `SR0_*` = TELEM1 (Telemetry Port 1)
> - `SR1_*` = TELEM2 (Telemetry Port 2, optional)
> - `SR2_*` = USB (MAVSDK / QGC via direct USB)


## 5. Pre-flight Checklist

Before you take off, double-check the following:
- Ensure the **battery is fully charged**.
- Make sure the **motors and propellers** are secure.
- Verify that **all wiring is intact**.
- Perform a **control test** using the remote controller to ensure proper responsiveness.

## 6. First Flight

Once everything is set up and calibrated:
- Place the drone in an open area.
- Perform a **low-altitude hover test** to ensure stability.
- Gradually increase flight time and altitude to familiarize yourself with the controls.



