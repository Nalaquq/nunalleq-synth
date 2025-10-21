
# ============================================================================
# nunalleq_synth/utils/io.py
# ============================================================================
"""File I/O utilities."""

import logging
from pathlib import Path
from typing import List, Optional, Union

import cv2
import numpy as np

logger = logging.getLogger(__name__)


def ensure_dir(path: Union[str, Path]) -> Path:
    """Ensure directory exists, create if it doesn't.
    
    Args:
        path: Directory path.
        
    Returns:
        Path object for the directory.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def list_files(
    directory: Union[str, Path],
    pattern: str = "*",
    recursive: bool = False,
) -> List[Path]:
    """List files in directory matching pattern.
    
    Args:
        directory: Directory to search.
        pattern: Glob pattern to match (e.g., "*.glb").
        recursive: If True, search recursively.
        
    Returns:
        List of matching file paths.
    """
    directory = Path(directory)
    
    if not directory.exists():
        logger.warning(f"Directory does not exist: {directory}")
        return []
    
    if recursive:
        files = list(directory.rglob(pattern))
    else:
        files = list(directory.glob(pattern))
    
    logger.debug(f"Found {len(files)} files matching '{pattern}' in {directory}")
    return sorted(files)


def save_image(
    image: np.ndarray,
    path: Union[str, Path],
    quality: int = 95,
) -> bool:
    """Save image to disk.
    
    Args:
        image: Image array (RGB or BGR format).
        path: Output path.
        quality: JPEG quality (0-100).
        
    Returns:
        True if successful, False otherwise.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Convert RGB to BGR for OpenCV
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        else:
            image_bgr = image
        
        success = cv2.imwrite(
            str(path),
            image_bgr,
            [cv2.IMWRITE_JPEG_QUALITY, quality],
        )
        
        if success:
            logger.debug(f"Saved image to {path}")
        else:
            logger.error(f"Failed to save image to {path}")
        
        return success
        
    except Exception as e:
        logger.error(f"Error saving image to {path}: {e}")
        return False


def load_image(
    path: Union[str, Path],
    color_mode: str = "RGB",
) -> Optional[np.ndarray]:
    """Load image from disk.
    
    Args:
        path: Image path.
        color_mode: Color mode - "RGB", "BGR", or "GRAY".
        
    Returns:
        Image array or None if loading failed.
    """
    path = Path(path)
    
    if not path.exists():
        logger.error(f"Image file does not exist: {path}")
        return None
    
    try:
        if color_mode == "GRAY":
            image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        else:
            image = cv2.imread(str(path))
            if color_mode == "RGB" and image is not None:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        if image is None:
            logger.error(f"Failed to load image: {path}")
        else:
            logger.debug(f"Loaded image from {path}")
        
        return image
        
    except Exception as e:
        logger.error(f"Error loading image from {path}: {e}")
        return None

