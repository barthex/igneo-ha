# Contributing to Estyma Igneo HA Integration

Thank you for your interest! 🎉

## Reporting Issues

1. Check if the issue already exists in [Issues](https://github.com/barthex/igneo-ha/issues)
2. If not - open a new Issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Home Assistant version
   - Integration version
   - Logs (if available)

## Submitting Pull Requests

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Guidelines

- One feature/fix per PR
- Update README if adding new features
- Test on Home Assistant (if possible)
- Follow PEP 8 style guide
- Include descriptive commit messages
- Link related issues in PR description

## Development Setup

```bash
# Clone repo
git clone https://github.com/barthex/igneo-ha.git
cd igneo-ha

# Setup virtual environment
bash setup.sh
source venv/bin/activate

# Test API client
python3 scripts/test_api.py
```

## Areas for Contribution

- 🐛 Bug fixes
- 📚 Documentation improvements
- 🎨 UI/UX improvements (Lovelace templates)
- 🧪 Testing & test cases
- 🌍 Internationalization (translations)
- ⚡ Performance optimizations
- 🔧 New features/sensors

## Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions
- Keep functions small and focused
- Use meaningful variable names

## Testing

Before submitting:
```bash
# Test API client
python3 scripts/test_api.py

# Check Python syntax
python3 -m py_compile src/*.py custom_components/igneo/*.py
```

## Questions?

- Open an Issue with label `question`
- Check existing Issues for answers
- Look at `examples/` directory for usage patterns

## Code of Conduct

- Be respectful to all contributors
- Welcome diverse perspectives
- Focus on the code, not the person
- Help each other learn and grow

Thanks for contributing! 🚀
