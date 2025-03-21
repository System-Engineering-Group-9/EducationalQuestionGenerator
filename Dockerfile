# Use the official NVIDIA CUDA 12.4 runtime image (Ubuntu 22.04)
FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04

# Set the working directory
WORKDIR /app

# Install system dependencies required for OpenCV and llama-cpp-python
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    cmake \
    make \
    libstdc++6 \
    git \
    libgl1 \
    libglib2.0-0 \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code into the container
COPY . .

# Create a directory for static files
RUN mkdir -p /static

# Download the pre-trained model
RUN python3 -c "from llama_cpp import Llama; Llama.from_pretrained(repo_id='QuantFactory/granite-3.0-8b-instruct-GGUF', filename='granite-3.0-8b-instruct.Q4_K_S.gguf')"
RUN python3 -c "import torch; from diffusers import AutoPipelineForText2Image; AutoPipelineForText2Image.from_pretrained('lykon/dreamshaper-8', torch_dtype=torch.float16, variant='fp16')"

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000", "app.main:app"]
