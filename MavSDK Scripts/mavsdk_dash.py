import asyncio
import glob
from mavsdk import System
import os
from datetime import datetime

telemetry_data = {
    "lat": "N/A", "lon": "N/A", "alt": "N/A", "abs_alt": "N/A",
    "speed": "N/A", "roll": "N/A", "pitch": "N/A", "yaw": "N/A",
    "voltage": "N/A", "battery": "N/A",
    "gps_fix": "N/A", "satellites": "N/A",
    "flight_mode": "N/A", "armed": "N/A",
    "rc_signal": "N/A",
    "health": {
        "Accelerometer calibration": "N/A",
        "Armable": "N/A",
        "Global position": "N/A",
        "Gyrometer calibration": "N/A",
        "Home position": "N/A",
        "Local position": "N/A",
        "Magnetometer calibration": "N/A"
    },
}

short_labels = {
    "Accelerometer calibration": "Acc",
    "Gyrometer calibration": "Gyro",
    "Magnetometer calibration": "Mag",
    "Global position": "GPos",
    "Home position": "Home",
    "Local position": "LPos",
    "Armable": "Arm"
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
        print("🚁 Searching for available ports...")
        available_ports = glob.glob("/dev/ttyACM*") + glob.glob("/dev/ttyUSB*")

        if not available_ports:
            print("⚠️ No available ports found. Please connect the drone and try again.")
            return

        print("📜 Available ports:")
        for i, port in enumerate(available_ports, start=1):
            print(f"  {i}. {port}")

        try:
            selection = int(input("👉 Select the port number to connect to: ").strip())
            if selection < 1 or selection > len(available_ports):
                print("⚠️ Invalid selection. Please try again.")
                return

            selected_port = available_ports[selection - 1]
            print(f"🚁 Connecting to drone on {selected_port}...")
            await drone.connect(system_address=f"serial://{selected_port}:57600")
        except ValueError:
            print("⚠️ Invalid input. Please enter a number.")
            return

        print("⏳ Waiting for drone to connect...")
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
            asyncio.create_task(display_loop())
        ]
        
        await asyncio.gather(*tasks)
        
    except Exception as e:
        add_error(f"Main connection error: {str(e)}")
        await asyncio.sleep(5)  # Wait before retrying
        await run()  # Attempt to reconnect

async def display_loop():
    while True:
        try:
            os.system("clear")  # Use 'cls' on Windows

            # Main Title
            print("╔═════════════════════════════════════════════════════════════════════╗")
            print("║               🚁 MAVSDK - Compact Telemetry Panel                   ║")
            print("╚═════════════════════════════════════════════════════════════════════╝\n")
            # Section 1: GPS / Position and Attitude
            print("🛰️  GPS / Position                                 🎛️  Orientation")
            print("──────────────────────────────────────────────    ─────────────────────")
            print(f"  Fix     : {telemetry_data['gps_fix']:<10}    Sats    : {telemetry_data['satellites']:<10}         Roll  : {telemetry_data['roll']}°")
            print(f"  Lat     : {telemetry_data['lat']:<10}    Lon     : {telemetry_data['lon']:<10}         Pitch : {telemetry_data['pitch']}°")
            print(f"  Rel Alt : {telemetry_data['alt']:<10}    Abs Alt : {telemetry_data['abs_alt']:<10}         Yaw   : {telemetry_data['yaw']}°\n")
    

            # Section 2: Battery / RC and Flight
            print("🔋 Battery / RC                                    ✈️  Flight")
            print("─────────────────────                             ─────────────────────")
            
            print(f"  Voltage : {telemetry_data['voltage'] + 'V':<11}                             Mode  : {telemetry_data['flight_mode']}")
            print(f"  Battery : {telemetry_data['battery'] + '%':<11}                             Armed : {'🟢' if telemetry_data['armed'] == 'Yes' else '🔴'} {telemetry_data['armed']}")         
            print(f"  RC Sig  : {telemetry_data['rc_signal'] + '%':<11}\n")

            # Section 3: Health
            print("\n🧪 Health Check")
            print("───────────────────────────────────────────────────────────────────────")
            print("  ".join(
                f"{short_labels.get(key, key[:4])}: {'✅' if status == 'OK' else '❌'}"
                for key, status in telemetry_data["health"].items()
            ))
            # Section 4: Errors
            if error_list:
                print("\n")
                print("⚠️  Errors")
                print("───────────────────────────────────────────────────────────────────────")
                for err in error_list[-MAX_ERRORS_DISPLAYED:]:
                    print(f"  • {err}")
            print("\n")
            print("═══════════════════════════════════════════════════════════════════════\n")

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
                    "Accelerometer calibration": "OK" if health.is_accelerometer_calibration_ok else "FAIL",
                    "Gyrometer calibration"   : "OK" if health.is_gyrometer_calibration_ok else "FAIL",
                    "Magnetometer calibration": "OK" if health.is_magnetometer_calibration_ok else "FAIL",
                    "Global position"         : "OK" if health.is_global_position_ok else "FAIL",
                    "Home position"           : "OK" if health.is_home_position_ok else "FAIL",
                    "Local position"          : "OK" if health.is_local_position_ok else "FAIL",
                    "Armable"                 : "OK" if health.is_armable else "FAIL"
                }
        except Exception as e:
            add_error(f"Health check fetch error: {str(e)}")
            await asyncio.sleep(1)
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        add_error(f"Fatal error in main: {str(e)}")