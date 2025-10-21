
# ============================================================================
# nunalleq_synth/pipeline/generator.py
# ============================================================================
"""Main synthetic data generation pipeline."""

import logging
import random
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
from tqdm import tqdm

from nunalleq_synth.core.scene import Scene
from nunalleq_synth.core.physics import PhysicsSimulator
from nunalleq_synth.core.renderer import Renderer
from nunalleq_synth.core.camera import Camera
from nunalleq_synth.objects.loader import ObjectLoader
from nunalleq_synth.randomization.lighting import LightingRandomizer
from nunalleq_synth.randomization.camera import CameraRandomizer
from nunalleq_synth.annotation.bbox import BoundingBoxCalculator
from nunalleq_synth.annotation.yolo import YOLOAnnotator
from nunalleq_synth.pipeline.config import GenerationConfig
from nunalleq_synth.utils.io import ensure_dir, list_files

logger = logging.getLogger(__name__)


class SyntheticGenerator:
    """Main pipeline for generating synthetic training data.
    
    Attributes:
        config: Generation configuration.
        scene: Blender scene manager.
        physics: Physics simulator.
        renderer: Image renderer.
        object_loader: 3D object loader.
        bbox_calculator: Bounding box calculator.
        annotator: Annotation writer.
    """
    
    def __init__(self, config: GenerationConfig) -> None:
        """Initialize synthetic data generator.
        
        Args:
            config: Generation configuration.
        """
        self.config = config
        
        # Set random seed
        if config.random_seed is not None:
            random.seed(config.random_seed)
            np.random.seed(config.random_seed)
            logger.info(f"Random seed set to {config.random_seed}")
        
        # Initialize components
        self._initialize_components()
        
        # Load models
        self.model_files = self._discover_models()
        logger.info(f"Found {len(self.model_files)} 3D models")
        
        # Setup output directories
        self._setup_output_dirs()
    
    def _initialize_components(self) -> None:
        """Initialize all pipeline components."""
        logger.info("Initializing pipeline components...")
        
        self.scene = Scene(
            name="SyntheticScene",
            resolution=self.config.render.resolution,
        )
        
        self.physics = PhysicsSimulator(
            gravity=self.config.physics.gravity,
            simulation_steps=self.config.physics.simulation_steps,
            substeps=self.config.physics.substeps,
        )
        
        self.renderer = Renderer(self.config.render)
        self.object_loader = ObjectLoader()
        
        self.lighting_randomizer = LightingRandomizer(
            self.config.randomization,
        )
        
        self.camera_randomizer = CameraRandomizer(
            self.config.randomization,
        )
        
        self.bbox_calculator = BoundingBoxCalculator()
        
        self.annotator = YOLOAnnotator(
            class_names=self.config.annotation.class_names,
        )
        
        logger.info("Pipeline components initialized")
    
    def _discover_models(self) -> List[Path]:
        """Discover 3D models in model directory.
        
        Returns:
            List of paths to .glb files.
        """
        model_files = list_files(
            self.config.model_dir,
            pattern="*.glb",
            recursive=True,
        )
        
        if not model_files:
            logger.warning(f"No .glb files found in {self.config.model_dir}")
        
        return model_files
    
    def _setup_output_dirs(self) -> None:
        """Create output directory structure."""
        logger.info(f"Setting up output directories in {self.config.output_dir}")
        
        for split in ['train', 'test', 'val']:
            ensure_dir(self.config.output_dir / split / 'images')
            ensure_dir(self.config.output_dir / split / 'labels')
        
        logger.debug("Output directories created")
    
    def _get_split_counts(self) -> Tuple[int, int, int]:
        """Calculate number of images per dataset split.
        
        Returns:
            Tuple of (train_count, test_count, val_count).
        """
        train_ratio, test_ratio, val_ratio = self.config.train_test_val_split
        total = self.config.num_images
        
        train_count = int(total * train_ratio)
        test_count = int(total * test_ratio)
        val_count = total - train_count - test_count
        
        logger.info(
            f"Dataset split: train={train_count}, test={test_count}, val={val_count}"
        )
        
        return train_count, test_count, val_count
    
    def _setup_scene(self) -> None:
        """Setup basic scene with ground plane and lighting."""
        # Clear scene
        self.scene.clear()
        
        # Add ground plane
        ground = self.scene.add_plane(size=10.0, location=(0, 0, 0), name="Ground")
        self.physics.add_rigid_body(
            ground,
            body_type="PASSIVE",
            friction=self.config.physics.friction,
        )
        
        # Add randomized lighting
        self.lighting_randomizer.randomize_scene_lighting(self.scene)
        
        # Set background
        self.scene.set_background_color((1.0, 1.0, 1.0, 1.0))
    
    def _place_objects(self) -> List[Tuple[object, int]]:
        """Place random objects in scene using physics.
        
        Returns:
            List of (object, class_id) tuples.
        """
        num_objects = random.randint(1, self.config.max_objects_per_scene)
        placed_objects = []
        
        for _ in range(num_objects):
            # Select random model
            model_path = random.choice(self.model_files)
            class_id = self._get_class_id(model_path)
            
            # Load object
            obj = self.object_loader.load_glb(
                model_path,
                scale=random.uniform(*self.config.randomization.object_scale_range),
            )
            
            if obj is None:
                continue
            
            # Drop object from random position
            x = random.uniform(-2.0, 2.0)
            y = random.uniform(-2.0, 2.0)
            height = random.uniform(0.5, 2.0)
            
            self.physics.drop_object(obj, height=height, location=(x, y))
            placed_objects.append((obj, class_id))
        
        # Run physics simulation
        self.physics.simulate()
        
        return placed_objects
    
    def _get_class_id(self, model_path: Path) -> int:
        """Get class ID for a model file.
        
        Args:
            model_path: Path to model file.
            
        Returns:
            Class ID (index in class_names list).
        """
        # Extract class name from path (assuming directory structure)
        # e.g., models/ulus/model.glb -> "ulus"
        class_name = model_path.parent.name
        
        if class_name in self.config.annotation.class_names:
            return self.config.annotation.class_names.index(class_name)
        else:
            # Add new class if not in list
            self.config.annotation.class_names.append(class_name)
            logger.debug(f"Added new class: {class_name}")
            return len(self.config.annotation.class_names) - 1
    
    def generate_single_image(
        self,
        output_path: Path,
        annotation_path: Path,
    ) -> bool:
        """Generate a single synthetic image with annotations.
        
        Args:
            output_path: Path to save rendered image.
            annotation_path: Path to save annotations.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Setup scene
            self._setup_scene()
            
            # Place objects
            placed_objects = self._place_objects()
            
            if not placed_objects:
                logger.warning("No objects placed, skipping image")
                return False
            
            # Randomize camera
            self.camera_randomizer.randomize_camera(self.scene.camera)
            
            # Render image
            self.renderer.render(output_path)
            
            # Calculate bounding boxes
            annotations = []
            for obj, class_id in placed_objects:
                bbox = self.bbox_calculator.calculate_bbox(
                    obj,
                    self.scene.camera,
                    self.config.render.resolution,
                )
                
                if bbox is not None:
                    # Check minimum visibility
                    if bbox.area >= self.config.annotation.min_bbox_area:
                        annotations.append((class_id, bbox))
            
            # Save annotations
            if annotations:
                self.annotator.save_annotations(
                    annotations,
                    annotation_path,
                    self.config.render.resolution,
                )
            else:
                logger.warning("No valid annotations, skipping image")
                return False
            
            # Cleanup
            self.object_loader.clear_all()
            self.physics.clear_simulation()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate image: {e}", exc_info=True)
            return False
    
    def generate_split(
        self,
        split: str,
        num_images: int,
    ) -> int:
        """Generate images for a dataset split.
        
        Args:
            split: Split name ('train', 'test', or 'val').
            num_images: Number of images to generate.
            
        Returns:
            Number of successfully generated images.
        """
        logger.info(f"Generating {num_images} images for {split} split")
        
        images_dir = self.config.output_dir / split / 'images'
        labels_dir = self.config.output_dir / split / 'labels'
        
        success_count = 0
        
        for i in tqdm(range(num_images), desc=f"Generating {split}"):
            image_path = images_dir / f"{split}_{i:06d}.jpg"
            label_path = labels_dir / f"{split}_{i:06d}.txt"
            
            if self.generate_single_image(image_path, label_path):
                success_count += 1
        
        logger.info(
            f"Generated {success_count}/{num_images} images for {split} split"
        )
        
        return success_count
    
    def generate(self) -> None:
        """Generate complete synthetic dataset."""
        logger.info("Starting synthetic dataset generation")
        
        # Get split counts
        train_count, test_count, val_count = self._get_split_counts()
        
        # Generate each split
        self.generate_split('train', train_count)
        self.generate_split('test', test_count)
        self.generate_split('val', val_count)
        
        # Save configuration
        config_path = self.config.output_dir / 'config.yaml'
        from nunalleq_synth.pipeline.config import save_config
        save_config(self.config, config_path)
        
        # Save class names
        classes_path = self.config.output_dir / 'classes.txt'
        with open(classes_path, 'w') as f:
            for class_name in self.config.annotation.class_names:
                f.write(f"{class_name}\n")
        
        logger.info(f"Dataset generation complete: {self.config.output_dir}")