# Hardware Specifications

## 1. System Overview
- **Platform**: Quadcopter (X-configuration)
- **Primary Controller**: Pixhawk 4 (Autopilot Flight Controller)

## 2. Component List

- **Frame**: F450 Plastic X configuration
- **Controller**: Pixhawk 4 FMUv2
  - **Built-in Features**:
    - **Processor**: 32-bit ARM Cortex M7
    - **Accelerometer**: 3-axis (ADIS16488)
    - **Gyroscope**: 3-axis (ADIS16488)
    - **Barometer**: MS5611
    - **Magnetometer**: I2C-based (HMC5883L)
    - **GPS/Compass**: UBlox M8N (optional external GPS)
    - **PWM Outputs**: 8 outputs for motor control
    - **PWM Inputs**: 6 inputs for remote control receivers
    - **Serial Ports**: 5 serial ports for external peripherals (e.g., telemetry, GPS)
    - **Supports**: ArduPilot, PX4, and other open-source autopilot software
    - **Power**: 5V regulated, high-efficiency power supply
    - **OS**: ChibiOS (RTOS)
- **GPS Module**: UBlox GPS + Compass Module
- **Power Distribution Board**: F450 Quad-Copter Frame
- **Landing Gear**: Universal Tall Landing Gear Skids for F450
- **Battery**: 11.1V 5200mAh 60C 3S LiPo Battery
- **Power Regulator**: XT60 5.3V DC BEC Power Module
- **Battery Mount**: Custom 3D Printed Mount
- **ESCs**: RoHS 30A OPTO 2-6LiPo/600Hz
- **Motor**: 880KV DC Brushless Motor
- **Propeller**: 1045 Propeller Blade
- **Telemetry**: 433MHz Radio Telemetry
- **Remote Controller**: FlySky FS-iA6
  
## 3. Physical Specifications
- **Frame Size**: 450mm - 550mm (diagonal motor-to-motor)
- **Dimensions**:
  - Length x Width x Height
- **Weight**:
  - Frame Weight - 310g
  - Max Takeoff Weight (MTOW)
- **Motor Mount Size**: 16mm, 19mm, etc. (depending on motor type)
- **Propeller Size**: 1045
- **Material**: Glass fiber and Polyamide nylon
- **Landing Gear Type**: Fixed

## 4. Performance Specifications
- **Max Speed**:
  - Horizontal speed (m/s or km/h)
  - Vertical speed (m/s or ft/s)
- **Max Flight Time**:
  - 8-12 minutes
- **Max Altitude**:
  - Maximum altitude in meters (AGL or MSL)
- **Max Range**:
  - Effective range for radio control (meters or kilometers)
  - Telemetry range (meters or kilometers)
- **Wind Resistance**:
  - Max wind speed (km/h or mph) the drone can operate in
- **Payload Capacity**:
  - Max payload weight (kg or lbs)

## 5. Electrical Specifications
- **Battery**:
  - Type: LiPo
  - Voltage: 11.1V
  - Capacity: 5200mAh
  - Discharge Rate: 60C
- **ESC (Electronic Speed Controller)**:
  - Rating: 30A
  - Type: Brushless OPTO
- **Motors**:
  - Type: Brushless DC (BLDC)
  - KV Rating: 880KV
- **Power Distribution Board**:
  - Type: XT60, XT90 connectors, etc.
- **Power Regulator**:
  - Voltage Output: 5V

## 6. Communication Specifications
- **Remote Controller**:
  - Model: FlySky FS-iA6
  - Channels: 6 channels
  - Frequency: 2.4GHz
- **Radio Link**:
  - Frequency: 2.4GHz
  - Range: 1-5 km (depending on configuration)

## 7. Sensor Specifications
- **Accelerometer**:
  - Type: 3-axis MEMS
  - Range: ±16g
- **Gyroscope**:
  - Type: 3-axis MEMS
  - Range: ±2000°/sec
- **Barometer**:
  - Type: MS5611
  - Pressure Range: 300-1100hPa
- **Magnetometer**:
  - Type: HMC5883L (I2C)
  - Range: ±1.3 to ±8.1 Gauss
- **GPS**:
  - Model: UBlox M8N
  - Accuracy: < 2.5m (horizontal)

## 8. Software and Firmware
- **Firmware**:
  - ArduPilot, PX4, etc.
  - Supported OS: Linux, Windows (for ground control station)
- **Ground Control Software**:
  - QGroundControl, Mission Planner, etc.
  - Features: Mission planning, real-time flight control, telemetry display

## 9. Safety and Redundancy
- **Fail-safe Mechanisms**:
  - GPS Return-to-Launch (RTL)
  - Auto-land on low battery
  - Parachute release (optional)
- **Battery Backup**:
  - Redundant battery for critical avionics
- **LED Indicators**:
  - RGB LEDs for flight status and errors
  - Flashing LEDs for warnings and low battery alerts

## 10. Environmental Specifications
- **Operating Temperature**:
  - Range: -20°C to 50°C
- **Storage Temperature**:
  - Range: -40°C to 60°C
- **Humidity Resistance**:
  - IP rating (IP65, IP67, etc.) for moisture protection

## 11. Miscellaneous
- **Mounting Options**:
  - Gimbals (for camera stabilization)
  - Camera/FPV mounts
- **Vibration Dampening**:
  - Type: Rubber mounts, gel dampers, etc.
