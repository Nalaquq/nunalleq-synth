# ============================================================================
# tests/conftest.py
# ============================================================================

"""Pytest configuration and fixtures."""  # FIXED

import pytest
from pathlib import Path
import tempfile
import shutil

from nunalleq_synth.pipeline.config import GenerationConfig


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests."""
    tmpdir = Path(tempfile.mkdtemp())
    yield tmpdir
    shutil.rmtree(tmpdir)


@pytest.fixture
def sample_config(temp_dir):
    """Create sample configuration for testing."""
    model_dir = temp_dir / "models"
    output_dir = temp_dir / "output"
    model_dir.mkdir()
    output_dir.mkdir()
    
    config = GenerationConfig(
        model_dir=model_dir,
        output_dir=output_dir,
        num_images=10,
        max_objects_per_scene=2,
        random_seed=42,
    )
    
    return config


@pytest.fixture
def mock_blender(monkeypatch):
    """Mock Blender imports for testing without Blender."""
    import sys
    from unittest.mock import MagicMock
    
    # Create mock bpy module
    mock_bpy = MagicMock()
    sys.modules['bpy'] = mock_bpy
    
    yield mock_bpy
    
    # Cleanup
    if 'bpy' in sys.modules:
        del sys.modules['bpy']