#!/bin/bash
# Setup virtual environment

echo "🔧 Setting up virtual environment..."

# Create venv
python3 -m venv venv

# Install requirements in venv
echo "📦 Installing dependencies..."
./venv/bin/pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To activate venv run:"
echo "  source venv/bin/activate"
echo ""
echo "Then run exploration script:"
echo "  python3 scripts/explore_local_module.py"
