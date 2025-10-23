#!/bin/bash
# ============================================================================
# scripts/setup_blender.sh
# ============================================================================
# Setup script for installing Blender and nunalleq-synth
#
# This script:
# 1. Detects your OS and suggests the best installation method
# 2. Optionally installs Blender system-wide
# 3. Installs nunalleq-synth into Blender's Python environment
#
# Usage:
#   bash scripts/setup_blender.sh [--auto]
#
# Options:
#   --auto    Skip prompts and use defaults where possible
# ============================================================================

set -e

AUTO_MODE=false
if [[ "$1" == "--auto" ]]; then
    AUTO_MODE=true
fi

echo "========================================="
echo "Nunalleq-Synth Blender Setup"
echo "========================================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

echo "Detected OS: $OS"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to find Blender Python
find_blender_python() {
    local blender_python=""

    # Try common locations
    if [ "$OS" = "linux" ]; then
        # Snap installation
        if [ -d "/snap/blender" ]; then
            blender_python=$(find /snap/blender/current -name "python3.*" -type f 2>/dev/null | grep bin | head -1)
        fi
        # System installation
        if [ -z "$blender_python" ] && [ -d "/opt/blender" ]; then
            blender_python=$(find /opt/blender -name "python3.*" -type f 2>/dev/null | grep bin | head -1)
        fi
        # User installation
        if [ -z "$blender_python" ] && [ -d "$HOME/.local/blender" ]; then
            blender_python=$(find "$HOME/.local/blender" -name "python3.*" -type f 2>/dev/null | grep bin | head -1)
        fi
    elif [ "$OS" = "macos" ]; then
        # Application bundle
        if [ -d "/Applications/Blender.app" ]; then
            blender_python=$(find /Applications/Blender.app -name "python3.*" -type f 2>/dev/null | grep bin | head -1)
        fi
    fi

    echo "$blender_python"
}

# Check if Blender is already installed
BLENDER_PYTHON=$(find_blender_python)

if [ -n "$BLENDER_PYTHON" ] && [ -f "$BLENDER_PYTHON" ]; then
    echo "✓ Found existing Blender installation"
    echo "  Python: $BLENDER_PYTHON"
    BLENDER_VERSION=$("$BLENDER_PYTHON" --version 2>&1 | cut -d' ' -f2 || echo "unknown")
    echo "  Version: $BLENDER_VERSION"
    echo ""
else
    echo "❌ Blender not found on your system"
    echo ""
    echo "Recommended installation methods:"
    echo ""

    if [ "$OS" = "linux" ]; then
        echo "Option 1 (Recommended): Using snap"
        echo "  sudo snap install blender --classic"
        echo ""
        echo "Option 2: Download from blender.org"
        echo "  wget https://download.blender.org/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz"
        echo "  tar -xf blender-4.0.2-linux-x64.tar.xz"
        echo "  sudo mv blender-4.0.2-linux-x64 /opt/blender"
        echo ""

        if ! $AUTO_MODE; then
            read -p "Install Blender using snap now? (y/N) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                if command_exists snap; then
                    echo "Installing Blender via snap..."
                    sudo snap install blender --classic
                    BLENDER_PYTHON=$(find_blender_python)
                else
                    echo "❌ Snap is not installed. Please install it first:"
                    echo "  sudo apt install snapd"
                    exit 1
                fi
            else
                echo "Please install Blender manually and re-run this script."
                exit 0
            fi
        else
            echo "⚠️  Auto mode: Please install Blender manually"
            exit 1
        fi

    elif [ "$OS" = "macos" ]; then
        echo "Option 1 (Recommended): Using Homebrew"
        echo "  brew install --cask blender"
        echo ""
        echo "Option 2: Download from blender.org"
        echo "  https://www.blender.org/download/"
        echo ""

        if ! $AUTO_MODE; then
            read -p "Install Blender using Homebrew now? (y/N) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                if command_exists brew; then
                    echo "Installing Blender via Homebrew..."
                    brew install --cask blender
                    BLENDER_PYTHON=$(find_blender_python)
                else
                    echo "❌ Homebrew is not installed. Install from https://brew.sh"
                    exit 1
                fi
            else
                echo "Please install Blender manually and re-run this script."
                exit 0
            fi
        else
            echo "⚠️  Auto mode: Please install Blender manually"
            exit 1
        fi
    fi

    # Re-check for Blender Python
    BLENDER_PYTHON=$(find_blender_python)
    if [ -z "$BLENDER_PYTHON" ] || [ ! -f "$BLENDER_PYTHON" ]; then
        echo "❌ Could not find Blender Python after installation"
        exit 1
    fi
fi

echo ""
echo "========================================="
echo "Installing nunalleq-synth"
echo "========================================="
echo ""

# Ensure pip is available
echo "Setting up pip in Blender's Python..."
"$BLENDER_PYTHON" -m ensurepip 2>/dev/null || true
"$BLENDER_PYTHON" -m pip install --upgrade pip

# Install nunalleq-synth
echo ""
echo "Installing nunalleq-synth into Blender's Python environment..."
if [ -f "setup.py" ]; then
    # Development installation (in repo)
    "$BLENDER_PYTHON" -m pip install -e .
    echo "✓ Installed nunalleq-synth in development mode"
else
    # PyPI installation
    "$BLENDER_PYTHON" -m pip install nunalleq-synth
    echo "✓ Installed nunalleq-synth from PyPI"
fi

# Verify installation
echo ""
echo "========================================="
echo "Verifying Installation"
echo "========================================="
echo ""

if "$BLENDER_PYTHON" -c "import nunalleq_synth; print('nunalleq-synth version:', nunalleq_synth.__version__)" 2>/dev/null; then
    echo "✓ nunalleq-synth is installed and working"
else
    echo "❌ Installation verification failed"
    exit 1
fi

if "$BLENDER_PYTHON" -c "import bpy; print('Blender version:', bpy.app.version_string)" 2>/dev/null; then
    echo "✓ Blender (bpy) is accessible"
else
    echo "⚠️  Warning: bpy import failed"
fi

# Create helper alias suggestion
echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "To use nunalleq-synth, run your scripts with Blender's Python:"
echo ""
echo "  $BLENDER_PYTHON your_script.py"
echo ""
echo "Or create an alias for convenience:"
echo ""
if [ "$OS" = "linux" ]; then
    echo "  echo 'alias blender-python=\"$BLENDER_PYTHON\"' >> ~/.bashrc"
    echo "  source ~/.bashrc"
elif [ "$OS" = "macos" ]; then
    echo "  echo 'alias blender-python=\"$BLENDER_PYTHON\"' >> ~/.zshrc"
    echo "  source ~/.zshrc"
fi
echo ""
echo "Then you can use: blender-python your_script.py"
echo ""
echo "Next steps:"
echo "  1. Read the Quick Start guide: README.md"
echo "  2. Try an example: $BLENDER_PYTHON examples/batch_processing.py"
echo "  3. Read the docs: https://nunalleq-synth.readthedocs.io"
echo ""
