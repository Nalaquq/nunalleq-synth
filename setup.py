# setup.py
"""Setup configuration for nunalleq-synth package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read version
version = {}
with open("nunalleq_synth/__version__.py") as f:
    exec(f.read(), version)

# Read long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Core dependencies (without Blender - always installable)
install_requires = [
    "numpy>=1.24.0,<2.0.0",
    "opencv-python>=4.7.0,<5.0.0",
    "Pillow>=9.5.0,<11.0.0",
    "PyYAML>=6.0,<7.0.0",
    "tqdm>=4.65.0,<5.0.0",
    "pydantic>=2.0.0,<3.0.0",
    "typing-extensions>=4.6.0",
]

# Blender dependencies (optional - for actual rendering)
blender_requires = [
    "bpy>=3.6.0; python_version=='3.11'",  # bpy only works on Python 3.11
]

# Development dependencies
dev_requires = [
    "pytest>=7.3.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.11.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.3.0",
    "isort>=5.12.0",
    "mypy>=1.3.0",
    "flake8>=6.0.0",
    "pylint>=2.17.0",
    "pre-commit>=3.3.0",
    "ipython>=8.12.0",
    "ipdb>=0.13.13",
]

# Documentation dependencies
doc_requires = [
    "sphinx>=6.2.0",
    "sphinx-rtd-theme>=1.2.0",
    "myst-parser>=1.0.0",
]

setup(
    name="nunalleq-synth",
    version=version["__version__"],
    description="Physics-based synthetic data generation for Yup'ik artifact object detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nalaquq, LLC & Native Village of Kwinhagak",
    author_email="info@nalaquq.com",
    url="https://github.com/nalaquq/nunalleq-synth",
    project_urls={
        "Documentation": "https://nunalleq-synth.readthedocs.io",
        "Source": "https://github.com/nalaquq/nunalleq-synth",
        "Tracker": "https://github.com/nalaquq/nunalleq-synth/issues",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require={
        "blender": blender_requires,
        "dev": dev_requires,
        "docs": doc_requires,
        "all": blender_requires + dev_requires + doc_requires,
    },
    entry_points={
        "console_scripts": [
            "nunalleq-synth=nunalleq_synth.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
    ],
    keywords="synthetic-data computer-vision object-detection blender yolo cultural-heritage",
    license="MIT",
    zip_safe=False,
)

