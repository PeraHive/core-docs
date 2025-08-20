import asyncio
import os
import math
from mavsdk import System
from mavsdk.offboard import PositionNedYaw, VelocityNedYaw
from mavsdk.action import ActionError
import glob

async def connect_drone():
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
    return drone

async def arm_drone(drone):
    print("🔍 Checking if drone is ready to arm...")
    async for health in drone.telemetry.health():
        if health.is_armable:
            print("✅ Drone is ready to arm!")
            break
        else:
            print("❌ Drone is not ready to arm. Please check pre-arm conditions.")
            return

    try:
        await drone.action.arm()
        print("🚀 Drone armed!")
    except Exception as e:
        print(f"⚠️ Failed to arm the drone: {str(e)}")

async def goto_location(drone):
    print("\n🌍 Enter target GPS coordinates:")
    try:
        lat = float(input("Latitude (decimal degrees): "))
        lon = float(input("Longitude (decimal degrees): "))
        alt = float(input("Altitude (meters): "))
        
        print(f"\n🚀 Flying to: Lat {lat}, Lon {lon}, Alt {alt}m")
        await drone.action.goto_location(lat, lon, alt, 0)  # 0=yaw angle (north)
        print("✅ Command sent!")
    except ValueError:
        print("⚠️ Invalid input! Please enter numbers only.")
    except ActionError as e:
        print(f"⚠️ Failed to execute command: {str(e)}")

async def move_relative(drone):
    print("\n🧭 Relative movement options:")
    print("1. Forward  2. Backward  3. Left  4. Right  5. Up  6. Down")
    
    try:
        direction = input("Select direction (1-6): ")
        distance = float(input("Distance (meters): "))
        
        if direction not in ["1","2","3","4","5","6"]:
            print("⚠️ Invalid direction!")
            return

        # Get current position in GPS coordinates
        async for position in drone.telemetry.position():
            current_lat = position.latitude_deg
            current_lon = position.longitude_deg
            current_alt = position.absolute_altitude_m
            break

        # Get current heading (yaw)
        async for heading in drone.telemetry.heading():
            current_yaw = heading.heading_deg
            break

        # Convert yaw to radians for calculations
        yaw_rad = math.radians(current_yaw)
        
        # Calculate new position based on direction
        earth_radius = 6378137.0  # meters
        if direction in ["1","2"]:  # Forward/Backward
            delta_lat = (distance * math.cos(yaw_rad)) / earth_radius * (180/math.pi)
            delta_lon = (distance * math.sin(yaw_rad)) / (earth_radius * math.cos(math.radians(current_lat))) * (180/math.pi)
            new_lat = current_lat + (delta_lat if direction == "1" else -delta_lat)
            new_lon = current_lon + (delta_lon if direction == "1" else -delta_lon)
        elif direction in ["3","4"]:  # Left/Right
            # Perpendicular to current heading (90 degrees)
            delta_lat = (distance * math.cos(yaw_rad + math.pi/2)) / earth_radius * (180/math.pi)
            delta_lon = (distance * math.sin(yaw_rad + math.pi/2)) / (earth_radius * math.cos(math.radians(current_lat))) * (180/math.pi)
            new_lat = current_lat + (delta_lat if direction == "4" else -delta_lat)
            new_lon = current_lon + (delta_lon if direction == "4" else -delta_lon)
        else:  # Up/Down
            new_lat = current_lat
            new_lon = current_lon
        
        # Calculate new altitude
        if direction == "5":  # Up
            new_alt = current_alt + distance
        elif direction == "6":  # Down
            new_alt = max(current_alt - distance, 0)  # Don't go below ground
        else:
            new_alt = current_alt

        print(f"\n📍 Current position: Lat {current_lat}, Lon {current_lon}, Alt {current_alt}m")
        print(f"🎯 New position: Lat {new_lat}, Lon {new_lon}, Alt {new_alt}m")
        
        # Execute movement
        await drone.action.goto_location(new_lat, new_lon, new_alt, current_yaw)
        print("✅ Movement command sent!")

    except ValueError:
        print("⚠️ Invalid distance! Please enter a number.")
    except Exception as e:
        print(f"⚠️ Movement failed: {str(e)}")
async def change_mode(drone):
    modes = {
        "1": {"name": "MANUAL", "type": "rc_override", "channel_value": -0.1},
        "2": {"name": "ALTCTL (Altitude Hold)", "type": "rc_override", "channel_value": 0.5},
        "3": {"name": "POSCTL (Position Hold)", "type": "rc_override", "channel_value": 0.9},
        "4": {"name": "AUTO.MISSION", "type": "action", "command": "hold"},
        "5": {"name": "AUTO.LOITER", "type": "action", "command": "hold"},
        "6": {"name": "AUTO.RTL (Return to Launch)", "type": "action", "command": "rtl"},
        "7": {"name": "AUTO.LAND", "type": "action", "command": "land"},
        "8": {"name": "AUTO.TAKEOFF", "type": "action", "command": "takeoff"},
        "9": {"name": "OFFBOARD (External Control)", "type": "offboard"},
    }

    print("📜 Available Modes:")
    for key, mode in modes.items():
        print(f"  {key}. {mode['name']}")

    try:
        selection = input("👉 Enter the number of the mode you want to set: ").strip()
        if selection not in modes:
            print("⚠️ Invalid selection.")
            return

        selected_mode = modes[selection]
        print(f"🔄 Attempting to change flight mode to {selected_mode['name']}...")

        try:
            await drone.manual_control.set_manual_control_input(0, 0, 0, 0)
            await asyncio.sleep(0.2)

            if selected_mode["type"] == "rc_override":
                await drone.manual_control.set_manual_control_input(
                    0, 0, 0, selected_mode["channel_value"]
                )
                print("⚠️ RC override used. Ensure RC channel 5 is configured on the drone.")

            elif selected_mode["type"] == "action":
                if selected_mode["command"] == "takeoff":
                    # await drone.action.arm()
                    await drone.action.takeoff()
                elif selected_mode["command"] == "land":
                    await drone.action.land()
                elif selected_mode["command"] == "rtl":
                    await drone.action.return_to_launch()
                elif selected_mode["command"] == "hold":
                    await drone.action.hold()

            elif selected_mode["type"] == "offboard":
                await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -1.0, 0.0))
                await drone.offboard.start()
                print("🚀 Offboard mode activated.")

            async for mode in drone.telemetry.flight_mode():
                print(f"✅ Current flight mode: {mode}")
                break

        except Exception as e:
            print(f"❌ Failed to change mode: {str(e)}")
            if selection in ["8", "9"]:
                await drone.action.disarm()

    except Exception as e:
        print(f"⚠️ Error: {str(e)}")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

async def control_panel():
    drone = await connect_drone()

    while True:
        clear_console()
        print("╔═════════════════════════════════════════════════════════════════════╗")
        print("║                     🚁 MAVSDK - Control Panel                       ║")
        print("╚═════════════════════════════════════════════════════════════════════╝\n")

        print("📜 Commands:")
        print("  🅰️  Arm the drone      : A")
        print("  🔄 Change mode        : M")
        print("  🌍 Go to GPS location : G")
        print("  🧭 Move relative      : R")
        print("  ❌ Quit the program   : Q")
        print("______________________________________________________________________")
        print()

        user_input = input("👉 Enter your command: ").strip().lower()

        if user_input == "a":
            clear_console()
            await arm_drone(drone)
            input("🔙 Press 'Enter' to return to the main menu.")
        elif user_input == "m":
            clear_console()
            await change_mode(drone)
            input("🔙 Press 'Enter' to return to the main menu.")
        elif user_input == "g":
            clear_console()
            await goto_location(drone)
            input("🔙 Press 'Enter' to return to the main menu.")
        elif user_input == "r":
            clear_console()
            await move_relative(drone)
            input("🔙 Press 'Enter' to return to the main menu.")
        elif user_input == "q":
            clear_console()
            print("👋 Exiting control panel...")
            break
        else:
            clear_console()
            print("⚠️ Invalid command. Please try again.")

if __name__ == "__main__":
    asyncio.run(control_panel())