#!/usr/bin/env python3
"""
RS485 Traffic Logger for Estyma Igneo Slim Boiler
Captures and analyzes Modbus RTU communication
"""

import serial
import sys
import time
from datetime import datetime
from pathlib import Path

def calculate_crc(data):
    """Calculate Modbus RTU CRC16."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc.to_bytes(2, byteorder='little')

def format_frame(data):
    """Format and analyze Modbus frame."""
    hex_str = ' '.join(f'{b:02X}' for b in data)

    if len(data) < 4:
        return f"[SHORT] {hex_str}"

    slave_id = data[0]
    func_code = data[1]

    func_names = {
        0x03: "Read Holding Registers",
        0x04: "Read Input Registers",
        0x10: "Write Multiple Registers",
        0x06: "Write Single Register",
    }

    func_name = func_names.get(func_code, f"Unknown (0x{func_code:02X})")

    return f"[Slave {slave_id:02X}] {func_name:30} {hex_str}"

def main():
    """Main logging loop."""
    if len(sys.argv) < 2:
        print("Usage: python3 rs485_logger.py /dev/ttyUSB0 [baudrate] [output_file]")
        print()
        print("Examples:")
        print("  python3 rs485_logger.py /dev/ttyUSB0")
        print("  python3 rs485_logger.py /dev/ttyUSB0 19200")
        print("  python3 rs485_logger.py /dev/ttyUSB0 19200 log.txt")
        sys.exit(1)

    port = sys.argv[1]
    baudrate = int(sys.argv[2]) if len(sys.argv) > 2 else 19200
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    print(f"🔌 RS485 Logger for Estyma Igneo Slim")
    print(f"{'='*60}")
    print(f"Port:      {port}")
    print(f"Baud rate: {baudrate}")
    print(f"Data bits: 8")
    print(f"Parity:    Even (E)")
    print(f"Stop bits: 1")

    if output_file:
        print(f"Output:    {output_file}")

    print(f"{'='*60}")
    print("Starting capture... (Ctrl+C to stop)\n")

    try:
        # Open serial connection
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=8,
            parity=serial.PARITY_EVEN,
            stopbits=1,
            timeout=1
        )

        out_file = open(output_file, 'w') if output_file else None

        frame_buffer = bytearray()
        last_activity = time.time()

        while True:
            if ser.in_waiting > 0:
                byte = ser.read(1)
                frame_buffer.extend(byte)
                last_activity = time.time()

                # Simple frame detection: look for valid Modbus frame
                if len(frame_buffer) >= 8:
                    # Try to parse as Modbus frame
                    if len(frame_buffer) >= 8:
                        data = frame_buffer[:8]
                        crc = calculate_crc(data[:-2])

                        if data[-2:] == crc:
                            # Valid frame found
                            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                            message = f"[{timestamp}] {format_frame(data)}"
                            print(message)

                            if out_file:
                                out_file.write(message + "\n")
                                out_file.flush()

                            frame_buffer = frame_buffer[8:]
            else:
                # No data, check for timeout
                if time.time() - last_activity > 2 and len(frame_buffer) > 0:
                    # Timeout, incomplete frame
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    hex_str = ' '.join(f'{b:02X}' for b in frame_buffer)
                    message = f"[{timestamp}] [INCOMPLETE] {hex_str}"
                    print(message)

                    if out_file:
                        out_file.write(message + "\n")
                        out_file.flush()

                    frame_buffer = bytearray()
                    last_activity = time.time()

                time.sleep(0.01)

    except serial.SerialException as e:
        print(f"\n❌ Serial error: {e}")
        print(f"\nCheck if:")
        print(f"  1. Device is connected: ls -la {port}")
        print(f"  2. You have permissions: sudo chmod 666 {port}")
        print(f"  3. Port is available: lsof | grep {port}")

    except KeyboardInterrupt:
        print("\n\n✅ Capture stopped")
        if out_file:
            out_file.close()
            print(f"Data saved to: {output_file}")

    finally:
        if ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()
