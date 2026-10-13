# RS485/CAN Debugging Guide for Estyma Igneo Slim

Advanced guide for reverse engineering the Estyma boiler via RS485 protocol.

## Goals

- 📊 Discover new parameters available in the boiler
- 🌡️ Find external temperature sensor value
- 🔧 Control boiler directly via Modbus RTU
- 📈 Extend API client with native Modbus support

## Hardware Setup

### USB RS485 Adapter

**Required:**
- USB to RS485 adapter (~30-50 PLN)
- Options:
  - FTDI FT232RL RS485
  - Waveshare RS485 CAN Hat (for RPi)
  - CH340 RS485 module

**Connection:**
```
Boiler RS485    →  USB Adapter
A (Twisted)     →  A
B (Twisted)     →  B
GND             →  GND
```

### Identify Connection Points

Check boiler's manual for RS485 connector location:
- Igneo Slim control panel
- Terminal block labeled "RS485", "CAN", or "Comms"
- 2-4 pins: usually A, B, GND, (GND)

## Software Setup

### Step 1: Install Tools

```bash
# macOS
brew install minicom screen pyserial

# Ubuntu/Debian
sudo apt install minicom screen python3-serial

# For Python Modbus support
pip install pymodbus
```

### Step 2: Identify Serial Port

```bash
# List available ports
ls -la /dev/tty.* /dev/cu.*  # macOS
ls -la /dev/ttyUSB*          # Linux
ls -la /dev/ttyACM*          # Linux (some CH340)
```

### Step 3: Monitor Traffic

#### Option A: CoolTerm (GUI - Recommended)

1. Download: https://freeware.the-meister.org/
2. Connect:
   - Port: /dev/ttyUSB0
   - Baud Rate: 19200
   - Data: 8 bits
   - Parity: Even (E)
   - Stop: 1 bit
3. Click "Open Port"
4. Observe data flowing between Vide.Net module and boiler

#### Option B: minicom (Terminal)

```bash
minicom -D /dev/ttyUSB0 -b 19200 -8 -o
# Ctrl+A, Z for menu
# Q to quit
```

#### Option C: Python Logger

```bash
python3 scripts/rs485_logger.py
```

## Estyma Igneo Protocol Info

### Expected Parameters

**Baud Rate:** 19200
**Parity:** Even (E)
**Stop Bits:** 1
**Data Bits:** 8
**Protocol:** Modbus RTU (most likely)

### Common Modbus Addresses (Hypothesis)

Based on API response fields:
```
Register 0x0001: Boiler temp (kociol_temp_sub1)
Register 0x0002: Room temp (tpok_obw1_sub1)
Register 0x0003: CWU temp (cwu_temp_obw1_sub1)
Register 0x0004: Fuel counter (licznik_paliwa_sub1)
Register 0x00XX: External temp (UNKNOWN - to find!)
```

### Modbus RTU Frame Format

```
[Slave ID] [Function] [Start Addr H] [Start Addr L] [Count H] [Count L] [CRC H] [CRC L]

Example (read 10 registers from address 0):
01 03 00 00 00 0A 84 0A

Response:
01 03 14 [20 bytes of data] [CRC]
```

## Research Steps

### Step 1: Capture Raw Traffic

1. Connect USB adapter to boiler's RS485
2. Start CoolTerm/minicom/logger
3. Boot up boiler or Vide.Net module
4. Observe data stream
5. Save session to file

### Step 2: Analyze Patterns

Look for:
- Repeating patterns (polling)
- Temperature values matching display
- Command sequences (when boiler changes state)

Example hex output:
```
01 03 00 01 00 02 65 E8  ← Request
01 03 04 01 2C 01 F4 7D  ← Response (temperature data)
```

### Step 3: Decode Addresses

Use Modbus decoder to find:
- Which register = boiler temp
- Which register = external temp
- Which register = settings
- Control registers (write-able)

### Step 4: Test with pymodbus

```python
from pymodbus.client import ModbusSerialClient as ModbusClient

client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=19200)
client.connect()

# Read 10 registers starting at address 0
result = client.read_holding_registers(0, 10, slave=1)
if result.isError():
    print(f"Error: {result}")
else:
    print(f"Registers: {result.registers}")
    for i, val in enumerate(result.registers):
        print(f"  Reg {i}: {val} (0x{val:04x})")
```

## Expected Findings

If successful, we'll find:
- ✅ Direct access to all boiler parameters
- ✅ External temperature sensor location
- ✅ Control registers for direct manipulation
- ✅ Potentially undocumented features

## Integration

Once parameters are mapped:
1. Update `src/igneo_api.py` with Modbus RTU support
2. Add direct boiler communication (bypass igneo.pl)
3. Add external temperature sensor
4. Implement write commands for control

## Resources

- [Modbus RTU Specification](http://www.modbus.org/docs/Modbus_over_serial_line_V1_02.pdf)
- [PyModbus Documentation](https://pymodbus.readthedocs.io/)
- [RS485 Debugging Tips](https://wiki.analog.com/resources/tools-software/linux-drivers/iio-uart)

## Safety Notes

⚠️ **WARNING:**
- Do NOT send random Modbus commands to boiler
- Test on disabled boiler first
- Incorrect commands could damage equipment
- Always verify with boiler manual
- Have serial number / manual ready

## Next Steps

1. Set up USB adapter
2. Monitor traffic with CoolTerm
3. Document observed patterns
4. Share findings with project maintainers
5. Implement native Modbus support

---

**Questions?**
- Open GitHub Issue with your findings
- Share captured data (sanitized)
- Help improve boiler integration!
