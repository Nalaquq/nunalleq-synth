# Installation Guide

This guide covers all installation methods for `nunalleq-synth`, from simple pip installation to advanced Blender integration.

## Quick Start

```bash
# Install core library (always works)
pip install nunalleq-synth

# Install with Blender support (Python 3.11 only)
pip install nunalleq-synth[blender]
```

## Understanding Blender Integration

The `nunalleq-synth` library has **two modes**:

1. **Core Library**: Analysis, configuration, annotation tools (no Blender needed)
2. **Full Pipeline**: 3D rendering and physics simulation (requires Blender)

For actual synthetic data generation, you need Blender. There are **three ways** to get it:

## Installation Methods

### Method 1: pip install bpy (Simplest - Python 3.11 Only)

**Requirements**: Python 3.11

```bash
# Create virtual environment with Python 3.11
python3.11 -m venv venv
source venv/bin/activate

# Install with Blender support
pip install nunalleq-synth[blender]

# Verify installation
python -c "import bpy; print(bpy.app.version_string)"
```

**Pros**:
- Easiest installation
- Self-contained environment
- Works on Windows, macOS, Linux

**Cons**:
- Only works with Python 3.11
- Large download (~300-500 MB)
- May not be available on all platforms

**When to use**: You're using Python 3.11 and want the simplest setup.

---

### Method 2: System Blender + Install Library into Blender's Python (Most Flexible)

**Requirements**: Any Python version (3.8+), System Blender 3.6+

This method installs Blender system-wide and installs your library into Blender's bundled Python.

#### Step 1: Install Blender

**Linux (Ubuntu/Debian):**
```bash
# Option A: Using snap (recommended)
sudo snap install blender --classic

# Option B: Using our setup script
bash scripts/setup_blender.sh

# Option C: Download from blender.org
wget https://download.blender.org/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz
tar -xf blender-4.0.2-linux-x64.tar.xz
sudo mv blender-4.0.2-linux-x64 /opt/blender
sudo ln -s /opt/blender/blender /usr/local/bin/blender
```

**macOS:**
```bash
# Using Homebrew
brew install --cask blender

# Or download from blender.org
# https://www.blender.org/download/
```

**Windows:**
```powershell
# Using winget
winget install BlenderFoundation.Blender

# Or download installer from blender.org
```

#### Step 2: Find Blender's Python

```bash
# Linux/macOS
BLENDER_PYTHON=$(find /opt/blender -name python3.* -type f | grep bin)
# or for snap: /snap/blender/current/4.*/python/bin/python3.*

# macOS (Homebrew)
BLENDER_PYTHON=/Applications/Blender.app/Contents/Resources/4.*/python/bin/python3.*

# Windows
# C:\Program Files\Blender Foundation\Blender 4.0\4.0\python\bin\python.exe
```

#### Step 3: Install Library into Blender's Python

```bash
# Ensure pip is available
$BLENDER_PYTHON -m ensurepip
$BLENDER_PYTHON -m pip install --upgrade pip

# Install nunalleq-synth into Blender's Python
$BLENDER_PYTHON -m pip install nunalleq-synth

# Verify
$BLENDER_PYTHON -c "import nunalleq_synth; print(nunalleq_synth.__version__)"
```

#### Step 4: Run Scripts

```bash
# Use Blender's Python to run your scripts
$BLENDER_PYTHON examples/batch_processing.py

# Or create an alias
echo "alias blender-python='$BLENDER_PYTHON'" >> ~/.bashrc
source ~/.bashrc
blender-python your_script.py
```

**Pros**:
- Works with any Python version
- Most reliable cross-platform
- Can use system Blender GUI for debugging
- Full control over Blender version

**Cons**:
- More setup steps
- Need to use Blender's Python instead of your virtual environment
- Two separate Python environments to manage

**When to use**: You need maximum flexibility, want to use Blender GUI, or pip install bpy doesn't work.

---

### Method 3: Docker (Best for Production/CI)

**Requirements**: Docker, NVIDIA Docker (for GPU support)

```bash
# Build image
docker build -t nunalleq-synth:latest .

# Run with GPU support
docker run --gpus all \
  -v $(pwd)/models:/data/models \
  -v $(pwd)/output:/data/output \
  nunalleq-synth:latest \
  generate --models /data/models --output /data/output --num-images 1000

# Or using docker-compose
docker-compose up
```

**Pros**:
- Reproducible environment
- No local Blender installation needed
- Perfect for CI/CD
- GPU acceleration support

**Cons**:
- Requires Docker knowledge
- Larger disk space
- Setup overhead

**When to use**: Production deployments, CI/CD, or consistent environments across team.

---

## Installation Verification

After installation, verify everything works:

```python
# Test core library (no Blender needed)
python -c "from nunalleq_synth import GenerationConfig; print('Core: OK')"

# Test Blender integration
python -c "import bpy; from nunalleq_synth import SyntheticGenerator; print('Blender: OK')"

# Check GPU availability
python -c "from nunalleq_synth.utils.gpu import check_gpu; check_gpu()"
```

## Development Installation

For contributing to the project:

```bash
# Clone repository
git clone https://github.com/nalaquq/nunalleq-synth.git
cd nunalleq-synth

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install in development mode with all dependencies
pip install -e ".[all]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'bpy'"

**Solution**: You're not using Python 3.11, or bpy isn't available for your platform. Use Method 2 (System Blender) or Method 3 (Docker).

### "ImportError: DLL load failed" (Windows)

**Solution**: Install Visual C++ Redistributable:
- https://aka.ms/vs/17/release/vc_redist.x64.exe

### "CUDA not available" / GPU not detected

**Solution**:
```bash
# Check NVIDIA drivers
nvidia-smi

# Install CUDA toolkit
# https://developer.nvidia.com/cuda-downloads

# Verify in Blender
python -c "import bpy; bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'"
```

### pip install hangs or takes forever

**Solution**: bpy is a large package (300-500 MB). Be patient or use system Blender.

### "This package requires Python 3.11"

**Solution**: Either:
1. Use Python 3.11: `python3.11 -m venv venv`
2. Use system Blender (Method 2)
3. Use Docker (Method 3)

## Platform-Specific Notes

### Windows WSL2

WSL2 has limited GPU access. For best results:
- Use Method 2 (System Blender in Windows) and access from WSL
- Or use Method 3 (Docker with --gpus all)
- See: https://docs.microsoft.com/en-us/windows/ai/directml/gpu-cuda-in-wsl

### macOS (Apple Silicon)

```bash
# Blender works on M1/M2/M3 Macs
brew install --cask blender

# Use Blender's Python
/Applications/Blender.app/Contents/Resources/4.*/python/bin/python3.* -m pip install nunalleq-synth
```

### Linux (Headless Servers)

```bash
# Install Blender without GUI
sudo apt-get install xvfb
xvfb-run -a blender --background --python your_script.py

# Or use EEVEE engine (faster, no GPU needed)
# In your config: render.engine = "EEVEE"
```

## Recommended Setup by Use Case

| Use Case | Recommended Method | Why |
|----------|-------------------|-----|
| Quick testing | Method 1 (pip) | Fastest setup |
| Active development | Method 2 (System Blender) | Debugging with GUI |
| Production | Method 3 (Docker) | Reproducibility |
| CI/CD | Method 3 (Docker) | Consistent environments |
| Multi-version testing | Method 3 (Docker) | Isolated environments |
| Teaching/Workshops | Method 1 (pip) | Easiest for students |

## Next Steps

After installation:
1. Read the [Quick Start Guide](../README.md#quick-start)
2. Check [Configuration Guide](./CONFIGURATION.md)
3. Review [Examples](../examples/)
4. Join our [Community Discussions](https://github.com/nalaquq/nunalleq-synth/discussions)

## Getting Help

- **Documentation**: https://nunalleq-synth.readthedocs.io
- **Issues**: https://github.com/nalaquq/nunalleq-synth/issues
- **Email**: info@nalaquq.com
