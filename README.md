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

### Home Assistant (Custom Component)

1. Copy `custom_components/igneo` to your HA `custom_components` folder:
```bash
cp -r custom_components/igneo ~/.homeassistant/custom_components/
```

2. Restart Home Assistant

3. Go to Settings → Devices & Services → Create Integration → Search "Igneo"

4. Enter your igneo.pl credentials and device ID

### Device ID

You can find your device ID in:
- igneo.pl dashboard URL: `https://igneo.pl/device/2023873659`
- Or get it from HAR file analysis

## Features

- 📊 Real-time sensor data (temperatures, fuel counter, burner status)
- 🔄 Automatic polling every 5 minutes
- 🌡️ Temperature monitoring and alerts
- ⛽ Fuel consumption tracking
- 🔥 Burner status notifications
- 🚰 Hot water (CWU) temperature monitoring

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
