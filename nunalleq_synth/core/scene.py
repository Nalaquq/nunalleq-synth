
# ============================================================================
# nunalleq_synth/core/scene.py
# ============================================================================
"""Scene management for Blender."""

import logging
from pathlib import Path
from typing import Optional, List, Tuple

import bpy
import numpy as np

from nunalleq_synth.objects.loader import ObjectLoader
from nunalleq_synth.core.camera import Camera
from nunalleq_synth.core.physics import PhysicsSimulator

logger = logging.getLogger(__name__)


class Scene:
    """Manages Blender scene setup and objects.
    
    Attributes:
        name: Scene name.
        resolution: Image resolution as (width, height).
        camera: Camera instance.
        physics: Physics simulator instance.
    """
    
    def __init__(
        self,
        name: str = "SyntheticScene",
        resolution: Tuple[int, int] = (1920, 1080),
    ) -> None:
        """Initialize scene.
        
        Args:
            name: Scene name.
            resolution: Image resolution as (width, height).
        """
        self.name = name
        self.resolution = resolution
        self._setup_scene()
        
        # Initialize components
        self.camera = Camera()
        self.physics = PhysicsSimulator()
        self.object_loader = ObjectLoader()
        
        logger.info(f"Initialized scene '{name}' at {resolution}")
    
    def _setup_scene(self) -> None:
        """Setup basic Blender scene."""
        # Clear existing scene
        bpy.ops.wm.read_factory_settings(use_empty=True)
        
        # Create new scene
        bpy.ops.scene.new(type='NEW')
        scene = bpy.context.scene
        scene.name = self.name
        
        # Set render settings
        scene.render.resolution_x = self.resolution[0]
        scene.render.resolution_y = self.resolution[1]
        scene.render.resolution_percentage = 100
        scene.render.image_settings.file_format = 'JPEG'
        scene.render.image_settings.quality = 95
        
        # Set up world
        world = bpy.data.worlds.new(name="World")
        scene.world = world
        world.use_nodes = True
        
        logger.debug("Scene setup complete")
    
    def clear(self) -> None:
        """Clear all objects from scene."""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False, confirm=False)
        logger.debug("Scene cleared")
    
    def add_plane(
        self,
        size: float = 10.0,
        location: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        name: str = "Plane",
    ) -> bpy.types.Object:
        """Add a plane to the scene.
        
        Args:
            size: Plane size.
            location: Plane location as (x, y, z).
            name: Object name.
            
        Returns:
            Created plane object.
        """
        bpy.ops.mesh.primitive_plane_add(size=size, location=location)
        plane = bpy.context.active_object
        plane.name = name
        
        logger.debug(f"Added plane '{name}' at {location}")
        return plane
    
    def add_light(
        self,
        light_type: str = "POINT",
        energy: float = 1000.0,
        location: Tuple[float, float, float] = (0.0, 0.0, 5.0),
        name: str = "Light",
    ) -> bpy.types.Object:
        """Add a light to the scene.
        
        Args:
            light_type: Type of light ("POINT", "SUN", "SPOT", "AREA").
            energy: Light intensity.
            location: Light location as (x, y, z).
            name: Light name.
            
        Returns:
            Created light object.
        """
        light_data = bpy.data.lights.new(name=name, type=light_type)
        light_data.energy = energy
        
        light_object = bpy.data.objects.new(name=name, object_data=light_data)
        bpy.context.collection.objects.link(light_object)
        light_object.location = location
        
        logger.debug(f"Added {light_type} light '{name}' at {location}")
        return light_object
    
    def set_background_color(
        self,
        color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
    ) -> None:
        """Set background color.
        
        Args:
            color: RGBA color tuple (values 0-1).
        """
        world = bpy.context.scene.world
        bg = world.node_tree.nodes["Background"]
        bg.inputs[0].default_value = color
        
        logger.debug(f"Set background color to {color}")
    
    def get_all_objects(self) -> List[bpy.types.Object]:
        """Get all objects in the scene.
        
        Returns:
            List of Blender objects.
        """
        return list(bpy.context.scene.objects)