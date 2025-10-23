# ============================================================================
# nunalleq_synth/annotation/bbox.py
# ============================================================================
"""Bounding box calculation from 3D objects."""

import logging
from dataclasses import dataclass
from typing import Optional, Tuple

import bpy
import bpy_extras.object_utils  # FIXED: Added missing import
import numpy as np

from nunalleq_synth.core.camera import Camera

logger = logging.getLogger(__name__)


@dataclass
class BoundingBox:
    """Represents a 2D bounding box.
    
    Attributes:
        x_min: Minimum x coordinate (pixels).
        y_min: Minimum y coordinate (pixels).
        x_max: Maximum x coordinate (pixels).
        y_max: Maximum y coordinate (pixels).
        x_center: Center x coordinate (normalized 0-1).
        y_center: Center y coordinate (normalized 0-1).
        width: Width (normalized 0-1).
        height: Height (normalized 0-1).
        area: Area in pixels.
    """
    x_min: int
    y_min: int
    x_max: int
    y_max: int
    x_center: float
    y_center: float
    width: float
    height: float
    area: int


class BoundingBoxCalculator:
    """Calculates 2D bounding boxes from 3D objects."""
    
    def __init__(self) -> None:
        """Initialize bounding box calculator."""
        logger.debug("BoundingBoxCalculator initialized")
    
    def calculate_bbox(
        self,
        obj: bpy.types.Object,
        camera: Camera,
        resolution: Tuple[int, int],
    ) -> Optional[BoundingBox]:
        """Calculate 2D bounding box for object.
        
        Args:
            obj: Blender object.
            camera: Camera instance.
            resolution: Image resolution (width, height).
            
        Returns:
            BoundingBox or None if object not visible.
        """
        scene = bpy.context.scene
        width, height = resolution
        
        # Get object vertices in world space
        vertices_world = [
            obj.matrix_world @ v.co
            for v in obj.data.vertices
        ]
        
        # Project vertices to camera space
        vertices_2d = []
        depsgraph = bpy.context.evaluated_depsgraph_get()
        
        for v in vertices_world:
            # Convert to camera coordinates
            co_camera = bpy_extras.object_utils.world_to_camera_view(
                scene,
                camera.camera_obj,
                v
            )
            
            # Check if behind camera
            if co_camera.z < 0:
                continue
            
            # Convert to pixel coordinates
            x_pixel = int(co_camera.x * width)
            y_pixel = int((1 - co_camera.y) * height)  # Flip Y
            
            vertices_2d.append((x_pixel, y_pixel))
        
        if not vertices_2d:
            logger.debug(f"Object {obj.name} not visible in camera")
            return None
        
        # Calculate bounding box
        x_coords = [v[0] for v in vertices_2d]
        y_coords = [v[1] for v in vertices_2d]
        
        x_min = max(0, min(x_coords))
        x_max = min(width, max(x_coords))
        y_min = max(0, min(y_coords))
        y_max = min(height, max(y_coords))
        
        # Check if bbox has valid area
        bbox_width = x_max - x_min
        bbox_height = y_max - y_min
        
        if bbox_width <= 0 or bbox_height <= 0:
            return None
        
        # Calculate normalized coordinates
        x_center = (x_min + x_max) / 2 / width
        y_center = (y_min + y_max) / 2 / height
        width_norm = bbox_width / width
        height_norm = bbox_height / height
        area = bbox_width * bbox_height
        
        return BoundingBox(
            x_min=x_min,
            y_min=y_min,
            x_max=x_max,
            y_max=y_max,
            x_center=x_center,
            y_center=y_center,
            width=width_norm,
            height=height_norm,
            area=area,
        )