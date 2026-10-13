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

### ⚡ Quick Start (5 minutes)

**Prerequisites:**
- Home Assistant with HACS installed
- igneo.pl account with Igneo Slim boiler

**Steps:**
1. Open Home Assistant → HACS → Integrations
2. Click ⋮ → **Custom repositories**
3. Paste: `https://github.com/barthex/igneo-ha`
4. Category: **Integration** → Create
5. Find **Estyma Igneo Slim** → Install
6. Restart Home Assistant
7. Settings → Devices & Services → **+ Create Integration**
8. Search **Igneo** → Enter credentials

**Done!** Your boiler is now in Home Assistant 🔥

---

### 🚀 Method 1: HACS (Recommended - No Git Needed)

**Install from GitHub repository URL without cloning:**

1. **Ensure HACS is installed**
   - If not: https://hacs.xyz/docs/setup/prerequisites

2. **Open HACS in Home Assistant**
   - Go to: **HACS** → **Integrations**

3. **Add Custom Repository**
   - Click the **⋮** (three dots) in top-right corner
   - Select **Custom repositories**
   - Paste repository URL: `https://github.com/barthex/igneo-ha`
   - Choose Category: **Integration**
   - Click **Create**

4. **Install Integration**
   - Search for **"Estyma Igneo Slim"**
   - Click the result
   - Click **Install**
   - Wait for installation to complete

5. **Restart Home Assistant**
   - Settings → System → Restart

6. **Configure Integration**
   - Settings → Devices & Services
   - Click **+ Create Integration**
   - Search for **"Igneo"**
   - Click result
   - Enter your details:
     - **Username**: your igneo.pl login
     - **Password**: your igneo.pl password  
     - **Device ID**: from igneo.pl URL (e.g., `https://igneo.pl/device/YOUR_DEVICE_ID`)
     - **Standard fuel load**: 75kg (adjust to your typical refill: 5×15kg bags)
     - **Daily consumption**: 5kg/day (adjust based on heating season)
     - **Low fuel alert threshold**: 15kg (default - alert when below this level)
   - Click **Create**

7. **Enjoy!**
   - Boiler data appears in Home Assistant
   - Sensors available in automations, templates, etc.

**Note:** Currently requires manual custom repository setup. 
This is temporary while the integration is still in development. 
Future versions will be available directly from HACS marketplace.

**No command line, no git clone needed!** 🎉

### HACS Default Registry (Work in Progress)

⏳ **Status:** Planning to submit to HACS Default Registry in future versions

Currently available through **Custom Repositories** only. Once stability is proven (v0.2.0+), we'll submit for inclusion in the official HACS marketplace.

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

## ☕ Support This Project

If you find this integration useful and want to support its development:

[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-FFD700?logo=buy-me-a-coffee&logoColor=black)](YOUR_BUYMEACOFFEE_LINK)

Your support helps fund:
- New features and improvements
- Maintenance and bug fixes
- Better documentation

Thank you! 🙏

## Roadmap

### ✅ Completed (v0.1.0)
- [x] API client with authentication & cookie caching
- [x] Sensor entities (11 - temps, fuel, status)
- [x] Climate entities (2 - CWU & room thermostats)
- [x] Binary sensor alerts (3 - low fuel, high temp, burner status)
- [x] Custom services (4 - temperature control)
- [x] Home Assistant integration
- [x] HACS custom repository support
- [x] Fuel estimation with configurable consumption
- [x] Full English documentation

### 🔄 In Progress / Planned (v0.2.0+)
- [ ] **HACS Default Registry** (after stability proven)
- [ ] Energy dashboard integration
- [ ] Statistics and history tracking
- [ ] Multi-device support per user
- [ ] Advanced automation templates
- [ ] Mobile app support
- [ ] Webhook support for external integrations

## Changelog

### v0.1.0 (2026-10-13)
- Initial release
- Basic sensor and climate entities
- Binary sensors with alerts
- Example automations and dashboard
- RPi4 optimization with cookie caching
