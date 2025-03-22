# Use the NVIDIA CUDA 12.4 development image (Ubuntu 22.04)
FROM nvidia/cuda:12.4.0-devel-ubuntu22.04

# Set the working directory
WORKDIR /app

# Set environment variables to help with CUDA detection and enable GPU support in llama-cpp-python
ENV CUDA_HOME=/usr/local/cuda
ENV CMAKE_ARGS="-DGGML_CUDA=ON"
ENV GGML_CUDA=1

# Add the CUDA stubs directory to LD_LIBRARY_PATH and create a symlink for libcuda.so.1
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64/stubs:${LD_LIBRARY_PATH}"
RUN ln -sf /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/libcuda.so.1

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

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip

# Install torch and torchvision
RUN pip install torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu124

# Install diskcache
RUN pip install diskcache>=5.6.1

# Install llama-cpp-python
RUN pip install llama-cpp-python --index-url https://abetlen.github.io/llama-cpp-python/whl/cu124/

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Create a directory for static files
RUN mkdir -p /static

# Download the pre-trained model
RUN python3 -c "from llama_cpp import Llama; Llama.from_pretrained(repo_id='QuantFactory/granite-3.0-8b-instruct-GGUF', filename='granite-3.0-8b-instruct.Q4_K_S.gguf')"
RUN python3 -c "import torch; from diffusers import AutoPipelineForText2Image; AutoPipelineForText2Image.from_pretrained('lykon/dreamshaper-8', torch_dtype=torch.float16, variant='fp16')"

# Expose port 8000
EXPOSE 8000

# Run the application using gunicorn with Uvicorn workers
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000", "app.main:app"]
