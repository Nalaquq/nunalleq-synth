
# ============================================================================
# nunalleq_synth/objects/transform.py
# ============================================================================
"""Object transformation utilities."""

import logging
from typing import Tuple

import bpy
import numpy as np

logger = logging.getLogger(__name__)


class ObjectTransform:
    """Handles object transformations in Blender."""
    
    @staticmethod
    def set_location(
        obj: bpy.types.Object,
        location: Tuple[float, float, float],
    ) -> None:
        """Set object location.
        
        Args:
            obj: Blender object.
            location: New location as (x, y, z).
        """
        obj.location = location
        logger.debug(f"Set {obj.name} location to {location}")
    
    @staticmethod
    def set_rotation(
        obj: bpy.types.Object,
        rotation: Tuple[float, float, float],
        mode: str = 'XYZ',
    ) -> None:
        """Set object rotation.
        
        Args:
            obj: Blender object.
            rotation: Rotation in radians as (x, y, z).
            mode: Rotation mode (XYZ, XZY, YXZ, YZX, ZXY, ZYX).
        """
        obj.rotation_mode = mode
        obj.rotation_euler = rotation
        logger.debug(f"Set {obj.name} rotation to {rotation}")
    
    @staticmethod
    def set_scale(
        obj: bpy.types.Object,
        scale: Tuple[float, float, float],
    ) -> None:
        """Set object scale.
        
        Args:
            obj: Blender object.
            scale: Scale factors as (x, y, z).
        """
        obj.scale = scale
        logger.debug(f"Set {obj.name} scale to {scale}")
    
    @staticmethod
    def random_rotation(
        obj: bpy.types.Object,
        x_range: Tuple[float, float] = (-np.pi, np.pi),
        y_range: Tuple[float, float] = (-np.pi, np.pi),
        z_range: Tuple[float, float] = (-np.pi, np.pi),
    ) -> None:
        """Apply random rotation to object.
        
        Args:
            obj: Blender object.
            x_range: X rotation range in radians.
            y_range: Y rotation range in radians.
            z_range: Z rotation range in radians.
        """
        rx = np.random.uniform(*x_range)
        ry = np.random.uniform(*y_range)
        rz = np.random.uniform(*z_range)
        
        ObjectTransform.set_rotation(obj, (rx, ry, rz))
