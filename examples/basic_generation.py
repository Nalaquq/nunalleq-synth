# ============================================================================
# examples/basic_generation.py
# ============================================================================

#!/usr/bin/env python3
"""Basic example of synthetic data generation."""  # FIXED: Removed escaped quotes

from pathlib import Path

from nunalleq_synth import SyntheticGenerator, GenerationConfig


def main() -> None:
    """Generate a basic synthetic dataset."""
    
    # Configure generation
    config = GenerationConfig(
        model_dir=Path("models/ulus"),
        output_dir=Path("output/basic_example"),
        num_images=100,
        max_objects_per_scene=2,
        random_seed=42,
    )
    
    # Initialize generator
    print("Initializing generator...")
    generator = SyntheticGenerator(config)
    
    # Generate dataset
    print("Generating dataset...")
    generator.generate()
    
    print(f"Dataset saved to: {config.output_dir}")
    print(f"Classes: {config.annotation.class_names}")


if __name__ == "__main__":
    main()