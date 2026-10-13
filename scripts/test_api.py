#!/usr/bin/env python3
"""Test igneo.pl API client."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from igneo_api import IgleoClient

# Load environment
env_path = Path(__file__).parent.parent / "envs" / ".env.local"
load_dotenv(env_path)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Device ID z HAR file
DEVICE_ID = "2023873659"

def main():
    print("\n" + "="*60)
    print("🔥 Igneo API Client Test")
    print("="*60)

    client = IgleoClient(USERNAME, PASSWORD, DEVICE_ID)

    # Test login
    print("\n🔐 Logging in...")
    if not client.login():
        print("❌ Login failed!")
        return
    print("✅ Logged in")

    # Get device data
    print("\n📊 Getting device data...")
    data = client.get_device_data()

    if not data:
        print("❌ Failed to get device data")
        return

    print("✅ Device data retrieved:\n")
    print(f"  🌡️  Boiler temp:        {data.boiler_temp}°C")
    print(f"  🌡️  Room temp:          {data.room_temp}°C")
    print(f"  🌡️  CWU temp:           {data.cwu_temp}°C")
    print(f"  🌡️  CWU target temp:    {data.cwu_temp_target}°C")
    print(f"  🔥  Burner status:      {data.burner_status}")
    print(f"  ⛽  Fuel counter:       {data.fuel_counter} kg")
    print(f"  💨  Oxygen level:       {data.oxygen_level}%")
    print(f"  🏢  Device type:        {data.device_type}")
    print(f"  🔄  CO circuits:        {data.co_circuits}")
    print(f"  🚰  CWU circuits:       {data.cwu_circuits}")

    # Test setting parameter
    print("\n⚙️  Testing parameter set...")
    order = client.set_cwu_comfort_temp(50)
    if order:
        print(f"✅ Set CWU temp to 50°C (order #{order})")

        # Check order status
        status = client.check_order_status(order)
        print(f"   Order status: {status}")
    else:
        print("❌ Failed to set parameter")

    print("\n" + "="*60)
    print("✅ Test complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
