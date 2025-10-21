
# ============================================================================
# nunalleq_synth/annotation/__init__.py
# ============================================================================
"""Annotation generation and format conversion."""

from nunalleq_synth.annotation.bbox import BoundingBoxCalculator, BoundingBox
from nunalleq_synth.annotation.yolo import YOLOAnnotator
from nunalleq_synth.annotation.validation import AnnotationValidator

__all__ = [
    "BoundingBoxCalculator",
    "BoundingBox",
    "YOLOAnnotator",
    "AnnotationValidator",
]

