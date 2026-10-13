#!/bin/bash
# Setup RS485 debugging environment for Estyma Igneo Slim

set -e

echo "🔌 Setting up RS485 debugging environment..."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install pyserial

# Check for CoolTerm (macOS only)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo "📦 Optional: Install CoolTerm for easier serial monitoring"
    echo "   Download from: https://freeware.the-meister.org/"
    echo ""
fi

# List available serial ports
echo ""
echo "📍 Available serial ports:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    ls -la /dev/tty.* /dev/cu.* 2>/dev/null || echo "   (none found)"
else
    ls -la /dev/ttyUSB* /dev/ttyACM* 2>/dev/null || echo "   (none found)"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📖 Quick start:"
echo "   1. Connect USB RS485 adapter to your computer"
echo "   2. Note the port (e.g., /dev/ttyUSB0)"
echo "   3. Run: python3 scripts/rs485_logger.py /dev/ttyUSB0"
echo ""
echo "📚 Full guide: see docs/RS485_DEBUGGING.md"
