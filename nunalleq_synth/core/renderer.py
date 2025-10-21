# nunalleq_synth/core/renderer.py
"""Image rendering utilities."""

import logging
from pathlib import Path
from typing import Optional

import bpy

from nunalleq_synth.pipeline.config import RenderConfig
from nunalleq_synth.utils.gpu import enable_gpu

logger = logging.getLogger(__name__)


class Renderer:
    """Handles image rendering in Blender.
    
    Attributes:
        config: Render configuration.
    """
    
    def __init__(self, config: RenderConfig) -> None:
        """Initialize renderer.
        
        Args:
            config: Render configuration.
        """
        self.config = config
        self._setup_renderer()
        logger.info("Renderer initialized")
    
    def _setup_renderer(self) -> None:
        """Configure Blender render settings."""
        scene = bpy.context.scene
        
        # Set render engine
        scene.render.engine = self.config.engine
        
        # Configure Cycles
        if self.config.engine == "CYCLES":
            scene.cycles.samples = self.config.samples
            
            # Enable GPU if requested
            if self.config.use_gpu:
                enable_gpu()
        
        # Set resolution
        scene.render.resolution_x = self.config.resolution[0]
        scene.render.resolution_y = self.config.resolution[1]
        scene.render.resolution_percentage = 100
        
        # Set output format
        scene.render.image_settings.file_format = self.config.file_format
        if self.config.file_format == 'JPEG':
            scene.render.image_settings.quality = self.config.quality
        
        logger.debug(f"Renderer configured: {self.config.engine} @ {self.config.resolution}")
    
    def render(
        self,
        output_path: Path,
        animation: bool = False,
    ) -> bool:
        """Render scene to image file.
        
        Args:
            output_path: Output file path.
            animation: If True, render animation.
            
        Returns:
            True if rendering succeeded, False otherwise.
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Set output path
            bpy.context.scene.render.filepath = str(output_path)
            
            # Render
            if animation:
                bpy.ops.render.render(animation=True, write_still=True)
            else:
                bpy.ops.render.render(write_still=True)
            
            logger.debug(f"Rendered image to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Rendering failed: {e}")
            return False

