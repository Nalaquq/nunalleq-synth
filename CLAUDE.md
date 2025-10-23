# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Nunalleq Synthetic Data Generator is a physics-based synthetic data generation tool for training YOLO object detection models on Yup'ik cultural artifacts using Blender. The project supports the Nunalleq Museum Digital Guide by enabling real-time artifact recognition.

**Key Context**: This project handles Yup'ik cultural artifacts. Treat the work with cultural respect and care. Generated data is for educational and museum purposes only.

## Build and Development Commands

### Installation
```bash
# Install package in development mode (includes Blender + dev tools)
make install-dev

# Or manually
pip install -e ".[all]"         # Everything (Blender + dev tools)
pip install -e ".[blender]"     # Just Blender support (for production)
pip install -e ".[dev]"         # Dev tools only (no Blender)
pip install -e .                # Core deps only (no Blender, no dev tools)

# After installation with dev tools
pre-commit install
```

**Important**: Blender (bpy) is now an optional dependency. For actual data generation, you need `[blender]` or `[all]`. If bpy installation fails, use Docker or install system Blender.

### Testing
```bash
# Run all tests
make test
pytest tests/

# Run tests with coverage
make test-cov

# Run a single test file
pytest tests/test_core/test_scene.py -v

# Run specific test
pytest tests/test_pipeline/test_generator.py::TestSyntheticGenerator::test_generate -v
```

### Code Quality
```bash
# Format code (black + isort)
make format

# Run linters (flake8 + pylint)
make lint

# Type checking (mypy)
make type-check

# Run all quality checks before committing
make format && make lint && make type-check && make test
```

### Running the Generator
```bash
# Basic generation
nunalleq-synth generate --models ./models/ulus --output ./output --num-images 1000

# Use config file
nunalleq-synth generate --config configs/high_quality.yaml

# With custom resolution
nunalleq-synth generate --models ./models --output ./output --resolution 2560 1440

# Python API
python -c "from pathlib import Path; from nunalleq_synth import SyntheticGenerator, GenerationConfig; config = GenerationConfig(model_dir=Path('models'), output_dir=Path('output')); SyntheticGenerator(config).generate()"
```

### Docker
```bash
# Build Docker image
make docker-build

# Run with docker-compose
make docker-run

# Development container
make docker-dev
```

## Architecture Overview

### Pipeline Flow
The generation pipeline follows this flow:
1. **Config Loading** (`pipeline/config.py`) - Load YAML config or use defaults
2. **Model Discovery** (`objects/loader.py`) - Scan directories for .glb files
3. **Scene Setup** (`core/scene.py`) - Initialize Blender scene with ground plane
4. **Randomization** (`randomization/`) - Apply domain randomization to lighting, camera, materials
5. **Physics Simulation** (`core/physics.py`) - Drop objects and simulate physics for realistic placement
6. **Rendering** (`core/renderer.py`) - Render image using Blender (CYCLES or EEVEE)
7. **Annotation** (`annotation/`) - Calculate bounding boxes and save in YOLO format

### Module Structure
```
nunalleq_synth/
├── core/              # Core Blender functionality
│   ├── scene.py       # Scene management, object placement
│   ├── physics.py     # Physics simulation (rigid bodies, gravity)
│   ├── renderer.py    # Image rendering (GPU/CPU, CYCLES/EEVEE)
│   └── camera.py      # Camera management
├── objects/           # 3D model handling
│   ├── loader.py      # Load .glb files into Blender
│   ├── material.py    # Material and texture management
│   └── transform.py   # Object transformations
├── randomization/     # Domain randomization
│   ├── lighting.py    # Light intensity, color temperature
│   ├── camera.py      # Camera position, angle, FOV
│   └── environment.py # Background, materials
├── annotation/        # Annotation generation
│   ├── bbox.py        # Bounding box calculation from 3D to 2D
│   ├── yolo.py        # YOLO format writer
│   └── validation.py  # Annotation validation
├── pipeline/          # Main pipeline
│   ├── generator.py   # SyntheticGenerator orchestrates everything
│   ├── config.py      # Pydantic configs (GenerationConfig, PhysicsConfig, etc.)
│   └── batch.py       # Batch processing multiple directories
└── utils/             # Utilities
    ├── logger.py      # Logging setup
    ├── gpu.py         # GPU detection and setup
    └── io.py          # File I/O helpers
```

### Key Classes

**SyntheticGenerator** (`pipeline/generator.py`): Main orchestrator
- `generate()` - Generate complete dataset (train/test/val splits)
- `generate_single_image()` - Generate one image with annotations
- `_setup_scene()` - Clear scene, add ground plane, setup lighting
- `_place_objects()` - Load models, drop with physics, simulate

**Scene** (`core/scene.py`): Blender scene wrapper
- Manages Blender scene state
- Provides high-level API for adding planes, lights
- Integrates with Camera and PhysicsSimulator

**GenerationConfig** (`pipeline/config.py`): Pydantic configuration
- Hierarchical config: PhysicsConfig, RenderConfig, RandomizationConfig, AnnotationConfig
- Load from YAML: `load_config(path)`
- All configs use Pydantic for validation

### Configuration System

Configs use Pydantic models with nested structure:
- `GenerationConfig` - Top-level config
  - `PhysicsConfig` - gravity, simulation_steps, friction, restitution
  - `RenderConfig` - engine (CYCLES/EEVEE), samples, resolution, GPU usage
  - `RandomizationConfig` - ranges for lighting, camera, scaling
  - `AnnotationConfig` - format (yolo/coco), min_visibility, class_names

Load from YAML or create programmatically. See `configs/default.yaml` for examples.

### Dataset Structure

Generated datasets follow YOLO format:
```
output/
├── train/
│   ├── images/          # train_000000.jpg, train_000001.jpg, ...
│   └── labels/          # train_000000.txt, train_000001.txt, ...
├── test/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
├── classes.txt          # Class names (one per line)
└── config.yaml          # Generation config used
```

YOLO annotation format: `<class_id> <x_center> <y_center> <width> <height>` (normalized to [0,1])

### Model Directory Structure

Organize 3D models with directory names as class labels:
```
models/
├── ulus/           # Class name becomes label
│   ├── ulu_001.glb
│   └── ulu_002.glb
├── masks/
│   └── mask_001.glb
└── dolls/
    └── doll_001.glb
```

**Important**: Directory names become class labels in annotations.

## Development Workflow

### Adding New Features

1. **New randomization parameter**: Add to `RandomizationConfig` in `pipeline/config.py`, then implement in appropriate randomizer (`randomization/lighting.py`, etc.)

2. **New annotation format**: Create new annotator in `annotation/`, inherit pattern from `yolo.py`, update `AnnotationConfig.format` validator

3. **New render engine features**: Modify `Renderer` in `core/renderer.py`, update `RenderConfig`

### Testing Strategy

- Unit tests for individual components (`test_core/`, `test_pipeline/`)
- Use `conftest.py` for shared fixtures
- Mock Blender (`bpy`) when not testing rendering
- Integration tests should use small model files in `tests/fixtures/`

### Type Hints

All code uses type hints (enforced by mypy):
- Functions must have parameter and return type annotations
- Use `typing` module for complex types (List, Dict, Tuple, Optional)
- Pydantic models handle validation

### Blender Integration

This project uses Blender as a Python module (`bpy`):
- Blender must be installed and accessible to Python
- GPU rendering requires CUDA/OptiX (NVIDIA) or HIP (AMD)
- Scene state persists between operations - always clear when needed
- Use `bpy.ops` sparingly; prefer direct `bpy.data` access

## Common Issues

### Blender Not Found
If you see `ModuleNotFoundError: No module named 'bpy'`:
- Install Blender: `pip install bpy>=3.6.0`
- Or use system Blender and point Python to it
- Linux: Run `scripts/setup_blender.sh`

### GPU Not Detected
Check GPU availability: `from nunalleq_synth.utils.gpu import check_gpu; check_gpu()`
- Ensure CUDA drivers are installed
- Blender requires compatible GPU (see Blender docs)

### Physics Simulation Issues
If objects fall through ground or behave oddly:
- Increase `simulation_steps` in PhysicsConfig (default 120)
- Adjust `friction` and `restitution` values
- Check object scales (very small/large objects can cause issues)

## Code Style

- **Black** for formatting (line length 88)
- **isort** for import sorting (black profile)
- **Google-style docstrings**
- **PEP 8** compliance
- Pre-commit hooks enforce style automatically

## External References

- **Blender Python API**: https://docs.blender.org/api/current/
- **YOLO Format**: https://docs.ultralytics.com/datasets/detect/
- **Project Website**: https://www.nunalleq.org
- **Documentation**: https://nunalleq-synth.readthedocs.io
