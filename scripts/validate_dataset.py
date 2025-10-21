

# ============================================================================
# scripts/validate_dataset.py
# ============================================================================

#!/usr/bin/env python3
"\"\"\"Validate generated dataset and create report.\"\"\"

import argparse
import json
from pathlib import Path
from typing import Dict, Any

from nunalleq_synth.annotation.validation import AnnotationValidator
from nunalleq_synth.utils.io import list_files


def generate_report(dataset_dir: Path) -> Dict[str, Any]:
    "\"\"\"Generate validation report for dataset."
    
    Args:
        dataset_dir: Root directory of dataset.
        
    Returns:
        Dictionary containing validation report.
    
    validator = AnnotationValidator()
    
    report = {
        "dataset_dir": str(dataset_dir),
        "splits": {},
        "summary": {},
    }
    
    total_valid = 0
    total_invalid = 0
    all_errors = []
    
    # Validate each split
    for split in ['train', 'test', 'val']:
        images_dir = dataset_dir / split / 'images'
        labels_dir = dataset_dir / split / 'labels'
        
        if not images_dir.exists():
            continue
        
        image_files = list_files(images_dir, "*.jpg")
        label_files = list_files(labels_dir, "*.txt")
        
        report["splits"][split] = {
            "num_images": len(image_files),
            "num_labels": len(label_files),
        }
        
        total_valid += len(image_files)
    
    # Validate annotations
    valid_count, invalid_count, errors = validator.validate_dataset(dataset_dir)
    
    total_valid = valid_count
    total_invalid = invalid_count
    all_errors = errors
    
    # Summary
    report["summary"] = {
        "total_valid": total_valid,
        "total_invalid": total_invalid,
        "error_count": len(all_errors),
        "success_rate": total_valid / (total_valid + total_invalid) if (total_valid + total_invalid) > 0 else 0,
    }
    
    report["errors"] = all_errors[:100]  # Include first 100 errors
    
    return report


def main() -> None:
    "\"\"\"Main validation script.\"\"\"
    parser = argparse.ArgumentParser(description="Validate synthetic dataset")
    parser.add_argument(
        "--dataset",
        type=Path,
        required=True,
        help="Path to dataset directory",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output path for validation report (JSON)",
    )
    
    args = parser.parse_args()
    
    print(f"Validating dataset: {args.dataset}")
    
    # Generate report
    report = generate_report(args.dataset)
    
    # Print summary
    print("\\nValidation Summary:")
    print(f"  Valid samples: {report['summary']['total_valid']}")
    print(f"  Invalid samples: {report['summary']['total_invalid']}")
    print(f"  Success rate: {report['summary']['success_rate']:.2%}")
    print(f"  Errors found: {report['summary']['error_count']}")
    
    # Print split details
    print("\\nSplit Details:")
    for split, data in report["splits"].items():
        print(f"  {split}:")
        print(f"    Images: {data['num_images']}")
        print(f"    Labels: {data['num_labels']}")
    
    # Save report
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\\nReport saved to: {args.output}")
    
    # Print some errors
    if report["errors"]:
        print("\\nFirst few errors:")
        for error in report["errors"][:10]:
            print(f"  - {error}")


if __name__ == "__main__":
    main()
