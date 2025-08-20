# PeraHive - Drone Project

## Overview
This repository contains the design, hardware specifications, and software for our **drone project**. It includes the necessary files and steps to build and operate a functional drone with key components integrated for various applications.

---

## Hardware Specifications

For detailed hardware specifications, including dimensions, performance, and component list, refer to the [Hardware Specifications](./Hardware%20Specifications.md) document.

- **Platform**: Quadcopter (X-configuration)
- **Primary Controller**: Pixhawk 4 (Autopilot Flight Controller)
- **Frame**: F450 Plastic X configuration
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


## Getting Started

For detailed instructions on setting up your drone, including assembly, firmware installation, and calibration, refer to the [Getting Started](./Getting%20Started.md) guide.


## Parameters and Configuration

### Betaflight Configuration
- **PID Settings:**
  - P: 50
  - I: 40
  - D: 30
- **Flight Modes:**
  - Stabilized Mode
  - Acro Mode
  - GPS Hold Mode

### Calibration
- **ESC Calibration:** Run ESC calibration via Betaflight configurator to ensure proper motor speed response.
- **Compass Calibration:** Ensure the drone’s orientation is accurate using the onboard magnetometer.

---

## Troubleshooting

### Common Issues:
1. **Drone won’t power on:**
   - Check connections from the battery to the ESC and flight controller.
   - Ensure the battery is charged.

2. **Motor not spinning:**
   - Recalibrate the ESC.
   - Verify motor wiring and connections.

3. **No GPS lock:**
   - Ensure the GPS module is correctly wired and has a clear view of the sky.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

Feel free to fork this repository and submit pull requests. Please follow the contributing guidelines outlined in the [CONTRIBUTING.md](CONTRIBUTING.md).

---

