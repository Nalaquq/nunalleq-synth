
# ============================================================================
# nunalleq_synth/annotation/validation.py
# ============================================================================
"""Annotation validation utilities."""

import logging
from pathlib import Path
from typing import List, Tuple

from nunalleq_synth.annotation.bbox import BoundingBox

logger = logging.getLogger(__name__)


class AnnotationValidator:
    """Validates generated annotations."""
    
    def __init__(self) -> None:
        """Initialize annotation validator."""
        logger.debug("AnnotationValidator initialized")
    
    def validate_bbox(
        self,
        bbox: BoundingBox,
        min_area: int = 100,
        min_visibility: float = 0.3,
    ) -> bool:
        """Validate bounding box.
        
        Args:
            bbox: Bounding box to validate.
            min_area: Minimum area in pixels.
            min_visibility: Minimum visibility ratio (0-1).
            
        Returns:
            True if valid, False otherwise.
        """
        # Check minimum area
        if bbox.area < min_area:
            logger.debug(f"BBox rejected: area {bbox.area} < {min_area}")
            return False
        
        # Check if within image bounds
        if not (0 <= bbox.x_center <= 1 and 0 <= bbox.y_center <= 1):
            logger.debug("BBox rejected: center out of bounds")
            return False
        
        if not (0 < bbox.width <= 1 and 0 < bbox.height <= 1):
            logger.debug("BBox rejected: dimensions out of bounds")
            return False
        
        return True
    
    def validate_dataset(
        self,
        dataset_dir: Path,
    ) -> Tuple[int, int, List[str]]:
        """Validate a complete dataset.
        
        Args:
            dataset_dir: Root directory of dataset.
            
        Returns:
            Tuple of (valid_count, invalid_count, error_messages).
        """
        valid_count = 0
        invalid_count = 0
        errors = []
        
        for split in ['train', 'test', 'val']:
            images_dir = dataset_dir / split / 'images'
            labels_dir = dataset_dir / split / 'labels'
            
            if not images_dir.exists() or not labels_dir.exists():
                errors.append(f"Missing directories for {split} split")
                continue
            
            image_files = sorted(images_dir.glob('*.jpg'))
            
            for img_file in image_files:
                label_file = labels_dir / f"{img_file.stem}.txt"
                
                if not label_file.exists():
                    errors.append(f"Missing label file: {label_file}")
                    invalid_count += 1
                    continue
                
                # Validate label file
                try:
                    with open(label_file, 'r') as f:
                        lines = f.readlines()
                    
                    if not lines:
                        errors.append(f"Empty label file: {label_file}")
                        invalid_count += 1
                        continue
                    
                    # Parse and validate each annotation
                    for line in lines:
                        parts = line.strip().split()
                        if len(parts) != 5:
                            errors.append(
                                f"Invalid format in {label_file}: {line.strip()}"
                            )
                            invalid_count += 1
                            break
                        
                        # Check if values are valid
                        try:
                            class_id = int(parts[0])
                            x_center = float(parts[1])
                            y_center = float(parts[2])
                            width = float(parts[3])
                            height = float(parts[4])
                            
                            if not (0 <= x_center <= 1 and 0 <= y_center <= 1):
                                errors.append(
                                    f"Invalid coordinates in {label_file}"
                                )
                                invalid_count += 1
                                break
                            
                            if not (0 < width <= 1 and 0 < height <= 1):
                                errors.append(
                                    f"Invalid dimensions in {label_file}"
                                )
                                invalid_count += 1
                                break
                        
                        except ValueError:
                            errors.append(
                                f"Non-numeric values in {label_file}"
                            )
                            invalid_count += 1
                            break
                    else:
                        valid_count += 1
                
                except Exception as e:
                    errors.append(f"Error reading {label_file}: {e}")
                    invalid_count += 1
        
        logger.info(f"Validation complete: {valid_count} valid, {invalid_count} invalid")
        return valid_count, invalid_count, errors