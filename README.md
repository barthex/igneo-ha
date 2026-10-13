# Estyma Igneo Slim — Home Assistant Integration

A complete Home Assistant integration for Estyma Igneo Slim boiler controller via igneo.pl service.

## Features

### Sensors (11 entities)
- 📊 Real-time sensor data (boiler temp, room temp, CWU temp)
- ⛽ Fuel consumption tracking in kg with low fuel alerts
- 💨 Oxygen level monitoring
- 🏢 Device information (type, number of circuits)
- 🔥 Burner status (heating, ignition, pause, cleaning)

### Climate Control
- 🚰 Hot water (CWU) thermostat (30-60°C)
- 🏠 Room temperature controller (10-30°C)
- Smooth temperature adjustments via Home Assistant

### Alerts & Automation
- 🚨 **Binary Sensors** - 3 alert conditions:
  - Low fuel alert (< 50kg)
  - Burner running status
  - High boiler temperature (> 80°C)

### Services (call from automations)
- `igneo.set_cwu_temperature` - Set hot water temperature
- `igneo.set_room_temperature` - Set room temperature
- `igneo.increase_temperature` - Increase +1°C
- `igneo.decrease_temperature` - Decrease -1°C

### Other Features
- 🔄 Automatic polling every 5 minutes
- 📱 Cookie caching for efficient Raspberry Pi 4 usage
- 📋 7 example automations included
- 🎨 Lovelace dashboard template
- 🔐 Secure authentication via Selenium

## Installation

### 🚀 Method 1: HACS (Recommended)

1. Install [HACS](https://hacs.xyz/docs/setup/prerequisites) if not already installed

2. In Home Assistant: **HACS → Integrations → ⋮ → Custom repositories**

3. Add repository:
   - **Repository URL**: `https://github.com/barthex/igneo-ha`
   - **Category**: Integration
   - Click **Create**

4. Find **Estyma Igneo Slim** in HACS → **Install**

5. **Restart** Home Assistant

6. Go to **Settings → Devices & Services → Create Integration → Igneo**

7. Enter credentials:
   - **Username**: your igneo.pl login
   - **Password**: your igneo.pl password
   - **Device ID**: found in igneo.pl URL (e.g., `https://igneo.pl/device/YOUR_DEVICE_ID`)

### Manual Installation

1. Copy `custom_components/igneo` to your HA `custom_components` folder:
```bash
cp -r custom_components/igneo ~/.homeassistant/custom_components/
```

2. Restart Home Assistant

3. Go to **Settings → Devices & Services → Create Integration → Search "Igneo"**

4. Enter your igneo.pl credentials and device ID

### RPi4 Optimization 🚀

**Good news!** This integration is RPi4-friendly with cookie caching:
- **First login**: Uses Selenium (full browser automation) - ~10 seconds
- **After that**: Uses cached cookies (~1 second per polling)
- **RAM usage**: ~10MB per cycle (vs 500MB with full Selenium)

Cookies are cached in `~/.igneo/` directory as JSON files.

### Device ID

You can find your device ID in:
- igneo.pl dashboard URL: `https://igneo.pl/device/YOUR_DEVICE_ID`
- Or get it from HAR file analysis (DevTools Network tab)

## Usage Examples

### Service Calls (in automations)

```yaml
# Set CWU temperature
- service: igneo.set_cwu_temperature
  data:
    device_id: "YOUR_DEVICE_ID"
    temperature: 50

# Set room temperature
- service: igneo.set_room_temperature
  data:
    device_id: "YOUR_DEVICE_ID"
    temperature: 20

# Quick +1°C
- service: igneo.increase_temperature
  data:
    device_id: "YOUR_DEVICE_ID"
```

### Template Examples

```jinja2
# Get fuel in kilograms
{{ (state_attr('sensor.igneo_fuel_counter', 'value') | int(0)) / 1000 }}kg

# Check if heating
{% if state_attr('binary_sensor.igneo_burner_active', 'state') == 'on' %}
  Heating active
{% endif %}

# Alert on low fuel
{% if states('binary_sensor.igneo_low_fuel_alert') == 'on' %}
  ⛽ Low fuel alert!
{% endif %}
```

### Ready-to-Use Examples

Check `examples/` directory:
- **automations.yaml** - 7 example automations
- **lovelace.yaml** - Dashboard configuration

Copy and customize for your needs!

## Architecture

```
Estyma Igneo Slim (RS485)
    ↓
Vide.Net Internet Module (10.73.40.40)
    ↓
igneo.pl Service (API)
    ↓
Python API Client (src/igneo_api.py)
    ↓
Home Assistant Integration
    ↓
Sensors, Climate, Binary Sensors, Services
```

## Technical Details

### API Reverse Engineering

The integration communicates with igneo.pl service through three endpoints:
- `POST /info_panel_update` - Get device data
- `POST /info_set_order` - Set parameters
- `POST /info_check_order` - Check order status

Authentication is handled via HTML form login, then cookies are cached for efficiency.

### Cookie Caching

First run uses Selenium for authentication (browser automation), subsequent runs use cached cookies. This reduces RAM usage from ~500MB to ~10MB per polling cycle.

## Requirements

- Home Assistant 2024.1.0+
- Python 3.11+
- requests library
- selenium (for first login)
- webdriver-manager (for Chrome driver)

## Development

### Setup

```bash
# Clone repo
git clone https://github.com/barthex/igneo-ha.git
cd igneo-ha

# Setup venv
bash setup.sh
source venv/bin/activate

# Test API client
python3 scripts/test_api.py
```

### Project Structure

```
src/
  igneo_api.py      # Python API client with cookie caching
  models.py         # Data models
custom_components/igneo/
  __init__.py       # Integration setup
  sensor.py         # Sensor entities
  climate.py        # Climate/thermostat entities
  binary_sensor.py  # Alert sensors
  services.py       # Custom services
  config_flow.py    # Setup wizard
  manifest.json     # Metadata
examples/
  automations.yaml  # Example automations
  lovelace.yaml     # Dashboard configuration
scripts/
  test_api.py       # API testing tool
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Submitting pull requests
- Development setup
- Code style

## License

MIT License - see [LICENSE](LICENSE) file

## Disclaimer

This integration is not affiliated with Estyma Electronics. Use at your own risk. The authors are not responsible for any issues arising from the use of this integration.

## Support

- 📖 [GitHub Issues](https://github.com/barthex/igneo-ha/issues) - Report bugs
- 💬 [Discussions](https://github.com/barthex/igneo-ha/discussions) - Ask questions
- 🚀 [Releases](https://github.com/barthex/igneo-ha/releases) - Check updates

## Roadmap

- [x] API client with authentication
- [x] Sensor entities (11)
- [x] Climate entities (2)
- [x] Binary sensor alerts (3)
- [x] Custom services (4)
- [x] Home Assistant integration
- [x] HACS support
- [ ] Energy dashboard integration
- [ ] Statistics and history tracking
- [ ] Multi-device support
- [ ] Advanced automation templates

## Changelog

### v0.1.0 (2026-10-13)
- Initial release
- Basic sensor and climate entities
- Binary sensors with alerts
- Example automations and dashboard
- RPi4 optimization with cookie caching
