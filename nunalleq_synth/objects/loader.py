# ============================================================================
# nunalleq_synth/objects/loader.py
# ============================================================================
"""3D model loading utilities."""

import logging
from pathlib import Path
from typing import Optional, List, Tuple  # FIXED: Import Tuple from typing

import bpy

logger = logging.getLogger(__name__)


class ObjectLoader:
    """Loads 3D models into Blender scene.
    
    Handles loading of .glb files and manages imported objects.
    """
    
    def __init__(self) -> None:
        """Initialize object loader."""
        self.loaded_objects: List[bpy.types.Object] = []
        logger.debug("ObjectLoader initialized")
    
    def load_glb(
        self,
        filepath: Path,
        scale: float = 1.0,
        location: Tuple[float, float, float] = (0.0, 0.0, 0.0),  # FIXED: Use Tuple
    ) -> Optional[bpy.types.Object]:
        """Load a .glb file into the scene.
        
        Args:
            filepath: Path to .glb file.
            scale: Scale factor for the object.
            location: Initial location as (x, y, z).
            
        Returns:
            Loaded Blender object or None if loading failed.
        """
        if not filepath.exists():
            logger.error(f"File not found: {filepath}")
            return None
        
        if filepath.suffix.lower() != '.glb':
            logger.error(f"Not a .glb file: {filepath}")
            return None
        
        try:
            # Import GLB
            bpy.ops.import_scene.gltf(
                filepath=str(filepath),
                loglevel=50,  # ERROR level
            )
            
            # Get imported object
            obj = bpy.context.selected_objects[0]
            obj_name = filepath.stem
            obj.name = obj_name
            
            # Apply transformations
            obj.scale = (scale, scale, scale)
            obj.location = location
            
            # Smooth shading
            bpy.ops.object.shade_smooth()
            
            self.loaded_objects.append(obj)
            logger.info(f"Loaded {obj_name} from {filepath}")
            
            return obj
            
        except Exception as e:
            logger.error(f"Failed to load {filepath}: {e}")
            return None
    
    def load_multiple(
        self,
        directory: Path,
        pattern: str = "*.glb",
    ) -> List[bpy.types.Object]:
        """Load multiple .glb files from directory.
        
        Args:
            directory: Directory containing .glb files.
            pattern: File pattern to match.
            
        Returns:
            List of loaded objects.
        """
        glb_files = sorted(directory.glob(pattern))
        logger.info(f"Found {len(glb_files)} files matching '{pattern}'")
        
        loaded = []
        for glb_file in glb_files:
            obj = self.load_glb(glb_file)
            if obj:
                loaded.append(obj)
        
        logger.info(f"Successfully loaded {len(loaded)}/{len(glb_files)} objects")
        return loaded
    
    def remove_object(self, obj: bpy.types.Object) -> None:
        """Remove object from scene.
        
        Args:
            obj: Object to remove.
        """
        bpy.data.objects.remove(obj, do_unlink=True)
        if obj in self.loaded_objects:
            self.loaded_objects.remove(obj)
        logger.debug(f"Removed object {obj.name}")
    
    def clear_all(self) -> None:
        """Remove all loaded objects from scene."""
        for obj in self.loaded_objects[:]:
            self.remove_object(obj)
        logger.debug("Cleared all loaded objects")