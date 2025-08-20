from mavsdk import System
import asyncio

async def run():
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyACM1:57600")

    async for rc_status in drone.telemetry.rc_status():
        print(f"RC Signal RSSI: {rc_status.signal_strength_percent}%")

asyncio.run(run())
