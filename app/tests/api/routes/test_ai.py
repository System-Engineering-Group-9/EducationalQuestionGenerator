import logging

import cv2
import numpy as np
from starlette.testclient import TestClient

from app.core.config import settings


# --- Test /ai/recognize/ endpoint ---
def test_recognize_success(client: TestClient):
    """
    Test the /ai/recognize/ endpoint with a valid image.
    """
    # Create a dummy black image using numpy
    dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
    # Encode the image as PNG in memory
    success, encoded_image = cv2.imencode('.png', dummy_image)
    assert success, "Failed to encode dummy image"
    image_bytes = encoded_image.tobytes()

    # Build file upload payload
    files = {
        "file": ("dummy.png", image_bytes, "image/png")
    }

    response = client.post(f"{settings.BASE_URL}/ai/recognize/", files=files)
    assert response.status_code == 200

    resp_json = response.json()
    logging.info(f"Recognize response: {resp_json}")
    assert resp_json.get("message") == "success"
    # The response data should contain an 'items' list (even if empty)
    assert "data" in resp_json and "items" in resp_json["data"]


def test_recognize_wrong_media_type(client: TestClient):
    """
    Test the /ai/recognize/ endpoint with an unsupported file type.
    """
    files = {
        "file": ("dummy.txt", b"this is not an image", "text/plain")
    }
    response = client.post(f"{settings.BASE_URL}/ai/recognize/", files=files)
    # Expecting a 400 error due to unsupported media type
    assert response.status_code == 400

    resp_json = response.json()
    logging.info(f"Wrong media type response: {resp_json}")
    assert resp_json.get("message") == "Unsupported Media Type"


# --- Test model release endpoints ---
def test_release_detection(client: TestClient):
    """
    Test the /ai/release-detection/ endpoint.
    """
    response = client.post(f"{settings.BASE_URL}/ai/release-detection/")
    assert response.status_code == 200
    resp_json = response.json()
    logging.info(f"Release detection response: {resp_json}")
    assert resp_json.get("message") == "success"


# --- Test the question generation endpoint ---
def test_generate_questions(client: TestClient):
    """
    Test the /ai/generate/ the question generator.
    """
    # Prepare query parameters matching GenerateModel fields.
    params = {
        "number": 1,
        "subject": "History",
        "ageGroup": "10-12",
        "item": "French Revolution"
    }
    response = client.get(f"{settings.BASE_URL}/ai/generate/", params=params)
    assert response.status_code == 200

    resp_json = response.json()
    logging.info(f"Generate questions response: {resp_json}")
    assert resp_json.get("message") == "success"

    data = resp_json.get("data")
    assert data is not None
    assert "questions" in data
    assert len(data["questions"]) == 1


def test_release_question_generator(client: TestClient):
    """
    Test the /ai/release-question-generator/ endpoint.
    """
    response = client.post(f"{settings.BASE_URL}/ai/release-question-generator/")
    assert response.status_code == 200
    resp_json = response.json()
    logging.info(f"Release question generator response: {resp_json}")
    assert resp_json.get("message") == "success"


# --- Test the background image generation endpoints ---
def test_generate_background_images(client: TestClient):
    """
    Test the /ai/generate-background-image/ and /ai/generate-quiz-background-image/ endpoints
    """

    params = {
        "subject": "History",
        "ageGroup": "10-12"
    }
    # Test /ai/generate-background-image/
    response_bg = client.get(f"{settings.BASE_URL}/ai/generate-background-image/", params=params)
    assert response_bg.status_code == 200
    logging.info("Background image endpoint returned status 200")
    # Expect a PNG file response
    assert response_bg.headers["content-type"] == "image/png"

    # Test /ai/generate-quiz-background-image/
    response_quiz = client.get(f"{settings.BASE_URL}/ai/generate-quiz-background-image/", params=params)
    assert response_quiz.status_code == 200
    logging.info("Quiz background image endpoint returned status 200")
    assert response_quiz.headers["content-type"] == "image/png"
