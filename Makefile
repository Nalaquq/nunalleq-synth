.PHONY: help install install-dev test lint format clean docker-build docker-run docs

help:
	@echo "Nunalleq Synthetic Data Generator - Available commands:"
	@echo ""
	@echo "  make install        Install package"
	@echo "  make install-dev    Install package with development dependencies"
	@echo "  make test           Run tests"
	@echo "  make test-cov       Run tests with coverage"
	@echo "  make lint           Run linters"
	@echo "  make format         Format code"
	@echo "  make type-check     Run type checking"
	@echo "  make clean          Clean build artifacts"
	@echo "  make docker-build   Build Docker image"
	@echo "  make docker-run     Run Docker container"
	@echo "  make docs           Build documentation"
	@echo ""

install:
	pip install -e ".[blender]"

install-dev:
	pip install -e ".[all]"
	pre-commit install

test:
	pytest tests/

test-cov:
	pytest --cov=nunalleq_synth --cov-report=html --cov-report=term tests/

lint:
	flake8 nunalleq_synth/
	pylint nunalleq_synth/

format:
	black nunalleq_synth/ tests/ examples/
	isort nunalleq_synth/ tests/ examples/

type-check:
	mypy nunalleq_synth/

clean:
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .mypy_cache/ htmlcov/ .coverage

docker-build:
	docker build -t nunalleq-synth:latest .

docker-run:
	docker-compose up nunalleq-synth

docker-dev:
	docker-compose up -d nunalleq-dev
	docker exec -it nunalleq-dev /bin/bash

docs:
	cd docs && make html
