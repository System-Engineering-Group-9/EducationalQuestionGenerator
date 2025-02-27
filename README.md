# Educational Quiz Question Generator

## Description

This is an educational quiz question generator used for project IBM – Mixed Reality Board and Toy Games with Granite 3 SLMs.

The Generator utilizes quantized IBM granite-3.0-8b-instruct for question generation and YOLO for object detection. It
consists of two main components:

- A GUI application for generating questions
- An AI server for handling API requests

## Prerequisites

- CUDA 12.4 or later (required)
- Python 3.8 or later
- pip package manager

## Installation

1. **Clone the project**
   ```bash
   git clone https://github.com/dcloud347/EducationalQuestionGenerator.git
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure llama-cpp-python with CUDA**
   ```bash
   CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
   ```

   For MacOS users (Metal support):
   ```bash
   CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python
   ```

## Usage

### GUI Application

Run the desktop application for generating questions:

```bash
python ./main.py
```

The GUI allows you to:

- Select number of questions (1-5)
- Choose subject area
- Add specific topics (optional)
- Set target age group
- Generate and save questions to `output.json`

### AI Server

Start the FastAPI server for API access:

```bash
uvicorn app.main:app --reload
```

The server provides:

- Image recognition endpoint (`/ai/recognize/`)
- Question generation endpoint (`/ai/generate/`)

For detailed API documentation, visit `http://127.0.0.1:8000/docs`

For more information about the AI server, see [AI Server Documentation](app/README.md)

## Troubleshooting

- Ensure CUDA 12.4 is properly installed
- Check NVIDIA drivers are up to date
- For MacOS users, verify Metal support requirements

## Author

[Yue Pan](https://dcloud347.github.io)
