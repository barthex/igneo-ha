# Estyma Igneo Slim — Home Assistant Integration

Integracja sterownika pieca Estyma Igneo Slim z Home Assistantem poprzez serwis igneo.pl.

## Funktionalność

- ✅ Włączanie/wyłączanie grzania
- ✅ Podgląd temperatury zewnętrznej
- ✅ Podgląd temperatury kotła
- ✅ Status kotła (modulacja, zatrzymany, rozpalanie, czyszczenie)
- ✅ Podgląd statusu CWU
- ✅ Statystyki zużycia paliwa
- ⏳ Alert o możliwym końcu paliwa
- ⏳ Rekomendacje optymalizacyjne

## Architektura

```
igneo.pl API
     ↓
src/igneo_api.py (Python client)
     ↓
custom_components/igneo/ (Home Assistant component)
     ↓
Home Assistant Entities & Services
```

## Setup

### Wymagania

- Python 3.11+
- Home Assistant 2024+
- Dostęp do igneo.pl

### Instalacja

```bash
# Clone
git clone <repo>
cd estyma-sterownik

# Ustawienia
cp envs/.env.example envs/.env.local
# Edytuj envs/.env.local z loginem i hasłem
```

## Struktura

```
src/
  igneo_api.py      # API client
  models.py         # Data models
custom_components/igneo/
  manifest.json     # HA component metadata
  __init__.py       # Component loader
  api.py            # API integration
  entities.py       # HA entities
scripts/
  explore_api.py    # API exploration tool
```

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
   - **Device ID**: found in igneo.pl URL (e.g., `https://igneo.pl/device/2023873659`)

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
- igneo.pl dashboard URL: `https://igneo.pl/device/2023873659`
- Or get it from HAR file analysis

## Features

### Sensors (11 entities)
- 📊 Real-time sensor data (temperatures, fuel counter, burner status)
- 🌡️ Boiler, room, CWU temperatures
- ⛽ Fuel consumption in kg (with low fuel alert)
- 💨 Oxygen level monitoring
- 🏢 Device info (type, circuits)

### Climate Control
- 🚰 Hot water (CWU) thermostat (30-60°C)
- 🏠 Room temperature controller (10-30°C)
- Smooth temperature adjustments

### Alerts & Automation
- 🚨 **Binary Sensors** - 3 alert conditions:
  - Low fuel (< 50kg)
  - Burner running status
  - High boiler temp (> 80°C)

### Services (call from automations)
- `igneo.set_cwu_temperature` - Set hot water temp
- `igneo.set_room_temperature` - Set room temp
- `igneo.increase_temperature` - +1°C
- `igneo.decrease_temperature` - -1°C

### Other
- 🔄 Automatic polling every 5 minutes
- 📱 Cookie caching for RPi4 efficiency
- 📋 7 example automations included
- 🎨 Lovelace dashboard template

## Usage Examples

### Service Calls (in automations)

```yaml
# Set CWU temperature
- service: igneo.set_cwu_temperature
  data:
    device_id: "2023873659"
    temperature: 50

# Set room temperature
- service: igneo.set_room_temperature
  data:
    device_id: "2023873659"
    temperature: 20

# Quick +1°C
- service: igneo.increase_temperature
  data:
    device_id: "2023873659"
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

## Development

```bash
# Test API client
python3 scripts/test_api.py

# Explore API
python3 scripts/explore_api.py
```

## Status

✅ Faza 1: Reverse engineering API igneo.pl - DONE
✅ Faza 2: Python API client - DONE
✅ Faza 3: Home Assistant integration - DONE
⏳ Faza 4: Climate entity (temperature control)
⏳ Faza 5: Service calls (setting parameters)
