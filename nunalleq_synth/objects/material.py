# ============================================================================
# nunalleq_synth/objects/material.py
# ============================================================================
"""Material management utilities."""

import logging
import random
from typing import Tuple  # FIXED: Import Tuple from typing

import bpy

logger = logging.getLogger(__name__)


class MaterialManager:
    """Manages object materials and textures."""
    
    @staticmethod
    def create_material(
        name: str,
        color: Tuple[float, float, float, float] = (0.8, 0.8, 0.8, 1.0),  # FIXED: Use Tuple
        metallic: float = 0.0,
        roughness: float = 0.5,
    ) -> bpy.types.Material:
        """Create a new material.
        
        Args:
            name: Material name.
            color: RGBA color (0-1).
            metallic: Metallic value (0-1).
            roughness: Roughness value (0-1).
            
        Returns:
            Created material.
        """
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        
        # Get principled BSDF node
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = color
            bsdf.inputs['Metallic'].default_value = metallic
            bsdf.inputs['Roughness'].default_value = roughness
        
        logger.debug(f"Created material: {name}")
        return mat
    
    @staticmethod
    def assign_material(
        obj: bpy.types.Object,
        material: bpy.types.Material,
    ) -> None:
        """Assign material to object.
        
        Args:
            obj: Blender object.
            material: Material to assign.
        """
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)
        
        logger.debug(f"Assigned material {material.name} to {obj.name}")
    
    @staticmethod
    def randomize_material_properties(
        obj: bpy.types.Object,
        color_variation: float = 0.1,
        roughness_variation: float = 0.2,
    ) -> None:
        """Randomize material properties of an object.
        
        Args:
            obj: Blender object.
            color_variation: Amount of color variation (0-1).
            roughness_variation: Amount of roughness variation (0-1).
        """
        if not obj.data.materials:
            return
        
        mat = obj.data.materials[0]
        if not mat.use_nodes:
            return
        
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if not bsdf:
            return
        
        # Randomize color
        base_color = bsdf.inputs['Base Color'].default_value
        new_color = [
            max(0, min(1, c + random.uniform(-color_variation, color_variation)))
            for c in base_color[:3]
        ]
        new_color.append(base_color[3])  # Keep alpha
        bsdf.inputs['Base Color'].default_value = new_color
        
        # Randomize roughness
        base_roughness = bsdf.inputs['Roughness'].default_value
        new_roughness = max(
            0,
            min(1, base_roughness + random.uniform(-roughness_variation, roughness_variation))
        )
        bsdf.inputs['Roughness'].default_value = new_roughness
        
        logger.debug(f"Randomized material for {obj.name}")