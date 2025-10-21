# ============================================================================
# nunalleq_synth/randomization/lighting.py
# ============================================================================
"""Lighting randomization."""

import logging
import random
from typing import Tuple

import bpy
import numpy as np

from nunalleq_synth.core.scene import Scene
from nunalleq_synth.pipeline.config import RandomizationConfig

logger = logging.getLogger(__name__)


class LightingRandomizer:
    """Randomizes scene lighting.
    
    Attributes:
        config: Randomization configuration.
    """
    
    def __init__(self, config: RandomizationConfig) -> None:
        """Initialize lighting randomizer.
        
        Args:
            config: Randomization configuration.
        """
        self.config = config
        logger.debug("LightingRandomizer initialized")
    
    def randomize_scene_lighting(self, scene: Scene) -> None:
        """Add randomized lights to scene.
        
        Args:
            scene: Scene to add lights to.
        """
        num_lights = random.randint(2, 4)
        
        for i in range(num_lights):
            # Random light type
            light_type = random.choice(['POINT', 'SUN', 'AREA'])
            
            # Random intensity
            intensity = random.uniform(
                *self.config.lighting_intensity_range
            )
            
            # Random position
            if light_type == 'SUN':
                # Sun lights should be far away
                distance = 10.0
            else:
                distance = random.uniform(2.0, 5.0)
            
            angle = random.uniform(0, 2 * np.pi)
            elevation = random.uniform(np.pi / 6, np.pi / 3)
            
            x = distance * np.cos(angle) * np.sin(elevation)
            y = distance * np.sin(angle) * np.sin(elevation)
            z = distance * np.cos(elevation)
            
            location = (x, y, z)
            
            # Add light
            light = scene.add_light(
                light_type=light_type,
                energy=intensity,
                location=location,
                name=f"Light_{i}",
            )
            
            # Random color temperature
            temp = random.uniform(*self.config.lighting_color_temp_range)
            self._set_color_temperature(light, temp)
        
        logger.debug(f"Added {num_lights} randomized lights")
    
    def _set_color_temperature(
        self,
        light: bpy.types.Object,
        temperature: float,
    ) -> None:
        """Set light color temperature in Kelvin.
        
        Args:
            light: Light object.
            temperature: Color temperature in Kelvin (3000-6500).
        """
        # Convert Kelvin to RGB (simplified)
        if temperature <= 6500:
            r = 1.0
            g = min(1.0, (temperature - 3000) / 3500)
            b = max(0.0, min(1.0, (temperature - 4000) / 2500))
        else:
            r = min(1.0, 1.0 - (temperature - 6500) / 3500)
            g = 1.0
            b = 1.0
        
        light.data.color = (r, g, b)

