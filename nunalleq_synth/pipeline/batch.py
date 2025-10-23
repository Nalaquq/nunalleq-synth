# ============================================================================
# nunalleq_synth/pipeline/batch.py
# ============================================================================
"""Batch processing utilities."""

import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional

from tqdm import tqdm

from nunalleq_synth.pipeline.config import GenerationConfig, load_config
from nunalleq_synth.pipeline.generator import SyntheticGenerator

logger = logging.getLogger(__name__)


class BatchProcessor:
    """Processes multiple model directories in batch.
    
    Attributes:
        config: Base generation configuration.
        num_workers: Number of parallel workers.
    """
    
    def __init__(
        self,
        config: GenerationConfig,
        num_workers: int = 4,
    ) -> None:
        """Initialize batch processor.
        
        Args:
            config: Base generation configuration.
            num_workers: Number of parallel workers.
        """
        self.config = config
        self.num_workers = num_workers
        logger.info(f"BatchProcessor initialized with {num_workers} workers")
    
    def process_directory(
        self,
        model_dir: Path,
        output_dir: Path,
    ) -> bool:
        """Process a single model directory.
        
        Args:
            model_dir: Directory containing models.
            output_dir: Output directory.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Create config for this directory
            # FIXED: Use model_copy() instead of copy() for Pydantic v2
            config = self.config.model_copy(deep=True)
            config.model_dir = model_dir
            config.output_dir = output_dir
            
            # Generate dataset
            generator = SyntheticGenerator(config)
            generator.generate()
            
            logger.info(f"Completed processing {model_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to process {model_dir}: {e}", exc_info=True)
            return False
    
    def process_multiple(
        self,
        model_dirs: List[Path],
        output_base: Path,
    ) -> int:
        """Process multiple model directories.
        
        Args:
            model_dirs: List of model directories.
            output_base: Base output directory.
            
        Returns:
            Number of successfully processed directories.
        """
        logger.info(f"Processing {len(model_dirs)} directories")
        
        success_count = 0
        
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            futures = {}
            
            for model_dir in model_dirs:
                output_dir = output_base / model_dir.name
                future = executor.submit(
                    self.process_directory,
                    model_dir,
                    output_dir,
                )
                futures[future] = model_dir
            
            # Process completed tasks
            for future in tqdm(
                as_completed(futures),
                total=len(futures),
                desc="Processing directories",
            ):
                model_dir = futures[future]
                try:
                    if future.result():
                        success_count += 1
                except Exception as e:
                    logger.error(f"Error processing {model_dir}: {e}")
        
        logger.info(
            f"Batch processing complete: {success_count}/{len(model_dirs)} succeeded"
        )
        
        return success_count