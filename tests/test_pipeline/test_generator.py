# tests/test_pipeline/test_generator.py
"""Tests for pipeline generator."""

import pytest
from pathlib import Path
from nunalleq_synth.pipeline.generator import SyntheticGenerator


def test_generator_initialization(sample_config, mock_blender):
    """Test generator initialization."""
    generator = SyntheticGenerator(sample_config)
    
    assert generator.config == sample_config
    assert generator.scene is not None
    assert generator.physics is not None


def test_split_counts(sample_config):
    """Test dataset split calculation."""
    generator = SyntheticGenerator(sample_config)
    
    train, test, val = generator._get_split_counts()
    
    assert train + test + val == sample_config.num_images
    assert train == 8  # 80% of 10
    assert test == 1   # 10% of 10
    assert val == 1    # 10% of 10