# AI Server

## Description

This directory contains the AI server for the Educational Quiz Question Generator project. The server is built using FastAPI and provides endpoints for image recognition and question generation.

## Installation

### Prerequisites

- CUDA 12.4 or later
- Python 3.8 or later
- pip package manager

### Dependencies

1. **Core Dependencies**
   ```bash
   pip install fastapi uvicorn llama-cpp-python
   ```

2. **CUDA Support**

   To enable CUDA support for llama-cpp-python, install with CUDA:
   ```bash
   CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
   ```

   Or if you've already installed llama-cpp-python:
   ```bash
   pip uninstall llama-cpp-python
   CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
   ```

3. **Metal Support (MacOS only)**
   ```bash
   CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python
   ```

### Verification

Verify CUDA installation:

```python
from llama_cpp import Llama

llm = Llama(model_path="path/to/model", n_gpu_layers=-1)
# If CUDA is properly installed, this will use GPU acceleration
```

## Endpoints

### Recognize Image

- **URL:** `/ai/recognize/`
- **Method:** `POST`
- **Description:** Recognizes items in an uploaded image.
- **Request:**
  - **Content-Type:** `multipart/form-data`
  - **File:** An image file to be recognized.
- **Response:**
  - **Status Code:** `200 OK` if successful, `400 Bad Request` if the file is not an image.
  - **Body:** JSON object containing the recognition result.

### Generate Questions

- **URL:** `/ai/generate/`
- **Method:** `GET`
- **Description:** Generates quiz questions based on provided parameters.
- **Request:**
  - **Parameters:**
    - `subject` (string): The subject for the questions.
    - `number` (int): The number of questions to generate.
    - `ageGroup` (string): The age group for the questions.
    - `item` (string, optional): Specific item to generate questions about.
- **Response:**
  - **Status Code:** `200 OK`
  - **Body:** JSON object containing the generated questions.

## Running the Server

1. **Start the FastAPI server**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the API documentation**
   Open your web browser and navigate to `http://127.0.0.1:8000/docs` to view the interactive API documentation provided by FastAPI.

## Troubleshooting

- If you encounter CUDA-related errors, ensure your NVIDIA drivers are up to date
- For Metal-related issues on MacOS, verify that your system meets the minimum requirements

## Author

[Yue Pan](https://dcloud347.github.io)
