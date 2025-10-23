# Nunalleq Synthetic Data Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Physics-based synthetic data generation for Yup'ik artifact object detection using Blender.

This project supports the [Nunalleq Museum Digital Guide](https://www.nunalleq.org), enabling real-time artifact recognition in the museum through computer vision trained on synthetic data.

## 🎯 Project Goals

The Nunalleq Synthetic Data Generator addresses critical needs for the Nunalleq Museum:

1. **Training Object Detection Models** - Generate thousands of annotated images for training YOLO models
2. **Offline Operation** - Works without internet connectivity (critical for Y-K Delta villages)
3. **Cultural Heritage Preservation** - Digitally document Yup'ik material culture
4. **Community Engagement** - Enable interactive museum experiences for community members

## 🌟 Features

- **Physics-Based Placement** - Realistic object positioning using Blender's physics engine
- **Domain Randomization** - Varied lighting, camera angles, backgrounds, and materials
- **Automatic Annotation** - YOLO-format bounding box generation
- **GPU Acceleration** - CUDA support for fast rendering
- **Batch Processing** - Process multiple model directories in parallel
- **Docker Support** - Containerized deployment
- **Type-Safe** - Full type hints for better code quality
- **Extensible** - Modular architecture for customization

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [Development](#development)
- [Docker](#docker)
- [Cultural Guidelines](#cultural-guidelines)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Quick Install

```bash
# Install core library (works on any Python 3.8+)
pip install nunalleq-synth

# Install with Blender support (Python 3.11 only)
pip install nunalleq-synth[blender]
```

### Understanding Installation Options

`nunalleq-synth` can be installed in two ways:

1. **Core Only**: Configuration, annotation tools, utilities (no 3D rendering)
2. **With Blender**: Full pipeline including 3D rendering and physics simulation

**For actual data generation, you need Blender.** Choose one of these methods:

| Method | Best For | Python Version | Difficulty |
|--------|----------|----------------|------------|
| `pip install nunalleq-synth[blender]` | Quick start | 3.11 only | ⭐ Easy |
| System Blender + install into Blender's Python | Maximum flexibility | Any (3.8+) | ⭐⭐ Moderate |
| Docker | Production, CI/CD | Any | ⭐⭐ Moderate |

📖 **[Read the Complete Installation Guide →](docs/INSTALLATION.md)**

### Quick Start Options

#### Option 1: Using pip (Python 3.11 only)

```bash
# Create Python 3.11 environment
python3.11 -m venv venv
source venv/bin/activate

# Install with Blender
pip install nunalleq-synth[blender]
```

#### Option 2: Using System Blender

```bash
# 1. Install Blender system-wide
sudo apt install blender  # Linux (Ubuntu/Debian)
brew install --cask blender          # macOS

# 2. Install library into Blender's Python
BLENDER_PYTHON=$(blender --background --python-expr "import sys; print(sys.executable)")
$BLENDER_PYTHON -m pip install nunalleq-synth

# 3. Run with Blender's Python
$BLENDER_PYTHON your_script.py
```

#### Option 3: Using Docker

```bash
# Build and run
docker-compose up

# Or use pre-built image (when published)
docker pull nunalleq/nunalleq-synth:latest
```

### Development Installation

```bash
# Clone repository
git clone https://github.com/nalaquq/nunalleq-synth.git
cd nunalleq-synth

# Create virtual environment (Python 3.11 for Blender support)
python3.11 -m venv venv
source venv/bin/activate

# Install in development mode with all dependencies
pip install -e ".[all]"

# Install pre-commit hooks
pre-commit install
```

### Verify Installation

```bash
# Check core library
python -c "from nunalleq_synth import GenerationConfig; print('✓ Core library installed')"

# Check Blender integration
python -c "import bpy; from nunalleq_synth import SyntheticGenerator; print('✓ Blender integration working')"

# Check GPU support
python -c "from nunalleq_synth.utils.gpu import check_gpu; check_gpu()"
```

## 🎬 Quick Start

### Basic Usage

```python
from pathlib import Path
from nunalleq_synth import SyntheticGenerator, GenerationConfig

# Configure generation
config = GenerationConfig(
    model_dir=Path("models/artifacts"),
    output_dir=Path("output/dataset"),
    num_images=1000,
    max_objects_per_scene=3,
    random_seed=42,
)

# Generate dataset
generator = SyntheticGenerator(config)
generator.generate()
```

### Command Line

```bash
# Generate dataset
nunalleq-synth generate \
    --models ./models/ulus \
    --output ./output \
    --num-images 1000 \
    --resolution 1920 1080

# Use configuration file
nunalleq-synth generate --config configs/high_quality.yaml

# Validate dataset
nunalleq-synth validate --dataset ./output --visualize
```

## 📖 Usage

### Directory Structure

Organize your 3D models like this:

```
models/
├── ulus/
│   ├── ulu_001.glb
│   ├── ulu_002.glb
│   └── ...
├── masks/
│   ├── mask_001.glb
│   └── ...
└── dolls/
    └── ...
```

The directory names become class labels in the generated dataset.

### Output Structure

Generated datasets follow this structure:

```
output/
├── train/
│   ├── images/
│   │   ├── train_000000.jpg
│   │   └── ...
│   └── labels/
│       ├── train_000000.txt
│       └── ...
├── test/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
├── classes.txt
└── config.yaml
```

### YOLO Annotation Format

Each `.txt` file contains annotations in YOLO format:
```
<class_id> <x_center> <y_center> <width> <height>
```

All coordinates are normalized to [0, 1].

## ⚙️ Configuration

### Configuration Files

Create YAML configuration files for different scenarios:

```yaml
# configs/custom.yaml
model_dir: "./models/artifacts"
output_dir: "./output/custom"
num_images: 500
max_objects_per_scene: 2

physics:
  gravity: [0.0, 0.0, -9.81]
  simulation_steps: 120
  
render:
  engine: "CYCLES"
  samples: 256
  resolution: [1920, 1080]
  
randomization:
  lighting_intensity_range: [800.0, 2000.0]
  camera_distance_range: [0.5, 2.0]
```

### Python API

```python
from nunalleq_synth.pipeline.config import (
    GenerationConfig,
    PhysicsConfig,
    RenderConfig,
    RandomizationConfig,
)

config = GenerationConfig(
    model_dir=Path("models"),
    output_dir=Path("output"),
    num_images=1000,
    physics=PhysicsConfig(
        simulation_steps=200,
        substeps=15,
    ),
    render=RenderConfig(
        samples=512,
        resolution=(2560, 1440),
    ),
)
```

## 🛠️ Development

### Running Tests

```bash
# Run all tests
make test

# With coverage
make test-cov

# Specific test file
pytest tests/test_core/test_scene.py -v
```

### Code Quality

```bash
# Format code
make format

# Run linters
make lint

# Type checking
make type-check

# All checks
make format && make lint && make type-check && make test
```

### Project Structure

```
nunalleq_synth/
├── core/           # Scene, physics, rendering
├── objects/        # 3D model loading
├── randomization/  # Domain randomization
├── annotation/     # Bbox calculation
├── pipeline/       # Main generation pipeline
└── utils/          # Utilities
```

## 🐳 Docker

### Build Image

```bash
make docker-build
```

### Run Container

```bash
# Using docker-compose
docker-compose up nunalleq-synth

# Direct docker run
docker run -v $(pwd)/models:/data/models \
           -v $(pwd)/output:/data/output \
           --gpus all \
           nunalleq-synth:latest \
           generate --models /data/models --output /data/output
```

### Development Container

```bash
# Start development container
make docker-dev

# Inside container
nunalleq-synth generate --models /data/models --output /data/output
```

## 🌍 Cultural Guidelines

This project handles Yup'ik cultural artifacts with respect and care. When contributing:

1. **Respect Cultural Significance** - These are not just objects; they represent Yup'ik heritage
2. **Community Input** - Major changes should involve community members
3. **Data Sovereignty** - Keep data ownership with the Yup'ik community
4. **Appropriate Use** - Generated data is for educational/museum purposes only

See [docs/cultural_guidelines.md](docs/cultural_guidelines.md) for detailed guidance.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linters (`make test && make lint`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Standards

- Follow PEP 8 style guide
- Use type hints for all functions
- Write docstrings (Google style)
- Add tests for new features
- Keep commits atomic and well-described

## 📚 Documentation

Full documentation is available at [https://nunalleq-synth.readthedocs.io](https://nunalleq-synth.readthedocs.io)

### Build Docs Locally

```bash
make docs
open docs/_build/html/index.html
```

## 🙏 Acknowledgments

This project is made possible by:

- **Native Village of Kwinhagak (NVK)** - Project leadership and cultural guidance
- **Qanirtuuq Inc (Q-Corp)** - Museum ownership and operations
- **Nalaquq, LLC** - Technical development and CRM solutions
- **University of Aberdeen** - Archaeological research partnership
- **Institute of Museum and Library Services (IMLS)** - Grant funding

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

- **Project Website**: [https://www.nunalleq.org](https://www.nunalleq.org)
- **Email**: info@nalaquq.com
- **Issues**: [GitHub Issues](https://github.com/nalaquq/nunalleq-synth/issues)

## 🗺️ Roadmap

### Current (v0.1.0)
- ✅ Basic physics-based generation
- ✅ YOLO annotation format
- ✅ Docker support
- ✅ Command-line interface

### Upcoming (v0.2.0)
- [ ] COCO annotation format
- [ ] Segmentation masks
- [ ] Advanced material randomization
- [ ] Web-based visualization tool

### Future (v1.0.0)
- [ ] Real-time preview mode
- [ ] Interactive GUI
- [ ] Cloud generation support
- [ ] Integration with training pipelines

## 📊 Citation

If you use this software in your research, please cite:

```bibtex
@software{nunalleq_synth2024,
  title={Nunalleq Synthetic Data Generator},
  author={Native Village of Kwinhagak and Nalaquq, LLC},
  year={2024},
  url={https://github.com/nalaquq/nunalleq-synth},
  version={0.1.0}
}
```

---

**Made with ❤️ for the Yup'ik community in Quinhagak, Alaska**