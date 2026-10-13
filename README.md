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

## Development

```bash
python3 scripts/explore_api.py
```

## Status

🚀 Faza 1: Reverse engineering API igneo.pl
