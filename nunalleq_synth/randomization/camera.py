# ============================================================================
# nunalleq_synth/randomization/camera.py
# ============================================================================
"""Camera randomization."""

import logging
import random
from typing import Tuple  # FIXED: Import Tuple from typing

import numpy as np

from nunalleq_synth.core.camera import Camera
from nunalleq_synth.pipeline.config import RandomizationConfig

logger = logging.getLogger(__name__)


class CameraRandomizer:
    """Randomizes camera position and parameters.
    
    Attributes:
        config: Randomization configuration.
    """
    
    def __init__(self, config: RandomizationConfig) -> None:
        """Initialize camera randomizer.
        
        Args:
            config: Randomization configuration.
        """
        self.config = config
        logger.debug("CameraRandomizer initialized")
    
    def randomize_camera(
        self,
        camera: Camera,
        focus_point: Tuple[float, float, float] = (0.0, 0.0, 0.5),  # FIXED: Use Tuple
    ) -> None:
        """Randomize camera position and orientation.
        
        Args:
            camera: Camera to randomize.
            focus_point: Point to focus on (x, y, z).
        """
        # Random distance from focus point
        distance = random.uniform(*self.config.camera_distance_range)
        
        # Random spherical coordinates
        azimuth = random.uniform(0, 2 * np.pi)
        
        # Convert angle range from degrees to radians
        angle_min = np.radians(self.config.camera_angle_range[0])
        angle_max = np.radians(self.config.camera_angle_range[1])
        elevation = random.uniform(
            np.pi / 4 + angle_min,
            np.pi / 4 + angle_max,
        )
        
        # Convert to Cartesian coordinates
        x = focus_point[0] + distance * np.cos(azimuth) * np.sin(elevation)
        y = focus_point[1] + distance * np.sin(azimuth) * np.sin(elevation)
        z = focus_point[2] + distance * np.cos(elevation)
        
        # Set camera position
        camera.set_location((x, y, z))
        
        # Point camera at focus point
        camera.look_at(focus_point)
        
        # Random focal length variation
        base_focal_length = 50.0
        focal_variation = random.uniform(-10.0, 10.0)
        camera.set_focal_length(base_focal_length + focal_variation)
        
        logger.debug(f"Camera randomized: distance={distance:.2f}, azimuth={azimuth:.2f}")