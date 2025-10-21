
# ============================================================================
# nunalleq_synth/__main__.py
# ============================================================================
"""Command-line interface for nunalleq-synth."""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional, Sequence

from nunalleq_synth import __version__
from nunalleq_synth.pipeline.config import GenerationConfig, load_config
from nunalleq_synth.pipeline.generator import SyntheticGenerator
from nunalleq_synth.utils.logger import setup_logger


def parse_args(args: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.
    
    Args:
        args: Command-line arguments to parse. If None, uses sys.argv.
        
    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Nunalleq Synthetic Data Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Generate command
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate synthetic dataset",
    )
    generate_parser.add_argument(
        "--models",
        type=Path,
        required=True,
        help="Directory containing 3D models (.glb files)",
    )
    generate_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output directory for generated dataset",
    )
    generate_parser.add_argument(
        "--config",
        type=Path,
        help="Path to configuration YAML file",
    )
    generate_parser.add_argument(
        "--num-images",
        type=int,
        default=1000,
        help="Total number of images to generate (default: 1000)",
    )
    generate_parser.add_argument(
        "--resolution",
        type=int,
        nargs=2,
        default=[1920, 1080],
        metavar=("WIDTH", "HEIGHT"),
        help="Image resolution (default: 1920 1080)",
    )
    generate_parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of parallel workers (default: 1)",
    )
    generate_parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducibility",
    )
    generate_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    
    # Batch command
    batch_parser = subparsers.add_parser(
        "batch",
        help="Batch process multiple model directories",
    )
    batch_parser.add_argument(
        "--models",
        type=Path,
        required=True,
        help="Parent directory containing model subdirectories",
    )
    batch_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output directory for generated datasets",
    )
    batch_parser.add_argument(
        "--config",
        type=Path,
        help="Path to configuration YAML file",
    )
    batch_parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of parallel workers (default: 4)",
    )
    
    # Validate command
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate generated dataset",
    )
    validate_parser.add_argument(
        "--dataset",
        type=Path,
        required=True,
        help="Path to dataset directory",
    )
    validate_parser.add_argument(
        "--visualize",
        action="store_true",
        help="Generate visualization of annotations",
    )
    
    return parser.parse_args(args)


def generate_command(args: argparse.Namespace) -> int:
    """Execute the generate command.
    
    Args:
        args: Parsed command-line arguments.
        
    Returns:
        Exit code (0 for success, non-zero for error).
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        if args.config:
            config = load_config(args.config)
        else:
            config = GenerationConfig()
        
        # Override config with command-line arguments
        config.model_dir = args.models
        config.output_dir = args.output
        config.num_images = args.num_images
        config.resolution = tuple(args.resolution)
        
        if args.seed is not None:
            config.random_seed = args.seed
        
        # Initialize generator
        logger.info("Initializing synthetic data generator...")
        generator = SyntheticGenerator(config)
        
        # Generate dataset
        logger.info(f"Generating {args.num_images} images...")
        generator.generate()
        
        logger.info(f"Dataset generated successfully in {args.output}")
        return 0
        
    except Exception as e:
        logger.error(f"Generation failed: {e}", exc_info=True)
        return 1


def batch_command(args: argparse.Namespace) -> int:
    """Execute the batch command.
    
    Args:
        args: Parsed command-line arguments.
        
    Returns:
        Exit code (0 for success, non-zero for error).
    """
    logger = logging.getLogger(__name__)
    logger.info("Batch processing not yet implemented")
    return 1


def validate_command(args: argparse.Namespace) -> int:
    """Execute the validate command.
    
    Args:
        args: Parsed command-line arguments.
        
    Returns:
        Exit code (0 for success, non-zero for error).
    """
    logger = logging.getLogger(__name__)
    logger.info("Validation not yet implemented")
    return 1


def main(args: Optional[Sequence[str]] = None) -> int:
    """Main entry point for CLI.
    
    Args:
        args: Command-line arguments. If None, uses sys.argv.
        
    Returns:
        Exit code (0 for success, non-zero for error).
    """
    parsed_args = parse_args(args)
    
    # Setup logging
    log_level = logging.DEBUG if getattr(parsed_args, "verbose", False) else logging.INFO
    setup_logger(log_level)
    
    # Execute command
    if parsed_args.command == "generate":
        return generate_command(parsed_args)
    elif parsed_args.command == "batch":
        return batch_command(parsed_args)
    elif parsed_args.command == "validate":
        return validate_command(parsed_args)
    else:
        print("No command specified. Use --help for usage information.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

