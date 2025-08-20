import asyncio
from mavsdk import System
import os
from datetime import datetime
import csv
import time

telemetry_data = {
    "lat": "N/A",
    "lon": "N/A",
    "alt": "N/A",
    "abs_alt": "N/A",
    "speed": "N/A",
    "roll": "N/A",
    "pitch": "N/A",
    "yaw": "N/A",
    "voltage": "N/A",
    "battery": "N/A",
    "gps_fix": "N/A",
    "satellites": "N/A",
    "flight_mode": "N/A",
    "armed": "N/A",
    "rc_signal": "N/A",
    "health": {
        "Accelerometer calibration": "N/A",
        "Armable": "N/A",
        "Global position": "N/A",
        "Gyrometer calibration": "N/A",
        "Home position": "N/A",
        "Local position": "N/A",
        "Magnetometer calibration": "N/A",
    },
}

# Error tracking system
error_list = []
MAX_ERRORS_DISPLAYED = 5


def add_error(error_msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    error_list.append(f"[{timestamp}] {error_msg}")
    # Keep only the most recent errors
    if len(error_list) > MAX_ERRORS_DISPLAYED:
        error_list.pop(0)


async def run():
    try:
        drone = System()
        # drone = System(mavsdk_server_address="localhost", port=50051)
        await drone.connect(system_address="serial:///dev/ttyUSB0:57600")
        # await drone.connect(system_address="serial://COM11:57600")
        print("Connecting to drone...")

        async for state in drone.core.connection_state():
            if state.is_connected:
                print("✅ Drone connected!")
                break

        # Launch all telemetry fetchers
        tasks = [
            asyncio.create_task(fetch_position(drone)),
            asyncio.create_task(fetch_attitude(drone)),
            asyncio.create_task(fetch_battery(drone)),
            asyncio.create_task(fetch_gps(drone)),
            asyncio.create_task(fetch_flight_mode(drone)),
            asyncio.create_task(fetch_armed_status(drone)),
            asyncio.create_task(fetch_rc_signal(drone)),
            asyncio.create_task(fetch_health(drone)),
            asyncio.create_task(display_loop()),
            asyncio.create_task(log_to_csv()),
        ]

        await asyncio.gather(*tasks)

    except Exception as e:
        add_error(f"Main connection error: {str(e)}")
        await asyncio.sleep(5)  # Wait before retrying
        await run()  # Attempt to reconnect


# # Store the log file name at script start
log_start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = os.path.join("flight_logs", f"telemetry_log_{log_start_time}.csv")
os.makedirs("flight_logs", exist_ok=True)


async def log_to_csv():
    header = [
        "timestamp",
        "lat",
        "lon",
        "alt",
        "abs_alt",
        "speed",
        "roll",
        "pitch",
        "yaw",
        "voltage",
        "battery",
        "gps_fix",
        "satellites",
        "flight_mode",
        "armed",
        "rc_signal",
        "health_accelerometer_calibration",
        "health_armable",
        "health_global_position",
        "health_gyrometer_calibration",
        "health_home_position",
        "health_local_position",
        "health_magnetometer_calibration",
    ]

    while True:
        # Flatten the health dictionary into the main data
        flat_data = telemetry_data.copy()
        health_data = flat_data.pop("health", {})

        # Add timestamp
        flat_data["timestamp"] = datetime.now().isoformat()

        # Flatten health data by adding it to the main dictionary with prefixed keys
        for key, value in health_data.items():
            flat_data[f'health_{key.lower().replace(" ", "_")}'] = value

        # Replace 'N/A' values with 0
        for k, v in flat_data.items():
            if v == "N/A":
                flat_data[k] = 0

        # Write to CSV
        try:
            # Check if file exists to determine if we need to write headers
            file_exists = False
            try:
                with open(filename, "r") as f:
                    file_exists = True
            except FileNotFoundError:
                pass

            with open(filename, "a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=header)

                if not file_exists:
                    writer.writeheader()

                # Write the data row, only including fields that are in our header
                row_data = {
                    k: flat_data.get(k, 0) if flat_data.get(k, 0) != "N/A" else 0
                    for k in header
                }
                writer.writerow(row_data)
        except Exception as e:
            print(f"Error writing to CSV: {e}")
        await asyncio.sleep(1)


async def display_loop():
    while True:
        try:
            os.system("clear")  # Use 'cls' on Windows
            print("========= PX4 MAVSDK Telemetry =========")
            print(f"GPS Fix        : {telemetry_data['gps_fix']}")
            print(f"Satellites     : {telemetry_data['satellites']}")
            print(f"Latitude       : {telemetry_data['lat']}")
            print(f"Longitude      : {telemetry_data['lon']}")
            print(f"Rel Alt (m)    : {telemetry_data['alt']}")
            print(f"Abs Alt (m)    : {telemetry_data['abs_alt']}")
            print(f"Roll           : {telemetry_data['roll']}°")
            print(f"Pitch          : {telemetry_data['pitch']}°")
            print(f"Yaw            : {telemetry_data['yaw']}°")
            print(f"Voltage        : {telemetry_data['voltage']} V")
            print(f"Battery        : {telemetry_data['battery']} %")
            print(f"Flight Mode    : {telemetry_data['flight_mode']}")
            print(f"Armed          : {telemetry_data['armed']}")
            print(f"RC Signal      : {telemetry_data['rc_signal']}")

            print("\n---------- Pre-Arm Health Check ---------")
            for key, value in telemetry_data["health"].items():
                print(f"{key:<30}: {value}")

            # Display errors
            print("\n=========== Recent Errors ===========")
            if error_list:
                for error in error_list[
                    -MAX_ERRORS_DISPLAYED:
                ]:  # Show only the most recent errors
                    print(error)
            else:
                print("No errors recorded")
            print("=====================================\n")

            await asyncio.sleep(1)
        except Exception as e:
            add_error(f"Display loop error: {str(e)}")
            await asyncio.sleep(1)


async def fetch_position(drone):
    while True:
        try:
            async for pos in drone.telemetry.position():
                telemetry_data["lat"] = f"{pos.latitude_deg:.6f}"
                telemetry_data["lon"] = f"{pos.longitude_deg:.6f}"
                telemetry_data["alt"] = f"{pos.relative_altitude_m:.2f}"
                telemetry_data["abs_alt"] = f"{pos.absolute_altitude_m:.2f}"
        except Exception as e:
            add_error(f"Position fetch error: {str(e)}")
            await asyncio.sleep(1)


async def fetch_attitude(drone):
    while True:
        try:
            async for att in drone.telemetry.attitude_euler():
                telemetry_data["roll"] = f"{att.roll_deg:.2f}"
                telemetry_data["pitch"] = f"{att.pitch_deg:.2f}"
                telemetry_data["yaw"] = f"{att.yaw_deg:.2f}"
        except Exception as e:
            add_error(f"Attitude fetch error: {str(e)}")
            await asyncio.sleep(1)


async def fetch_battery(drone):
    while True:
        try:
            async for batt in drone.telemetry.battery():
                telemetry_data["voltage"] = f"{batt.voltage_v:.2f}"
                telemetry_data["battery"] = f"{batt.remaining_percent * 1:.1f}"
        except Exception as e:
            add_error(f"Battery fetch error: {str(e)}")
            await asyncio.sleep(1)


async def fetch_gps(drone):
    while True:
        try:
            async for gps in drone.telemetry.gps_info():
                telemetry_data["gps_fix"] = str(gps.fix_type).replace("FIX_TYPE_", "")
                telemetry_data["satellites"] = f"{gps.num_satellites}"
        except Exception as e:
            add_error(f"GPS fetch error: {str(e)}")
            await asyncio.sleep(1)


async def fetch_flight_mode(drone):
    while True:
        try:
            async for mode in drone.telemetry.flight_mode():
                telemetry_data["flight_mode"] = str(mode).replace("FLIGHT_MODE_", "")
        except Exception as e:
            add_error(f"Flight mode fetch error: {str(e)}")
            await asyncio.sleep(1)


async def fetch_armed_status(drone):
    while True:
        try:
            async for armed in drone.telemetry.armed():
                telemetry_data["armed"] = "Yes" if armed else "No"
        except Exception as e:
            add_error(f"Armed status fetch error: {str(e)}")
            await asyncio.sleep(1)


async def fetch_rc_signal(drone):
    while True:
        try:
            async for rc in drone.telemetry.rc_status():
                try:
                    telemetry_data["rc_signal"] = f"{rc.signal_strength_percent:.1f}"
                except:
                    telemetry_data["rc_signal"] = "N/A"
        except Exception as e:
            add_error(f"RC signal fetch error: {str(e)}")
            await asyncio.sleep(1)


async def fetch_health(drone):
    while True:
        try:
            async for health in drone.telemetry.health():
                telemetry_data["health"] = {
                    "Accelerometer calibration": (
                        "OK" if health.is_accelerometer_calibration_ok else "FAIL"
                    ),
                    "Gyrometer calibration": (
                        "OK" if health.is_gyrometer_calibration_ok else "FAIL"
                    ),
                    "Magnetometer calibration": (
                        "OK" if health.is_magnetometer_calibration_ok else "FAIL"
                    ),
                    "Global position": "OK" if health.is_global_position_ok else "FAIL",
                    "Home position": "OK" if health.is_home_position_ok else "FAIL",
                    "Local position": "OK" if health.is_local_position_ok else "FAIL",
                    "Armable": "OK" if health.is_armable else "FAIL",
                }
        except Exception as e:
            add_error(f"Health check fetch error: {str(e)}")
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        add_error(f"Fatal error in main: {str(e)}")
