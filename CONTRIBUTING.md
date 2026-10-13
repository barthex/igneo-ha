# Contributing to Estyma Igneo HA Integration

Dziękujemy za zainteresowanie! 🎉

## Jak zgłaszać problemy

1. Sprawdź czy problem już istnieje w [Issues](https://github.com/barthex/igneo-ha/issues)
2. Jeśli nie - otwórz nowy Issue z:
   - Opisem problemu
   - Krokami do reprodukcji
   - Logs (jeśli dostępne)
   - Twoja konfiguracja HA

## Jak zgłaszać Pull Requests

1. **Fork** repository
2. **Stwórz branch** dla feature: `git checkout -b feature/amazing-feature`
3. **Commituj zmiany**: `git commit -m 'Add amazing feature'`
4. **Push** do branch: `git push origin feature/amazing-feature`
5. **Otwórz Pull Request**

### Guidelines

- Jeden feature/fix per PR
- Zaktualizuj README jeśli dodajesz nowe features
- Testuj na Home Assistant (jeśli możliwe)
- Follow PEP 8 style guide

## Development Setup

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

## Areas for Contribution

- 🐛 Bug fixes
- 📚 Documentation improvements
- 🎨 UI improvements (Lovelace templates)
- 🧪 Testing & test cases
- 🌍 Translations
- ⚡ Performance optimizations

## Questions?

- Open an Issue with label `question`
- Check existing Issues for answers
- Look at examples/ directory for usage

Thanks! 🚀
