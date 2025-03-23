# Educational Quiz Question Generator

## Description

This is an educational quiz question generator developed for the IBM – Mixed Reality Board and Toy Games with Granite 3 SLMs project.

The Generator utilizes:

- **Quantized IBM granite-3.0-8b-instruct** for question generation
- **YOLO** for object detection

It consists of two main components:

- A **GUI desktop application** for generating questions
- A **FastAPI server backend** for handling API requests and AI model processing

---

## Prerequisites

- Nvidia GPU with CUDA support (required)
- Python 3.8 or later
- pip package manager
- [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit) properly installed
- Compatible NVIDIA drivers installed and updated

---

## Installation

1. **Clone the project**
   ```bash
   git clone https://github.com/dcloud347/EducationalQuestionGenerator.git
   cd EducationalQuestionGenerator
   ```

2. **Install PyTorch (CUDA version)**
   
   Install the appropriate `torch` and `torchvision` versions matching your CUDA version:
   
   [Find your installation command here](https://pytorch.org/)

3. **Install llama-cpp-python with CUDA or Metal support**

   For **CUDA (Linux/Windows)**:
   ```bash
   CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python
   ```

   For **MacOS (Metal support)**:
   ```bash
   CMAKE_ARGS="-DGGML_METAL=on" pip install llama-cpp-python
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```



---

## Usage

### GUI Application

Run the desktop GUI application:

```bash
python ./main.py
```

Features:

- Select number of questions (1-5)
- Choose subject area
- Add specific topics (optional)
- Set target age group
- Generate and save questions to `output.json`

---

### FastAPI AI Server Backend

The FastAPI server handles:

- **AI Model Integration**: For question generation and image recognition
- **Data processing and storage**

#### Start the server:

```bash
uvicorn app.main:app --reload
```

Access API documentation:

```
http://127.0.0.1:8000/docs
```

---

## Docker Deployment

Deploying via Docker is also supported:

1. **Build the Docker image**
   ```bash
   docker build -t educational-quiz-generator .
   ```

2. **Run the Docker container**
   ```bash
   docker run --gpus all -p 8000:8000 educational-quiz-generator
   ```

Access the API at `http://127.0.0.1:8000`.

---

## Front-End Description

The project includes a front-end UI built with [teacher-ui](https://github.com/jackmok33/teacher-ui), providing educators an intuitive interface to interact with the quiz generator.

**Features:**

- **Intuitive Dashboard**: Easily generate and manage quiz questions
- **Responsive Design**: Optimized for desktop and mobile
- **Real-Time Interaction**: Connects seamlessly with the FastAPI server for live feedback
- **Customizable Settings**: Choose subject area, age group, and topics with ease

For customization and deployment details, visit the [teacher-ui GitHub repository](https://github.com/jackmok33/teacher-ui).

---

## Testing

**Always test before pushing!**

Run tests:

```bash
coverage run --source=app -m pytest
coverage report --show-missing
coverage html --title "${@-coverage}"
```

---

## Troubleshooting

- Ensure **CUDA Toolkit** and compatible NVIDIA drivers are correctly installed
- Verify PyTorch version matches your CUDA version
- Confirm `llama-cpp-python` is installed with `GGML_CUDA=on` (or `GGML_METAL=on` for MacOS)
- For MacOS, ensure Metal support is available and configured
- GPU not recognized?
  - Check NVIDIA driver installation
  - Check CUDA version compatibility
  - Ensure environment variables like `GGML_CUDA=on` are set **before** installation

---

## Repository Links

- **Main Repository**: [Educational Question Generator](https://github.com/System-Engineering-Group-9/EducationalQuestionGenerator)
- **Front-End UI**: [teacher-ui](https://github.com/jackmok33/teacher-ui)

---

## Author

[Yue Pan](https://dcloud347.github.io)
