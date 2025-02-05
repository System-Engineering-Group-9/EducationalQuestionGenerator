# Educational Quiz Question Generator

## Description

This is an educational quiz question generator used for project IBM – Mixed Reality Board and Toy Games with Granite 3 SLMs.

The Generator make use of ibm-granite/granite-3.1-2b-instruct for generating questions and YOLO for object detection.

## Installations

1. **Clone the project**
   ```bash
   git clone https://github.com/dcloud347/EducationalQuestionGenerator.git
   ```

2. **Install pip dependencies**
    
    ```bash
    pip install -r requirements.txt
    ```
   Make sure you are using CUDA 12.4 version, other versions may not work.

## How to use

1. **Generating questions by simply run**

   ```bash
   python ./main.py
   ```
2. **Start a Server**

   ```bash
   fastapi run app/main.py
   ```

## Author

[Yue Pan](https://dcloud347.github.io)

