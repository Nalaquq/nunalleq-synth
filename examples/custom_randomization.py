# ============================================================================
# examples/custom_randomization.py
# ============================================================================

#!/usr/bin/env python3
"""Example with custom randomization parameters."""  # FIXED

from pathlib import Path

from nunalleq_synth import GenerationConfig
from nunalleq_synth.pipeline.generator import SyntheticGenerator
from nunalleq_synth.pipeline.config import RandomizationConfig


def main() -> None:
    """Generate dataset with custom randomization."""
    
    # Custom randomization settings
    randomization = RandomizationConfig(
        lighting_intensity_range=(1000.0, 3000.0),  # Brighter lights
        lighting_color_temp_range=(5000.0, 6500.0),  # Cooler temperature
        camera_distance_range=(0.3, 1.0),  # Closer camera
        camera_angle_range=(-45.0, 45.0),  # Wider angle range
        object_scale_range=(0.7, 1.3),  # More scale variation
        background_brightness_range=(0.6, 1.0),  # Varied backgrounds
    )
    
    # Create configuration
    config = GenerationConfig(
        model_dir=Path("models/artifacts"),
        output_dir=Path("output/custom_randomization"),
        num_images=200,
        max_objects_per_scene=3,
        randomization=randomization,
    )
    
    # Generate
    generator = SyntheticGenerator(config)
    generator.generate()
    
    print("Custom randomization dataset generated!")


if __name__ == "__main__":
    main()