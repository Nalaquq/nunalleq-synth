
# ============================================================================
# nunalleq_synth/randomization/environment.py
# ============================================================================
"""Environment and background randomization."""

import logging
import random
from typing import Tuple

import bpy

from nunalleq_synth.core.scene import Scene
from nunalleq_synth.pipeline.config import RandomizationConfig

logger = logging.getLogger(__name__)


class EnvironmentRandomizer:
    """Randomizes environment and background.
    
    Attributes:
        config: Randomization configuration.
    """
    
    def __init__(self, config: RandomizationConfig) -> None:
        """Initialize environment randomizer.
        
        Args:
            config: Randomization configuration.
        """
        self.config = config
        logger.debug("EnvironmentRandomizer initialized")
    
    def randomize_background(self, scene: Scene) -> None:
        """Randomize background color.
        
        Args:
            scene: Scene to randomize.
        """
        brightness = random.uniform(
            *self.config.background_brightness_range
        )
        
        # Random color tint
        r = brightness * random.uniform(0.95, 1.0)
        g = brightness * random.uniform(0.95, 1.0)
        b = brightness * random.uniform(0.95, 1.0)
        
        scene.set_background_color((r, g, b, 1.0))
        logger.debug(f"Background color set to ({r:.2f}, {g:.2f}, {b:.2f})")

