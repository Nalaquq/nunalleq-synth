# nunalleq_synth/core/physics.py
"""Physics simulation for realistic object placement."""

import logging
from typing import List, Optional, Tuple

import bpy
import numpy as np

logger = logging.getLogger(__name__)


class PhysicsSimulator:
    """Handles physics simulation for object placement.
    
    Attributes:
        gravity: Gravity vector (x, y, z).
        simulation_steps: Number of simulation frames.
        substeps: Substeps per frame for accuracy.
    """
    
    def __init__(
        self,
        gravity: Tuple[float, float, float] = (0.0, 0.0, -9.81),
        simulation_steps: int = 120,
        substeps: int = 10,
    ) -> None:
        """Initialize physics simulator.
        
        Args:
            gravity: Gravity vector as (x, y, z).
            simulation_steps: Number of frames to simulate.
            substeps: Substeps per frame for accuracy.
        """
        self.gravity = gravity
        self.simulation_steps = simulation_steps
        self.substeps = substeps
        
        self._setup_physics()
        logger.info("Physics simulator initialized")
    
    def _setup_physics(self) -> None:
        """Configure Blender physics settings."""
        scene = bpy.context.scene
        scene.gravity = self.gravity
        scene.rigidbody_world.substeps_per_frame = self.substeps
        scene.rigidbody_world.solver_iterations = 10
        
        logger.debug(f"Physics configured: gravity={self.gravity}, steps={self.simulation_steps}")
    
    def add_rigid_body(
        self,
        obj: bpy.types.Object,
        body_type: str = "ACTIVE",
        mass: float = 1.0,
        friction: float = 0.5,
        restitution: float = 0.3,
    ) -> None:
        """Add rigid body physics to an object.
        
        Args:
            obj: Blender object.
            body_type: "ACTIVE" or "PASSIVE".
            mass: Object mass in kg.
            friction: Friction coefficient (0-1).
            restitution: Bounciness (0-1).
        """
        # Select object
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        # Add rigid body
        bpy.ops.rigidbody.object_add()
        obj.rigid_body.type = body_type
        obj.rigid_body.mass = mass
        obj.rigid_body.friction = friction
        obj.rigid_body.restitution = restitution
        
        if body_type == "PASSIVE":
            obj.rigid_body.collision_shape = 'MESH'
        
        logger.debug(f"Added {body_type} rigid body to {obj.name}")
    
    def simulate(
        self,
        start_frame: int = 1,
        end_frame: Optional[int] = None,
    ) -> None:
        """Run physics simulation.
        
        Args:
            start_frame: Starting frame.
            end_frame: Ending frame. If None, uses simulation_steps.
        """
        if end_frame is None:
            end_frame = start_frame + self.simulation_steps
        
        scene = bpy.context.scene
        scene.frame_start = start_frame
        scene.frame_end = end_frame
        
        logger.info(f"Running physics simulation: frames {start_frame}-{end_frame}")
        
        # Run simulation
        for frame in range(start_frame, end_frame + 1):
            scene.frame_set(frame)
        
        # Set to final frame
        scene.frame_set(end_frame)
        logger.debug("Physics simulation complete")
    
    def bake_simulation(self) -> None:
        """Bake physics simulation to keyframes."""
        bpy.ops.ptcache.bake_all(bake=True)
        logger.debug("Physics simulation baked")
    
    def clear_simulation(self) -> None:
        """Clear physics cache."""
        bpy.ops.ptcache.free_bake_all()
        logger.debug("Physics cache cleared")
    
    def drop_object(
        self,
        obj: bpy.types.Object,
        height: float = 1.0,
        location: Tuple[float, float] = (0.0, 0.0),
    ) -> None:
        """Drop object from specified height.
        
        Args:
            obj: Object to drop.
            height: Drop height above surface.
            location: (x, y) location on surface.
        """
        obj.location = (location[0], location[1], height)
        self.add_rigid_body(obj, body_type="ACTIVE")
        logger.debug(f"Dropping {obj.name} from height {height}")
