# Dockerfile
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    BLENDER_VERSION=3.6 \
    BLENDER_VERSION_FULL=3.6.5

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    wget \
    xz-utils \
    libxi6 \
    libxxf86vm1 \
    libxfixes3 \
    libxrender1 \
    libgl1 \
    libglu1-mesa \
    libsm6 \
    && rm -rf /var/lib/apt/lists/*

# Download and install Blender
RUN wget -q https://download.blender.org/release/Blender${BLENDER_VERSION}/blender-${BLENDER_VERSION_FULL}-linux-x64.tar.xz \
    && tar -xf blender-${BLENDER_VERSION_FULL}-linux-x64.tar.xz \
    && mv blender-${BLENDER_VERSION_FULL}-linux-x64 /opt/blender \
    && rm blender-${BLENDER_VERSION_FULL}-linux-x64.tar.xz \
    && ln -s /opt/blender/blender /usr/local/bin/blender

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install package in development mode
RUN pip3 install -e .

# Create data directories
RUN mkdir -p /data/models /data/output

# Set entrypoint
ENTRYPOINT ["nunalleq-synth"]
CMD ["--help"]
