# nunalleq_synth/pipeline/config.py
"""Configuration management for synthetic data generation."""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

import yaml
from pydantic import BaseModel, Field, validator

logger = logging.getLogger(__name__)


class PhysicsConfig(BaseModel):
    """Physics simulation configuration."""
    
    gravity: Tuple[float, float, float] = Field(
        default=(0.0, 0.0, -9.81),
        description="Gravity vector (x, y, z)",
    )
    simulation_steps: int = Field(
        default=120,
        ge=1,
        description="Number of simulation frames",
    )
    substeps: int = Field(
        default=10,
        ge=1,
        description="Substeps per frame for accuracy",
    )
    friction: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Default friction coefficient",
    )
    restitution: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Default bounciness",
    )


class RenderConfig(BaseModel):
    """Rendering configuration."""
    
    engine: str = Field(
        default="CYCLES",
        description="Render engine (CYCLES or EEVEE)",
    )
    samples: int = Field(
        default=128,
        ge=1,
        description="Number of render samples",
    )
    use_gpu: bool = Field(
        default=True,
        description="Use GPU acceleration if available",
    )
    resolution: Tuple[int, int] = Field(
        default=(1920, 1080),
        description="Image resolution (width, height)",
    )
    file_format: str = Field(
        default="JPEG",
        description="Output image format",
    )
    quality: int = Field(
        default=95,
        ge=0,
        le=100,
        description="Image quality (for JPEG)",
    )
    
    @validator('engine')
    def validate_engine(cls, v: str) -> str:
        """Validate render engine."""
        if v not in ['CYCLES', 'EEVEE']:
            raise ValueError("engine must be 'CYCLES' or 'EEVEE'")
        return v


class RandomizationConfig(BaseModel):
    """Domain randomization configuration."""
    
    lighting_intensity_range: Tuple[float, float] = Field(
        default=(500.0, 2000.0),
        description="Light intensity range (min, max)",
    )
    lighting_color_temp_range: Tuple[float, float] = Field(
        default=(3000.0, 6500.0),
        description="Light color temperature range (min, max)",
    )
    camera_distance_range: Tuple[float, float] = Field(
        default=(0.5, 2.0),
        description="Camera distance range (min, max)",
    )
    camera_angle_range: Tuple[float, float] = Field(
        default=(-30.0, 30.0),
        description="Camera angle range in degrees (min, max)",
    )
    object_scale_range: Tuple[float, float] = Field(
        default=(0.8, 1.2),
        description="Object scale randomization range (min, max)",
    )
    background_brightness_range: Tuple[float, float] = Field(
        default=(0.7, 1.0),
        description="Background brightness range (min, max)",
    )


class AnnotationConfig(BaseModel):
    """Annotation configuration."""
    
    format: str = Field(
        default="yolo",
        description="Annotation format (yolo, coco, pascal_voc)",
    )
    min_visibility: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Minimum object visibility to include",
    )
    min_bbox_area: int = Field(
        default=100,
        ge=1,
        description="Minimum bounding box area in pixels",
    )
    class_names: list[str] = Field(
        default_factory=list,
        description="List of class names for objects",
    )
    
    @validator('format')
    def validate_format(cls, v: str) -> str:
        """Validate annotation format."""
        if v not in ['yolo', 'coco', 'pascal_voc']:
            raise ValueError("format must be 'yolo', 'coco', or 'pascal_voc'")
        return v


class GenerationConfig(BaseModel):
    """Main configuration for synthetic data generation."""
    
    # Paths
    model_dir: Path = Field(
        ...,
        description="Directory containing 3D models (.glb files)",
    )
    output_dir: Path = Field(
        ...,
        description="Output directory for generated dataset",
    )
    
    # Generation parameters
    num_images: int = Field(
        default=1000,
        ge=1,
        description="Total number of images to generate",
    )
    train_test_val_split: Tuple[float, float, float] = Field(
        default=(0.8, 0.1, 0.1),
        description="Dataset split ratios (train, test, val)",
    )
    max_objects_per_scene: int = Field(
        default=3,
        ge=1,
        description="Maximum number of objects per scene",
    )
    random_seed: Optional[int] = Field(
        default=None,
        description="Random seed for reproducibility",
    )
    
    # Sub-configurations
    physics: PhysicsConfig = Field(
        default_factory=PhysicsConfig,
        description="Physics simulation settings",
    )
    render: RenderConfig = Field(
        default_factory=RenderConfig,
        description="Rendering settings",
    )
    randomization: RandomizationConfig = Field(
        default_factory=RandomizationConfig,
        description="Domain randomization settings",
    )
    annotation: AnnotationConfig = Field(
        default_factory=AnnotationConfig,
        description="Annotation settings",
    )
    
    @validator('train_test_val_split')
    def validate_split(cls, v: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Validate dataset split ratios sum to 1.0."""
        if not abs(sum(v) - 1.0) < 1e-6:
            raise ValueError("train_test_val_split must sum to 1.0")
        return v
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True


def load_config(config_path: Path) -> GenerationConfig:
    """Load configuration from YAML file.
    
    Args:
        config_path: Path to YAML configuration file.
        
    Returns:
        GenerationConfig instance.
        
    Raises:
        FileNotFoundError: If config file doesn't exist.
        ValueError: If config is invalid.
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    logger.info(f"Loading configuration from {config_path}")
    
    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    
    config = GenerationConfig(**config_dict)
    logger.info("Configuration loaded successfully")
    
    return config


def save_config(config: GenerationConfig, output_path: Path) -> None:
    """Save configuration to YAML file.
    
    Args:
        config: Configuration to save.
        output_path: Output file path.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    config_dict = config.dict()
    
    with open(output_path, 'w') as f:
        yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)
    
    logger.info(f"Configuration saved to {output_path}")

