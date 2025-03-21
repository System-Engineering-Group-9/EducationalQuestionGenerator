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

## Docker Deployment

You can also deploy the application using Docker.

1. **Build the Docker image**
   ```bash
   docker build -t educational-quiz-generator .
   ```

2. **Run the Docker container**
   ```bash
   docker run --gpus all -p 8000:8000 educational-quiz-generator
   ```

This will start the FastAPI server inside a Docker container, and you can access the API at `http://127.0.0.1:8000`.

## Front-End Description

The project also includes a front-end interface built with [teacher-ui](https://github.com/jackmok33/teacher-ui). This
front-end is designed to provide educators with an intuitive and responsive environment to interact with the quiz
question generator. Key features include:

- **Intuitive Dashboard:** Easily manage and generate educational quiz questions.
- **Responsive Design:** Optimized for both desktop and mobile devices to support various usage scenarios.
- **Real-Time Interaction:** Seamless integration with the AI server for live image recognition and question generation,
  ensuring immediate feedback.
- **User-Friendly Experience:** Clean interface and straightforward navigation, enabling teachers to customize settings
  like subject area, target age group, and specific topics without hassle.

For detailed information on front-end customization, deployment, and further enhancements, please refer to
the [teacher-ui GitHub repository](https://github.com/jackmok33/teacher-ui).

## Test

Please test the server before pushing your changes!!!

Test the server using the command below:

```bash
coverage run --source=app -m pytest
coverage report --show-missing
coverage html --title "${@-coverage}"
```

## Troubleshooting

- Ensure CUDA 12.4 is properly installed
- Check NVIDIA drivers are up to date
- For MacOS users, verify Metal support requirements

## Author

[Yue Pan](https://dcloud347.github.io)
