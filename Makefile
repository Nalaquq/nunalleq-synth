
# ============================================================================
# Makefile
# ============================================================================
"""
.PHONY: help install install-dev test lint format clean docker-build docker-run docs

help:
\t@echo "Nunalleq Synthetic Data Generator - Available commands:"
\t@echo ""
\t@echo "  make install        Install package"
\t@echo "  make install-dev    Install package with development dependencies"
\t@echo "  make test           Run tests"
\t@echo "  make test-cov       Run tests with coverage"
\t@echo "  make lint           Run linters"
\t@echo "  make format         Format code"
\t@echo "  make type-check     Run type checking"
\t@echo "  make clean          Clean build artifacts"
\t@echo "  make docker-build   Build Docker image"
\t@echo "  make docker-run     Run Docker container"
\t@echo "  make docs           Build documentation"
\t@echo ""

install:
\tpip install -e .

install-dev:
\tpip install -e ".[dev]"
\tpre-commit install

test:
\tpytest tests/

test-cov:
\tpytest --cov=nunalleq_synth --cov-report=html --cov-report=term tests/

lint:
\tflake8 nunalleq_synth/
\tpylint nunalleq_synth/

format:
\tblack nunalleq_synth/ tests/ examples/
\tisort nunalleq_synth/ tests/ examples/

type-check:
\tmypy nunalleq_synth/

clean:
\tfind . -type f -name '*.py[co]' -delete
\tfind . -type d -name '__pycache__' -delete
\tfind . -type d -name '*.egg-info' -exec rm -rf {} +
\trm -rf build/ dist/ .pytest_cache/ .mypy_cache/ htmlcov/ .coverage

docker-build:
\tdocker build -t nunalleq-synth:latest .

docker-run:
\tdocker-compose up nunalleq-synth

docker-dev:
\tdocker-compose up -d nunalleq-dev
\tdocker exec -it nunalleq-dev /bin/bash

docs:
\tcd docs && make html

# Example generation commands
generate-example:
\tnunalleq-synth generate \\
\t\t--models ./models \\
\t\t--output ./output \\
\t\t--num-images 100 \\
\t\t--resolution 1920 1080

generate-with-config:
\tnunalleq-synth generate --config configs/high_quality.yaml

validate-dataset:
\tnunalleq-synth validate --dataset ./output --visualize
"""

