# ============================================================================
# examples/batch_processing.py
# ============================================================================

#!/usr/bin/env python3
"\"\"\"Example of batch processing multiple model directories.\"\"\"

from pathlib import Path

from nunalleq_synth import GenerationConfig
from nunalleq_synth.pipeline.batch import BatchProcessor


def main() -> None:
    "\"\"\"Process multiple model directories in parallel.\"\"\"
    
    # Base configuration
    base_config = GenerationConfig(
        model_dir=Path("models"),  # Will be overridden
        output_dir=Path("output"),  # Will be overridden
        num_images=500,
        max_objects_per_scene=2,
    )
    
    # Initialize batch processor
    processor = BatchProcessor(
        config=base_config,
        num_workers=4,  # Process 4 directories in parallel
    )
    
    # Find all model directories
    model_base = Path("models")
    model_dirs = [
        d for d in model_base.iterdir()
        if d.is_dir() and list(d.glob("*.glb"))
    ]
    
    print(f"Found {len(model_dirs)} model directories")
    print(f"Model directories: {[d.name for d in model_dirs]}")
    
    # Process all directories
    output_base = Path("output/batch_processed")
    success_count = processor.process_multiple(model_dirs, output_base)
    
    print(f"Successfully processed {success_count}/{len(model_dirs)} directories")


if __name__ == "__main__":
    main()
