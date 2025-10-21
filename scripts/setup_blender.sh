
# ============================================================================
# scripts/setup_blender.sh
# ============================================================================
#!/bin/bash
# Setup script for Blender and dependencies

set -e

echo "Setting up Blender for nunalleq-synth..."

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

# Set Blender version
BLENDER_VERSION="3.6"
BLENDER_VERSION_FULL="3.6.5"

# Download URLs
if [ "$OS" = "linux" ]; then
    BLENDER_URL="https://download.blender.org/release/Blender${BLENDER_VERSION}/blender-${BLENDER_VERSION_FULL}-linux-x64.tar.xz"
    BLENDER_ARCHIVE="blender-${BLENDER_VERSION_FULL}-linux-x64.tar.xz"
    BLENDER_DIR="blender-${BLENDER_VERSION_FULL}-linux-x64"
elif [ "$OS" = "macos" ]; then
    BLENDER_URL="https://download.blender.org/release/Blender${BLENDER_VERSION}/blender-${BLENDER_VERSION_FULL}-macos-x64.dmg"
    echo "macOS: Please download Blender manually from ${BLENDER_URL}"
    exit 0
fi

# Download Blender
echo "Downloading Blender ${BLENDER_VERSION_FULL}..."
wget -q --show-progress "$BLENDER_URL"

# Extract
echo "Extracting Blender..."
tar -xf "$BLENDER_ARCHIVE"

# Move to /opt or user directory
if [ -w "/opt" ]; then
    INSTALL_DIR="/opt/blender"
    sudo mv "$BLENDER_DIR" "$INSTALL_DIR"
    sudo ln -sf "$INSTALL_DIR/blender" /usr/local/bin/blender
else
    INSTALL_DIR="$HOME/.local/blender"
    mkdir -p "$HOME/.local/bin"
    mv "$BLENDER_DIR" "$INSTALL_DIR"
    ln -sf "$INSTALL_DIR/blender" "$HOME/.local/bin/blender"
    echo "Add $HOME/.local/bin to your PATH"
fi

# Cleanup
rm "$BLENDER_ARCHIVE"

# Install Python packages to Blender's Python
echo "Installing Python packages to Blender..."
BLENDER_PYTHON="$INSTALL_DIR/${BLENDER_VERSION}/python/bin/python3.10"

if [ -f "$BLENDER_PYTHON" ]; then
    "$BLENDER_PYTHON" -m ensurepip
    "$BLENDER_PYTHON" -m pip install --upgrade pip
    "$BLENDER_PYTHON" -m pip install numpy pyyaml pydantic
    echo "Blender Python packages installed"
else
    echo "Warning: Could not find Blender Python"
fi

echo "Blender setup complete!"
echo "Blender installed to: $INSTALL_DIR"
blender --version
