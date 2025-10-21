# ============================================================================
# tests/test_core/test_scene.py
# ============================================================================
"""Tests for scene management."""

import pytest
from nunalleq_synth.core.scene import Scene


def test_scene_initialization(mock_blender):
    """Test scene initialization."""
    scene = Scene(name="TestScene", resolution=(1920, 1080))
    
    assert scene.name == "TestScene"
    assert scene.resolution == (1920, 1080)
    assert scene.camera is not None
    assert scene.physics is not None


def test_scene_clear(mock_blender):
    """Test scene clearing."""
    scene = Scene()
    scene.clear()
    
    # Verify clear was called
    mock_blender.ops.object.select_all.assert_called()# ============================================================================
# tests/test_core/test_scene.py
# ============================================================================
"""Tests for scene management."""

import pytest
from nunalleq_synth.core.scene import Scene


def test_scene_initialization(mock_blender):
    """Test scene initialization."""
    scene = Scene(name="TestScene", resolution=(1920, 1080))
    
    assert scene.name == "TestScene"
    assert scene.resolution == (1920, 1080)
    assert scene.camera is not None
    assert scene.physics is not None


def test_scene_clear(mock_blender):
    """Test scene clearing."""
    scene = Scene()
    scene.clear()
    
    # Verify clear was called
    mock_blender.ops.object.select_all.assert_called()