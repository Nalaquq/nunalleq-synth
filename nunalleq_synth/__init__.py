"""Nunalleq Synthetic Data Generator."""
from nunalleq_synth.__version__ import __version__
from nunalleq_synth.pipeline.generator import SyntheticGenerator
from nunalleq_synth.pipeline.config import GenerationConfig

__all__ = ["__version__", "SyntheticGenerator", "GenerationConfig"]
