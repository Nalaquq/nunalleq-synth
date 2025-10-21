
# ============================================================================
# nunalleq_synth/annotation/yolo.py
# ============================================================================
"""YOLO format annotation generation."""

import logging
from pathlib import Path
from typing import List, Tuple

from nunalleq_synth.annotation.bbox import BoundingBox

logger = logging.getLogger(__name__)


class YOLOAnnotator:
    """Generates YOLO format annotations.
    
    YOLO format: <class_id> <x_center> <y_center> <width> <height>
    All values normalized to [0, 1] except class_id.
    
    Attributes:
        class_names: List of class names.
    """
    
    def __init__(self, class_names: List[str]) -> None:
        """Initialize YOLO annotator.
        
        Args:
            class_names: List of class names.
        """
        self.class_names = class_names
        logger.debug(f"YOLOAnnotator initialized with {len(class_names)} classes")
    
    def save_annotations(
        self,
        annotations: List[Tuple[int, BoundingBox]],
        output_path: Path,
        resolution: Tuple[int, int],
    ) -> bool:
        """Save annotations in YOLO format.
        
        Args:
            annotations: List of (class_id, bbox) tuples.
            output_path: Output file path.
            resolution: Image resolution (width, height).
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                for class_id, bbox in annotations:
                    # YOLO format line
                    line = (
                        f"{class_id} "
                        f"{bbox.x_center:.6f} "
                        f"{bbox.y_center:.6f} "
                        f"{bbox.width:.6f} "
                        f"{bbox.height:.6f}\n"
                    )
                    f.write(line)
            
            logger.debug(f"Saved {len(annotations)} annotations to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save annotations: {e}")
            return False
