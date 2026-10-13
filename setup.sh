#!/bin/bash
# Setup virtual environment

echo "🔧 Setting up virtual environment..."

# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To activate venv run:"
echo "  source venv/bin/activate"
echo ""
echo "Then run exploration script:"
echo "  python3 scripts/explore_local_module.py"
