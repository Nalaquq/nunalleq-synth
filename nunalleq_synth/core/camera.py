# ============================================================================
# nunalleq_synth/core/camera.py
# ============================================================================
"""Camera management for scene rendering."""

import logging
import math
from typing import Optional, Tuple

import bpy
import numpy as np
from mathutils import Vector  # FIXED: Added import for Vector

logger = logging.getLogger(__name__)


class Camera:
    """Manages camera positioning and properties.
    
    Attributes:
        camera_obj: Blender camera object.
        camera_data: Blender camera data.
    """
    
    def __init__(self, name: str = "Camera") -> None:
        """Initialize camera.
        
        Args:
            name: Camera name.
        """
        self.name = name
        self.camera_obj: Optional[bpy.types.Object] = None
        self.camera_data: Optional[bpy.types.Camera] = None
        
        self._create_camera()
        logger.info(f"Camera '{name}' initialized")
    
    def _create_camera(self) -> None:
        """Create camera object."""
        # Create camera data
        self.camera_data = bpy.data.cameras.new(name=self.name)
        self.camera_data.lens = 50  # 50mm lens
        self.camera_data.sensor_width = 36  # Full frame sensor
        
        # Create camera object
        self.camera_obj = bpy.data.objects.new(name=self.name, object_data=self.camera_data)
        bpy.context.collection.objects.link(self.camera_obj)
        
        # Set as active camera
        bpy.context.scene.camera = self.camera_obj
        
        logger.debug("Camera object created")
    
    def set_location(self, location: Tuple[float, float, float]) -> None:
        """Set camera location.
        
        Args:
            location: Camera location as (x, y, z).
        """
        self.camera_obj.location = location
        logger.debug(f"Camera location set to {location}")
    
    def set_rotation(self, rotation: Tuple[float, float, float]) -> None:
        """Set camera rotation in Euler angles.
        
        Args:
            rotation: Rotation as (x, y, z) in radians.
        """
        self.camera_obj.rotation_euler = rotation
        logger.debug(f"Camera rotation set to {rotation}")
    
    def look_at(self, target: Tuple[float, float, float]) -> None:
        """Point camera at target location.
        
        Args:
            target: Target location as (x, y, z).
        """
        # FIXED: Use mathutils.Vector instead of numpy array
        direction = Vector(target) - Vector(self.camera_obj.location)
        
        # Calculate rotation
        rot_quat = direction.to_track_quat('-Z', 'Y')
        self.camera_obj.rotation_euler = rot_quat.to_euler()
        
        logger.debug(f"Camera looking at {target}")
    
    def add_track_to_constraint(self, target_obj: bpy.types.Object) -> None:
        """Add tracking constraint to follow an object.
        
        Args:
            target_obj: Object to track.
        """
        constraint = self.camera_obj.constraints.new(type='TRACK_TO')
        constraint.target = target_obj
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'
        
        logger.debug(f"Camera tracking {target_obj.name}")
    
    def set_focal_length(self, focal_length: float) -> None:
        """Set camera focal length.
        
        Args:
            focal_length: Focal length in mm.
        """
        self.camera_data.lens = focal_length
        logger.debug(f"Focal length set to {focal_length}mm")
    
    def set_depth_of_field(
        self,
        focus_distance: float,
        aperture_fstop: float = 2.8,
    ) -> None:
        """Enable depth of field effect.
        
        Args:
            focus_distance: Distance to focus point.
            aperture_fstop: F-stop value (lower = more blur).
        """
        self.camera_data.dof.use_dof = True
        self.camera_data.dof.focus_distance = focus_distance
        self.camera_data.dof.aperture_fstop = aperture_fstop
        
        logger.debug(f"DOF enabled: distance={focus_distance}, f-stop={aperture_fstop}")
    
    def get_projection_matrix(self) -> np.ndarray:
        """Get camera projection matrix.
        
        Returns:
            4x4 projection matrix as numpy array.
        """
        render = bpy.context.scene.render
        modelview_matrix = self.camera_obj.matrix_world.inverted()
        projection_matrix = self.camera_obj.calc_matrix_camera(
            bpy.context.evaluated_depsgraph_get(),
            x=render.resolution_x,
            y=render.resolution_y,
            scale_x=render.pixel_aspect_x,
            scale_y=render.pixel_aspect_y,
        )
        
        return np.array(projection_matrix)
    
    def world_to_camera(
        self,
        world_coords: np.ndarray,
    ) -> np.ndarray:
        """Convert world coordinates to camera coordinates.
        
        Args:
            world_coords: World coordinates as (x, y, z).
            
        Returns:
            Camera coordinates.
        """
        # FIXED: Properly compute and return camera coordinates
        camera_matrix = self.camera_obj.matrix_world.inverted()
        # Convert numpy array to Vector for matrix multiplication
        world_vec = Vector(world_coords)
        camera_coords = camera_matrix @ world_vec
        return np.array(camera_coords)