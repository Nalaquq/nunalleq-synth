
# ============================================================================
# nunalleq_synth/utils/gpu.py
# ============================================================================
"""GPU detection and management utilities."""

import logging
import subprocess
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


def detect_gpu() -> Tuple[bool, Optional[str]]:
    """Detect available GPU and compute capability.
    
    Returns:
        Tuple of (gpu_available, gpu_info).
    """
    try:
        result = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            encoding="utf-8",
        )
        gpu_name = result.strip()
        logger.info(f"NVIDIA GPU detected: {gpu_name}")
        return True, gpu_name
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("No NVIDIA GPU detected")
        return False, None


def enable_gpu() -> bool:
    """Enable GPU acceleration for Blender if available.
    
    Returns:
        True if GPU enabled successfully, False otherwise.
    """
    gpu_available, gpu_info = detect_gpu()
    
    if not gpu_available:
        logger.info("GPU acceleration disabled - using CPU")
        return False
    
    try:
        import bpy
        
        # Set render engine to Cycles
        bpy.context.scene.render.engine = "CYCLES"
        
        # Enable GPU compute
        bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "CUDA"
        bpy.context.scene.cycles.device = "GPU"
        
        # Get devices
        bpy.context.preferences.addons["cycles"].preferences.get_devices()
        
        # Enable all devices
        for device in bpy.context.preferences.addons["cycles"].preferences.devices:
            device.use = True
            logger.debug(f"Enabled device: {device.name}")
        
        logger.info("GPU acceleration enabled for Blender")
        return True
        
    except ImportError:
        logger.warning("Blender (bpy) not available - cannot enable GPU")
        return False
    except Exception as e:
        logger.error(f"Failed to enable GPU: {e}")
        return False

