# AI Server

## Description

This directory contains the AI server for the Educational Quiz Question Generator project. The server is built using FastAPI and provides endpoints for image recognition and question generation.

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
   fastapi run app/main.py
   ```

2. **Access the API documentation**
   Open your web browser and navigate to `http://127.0.0.1:8000/docs` to view the interactive API documentation provided by FastAPI.

## Author

[Yue Pan](https://dcloud347.github.io)
