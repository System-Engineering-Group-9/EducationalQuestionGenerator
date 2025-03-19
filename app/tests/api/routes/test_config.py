import logging
import os

import cv2
import numpy as np
from starlette.testclient import TestClient

from app.core.config import settings


def test_get_questions_not_set(client: TestClient):
    """
    Test GET /config/get-questions/ when no questions have been set.
    """
    # Ensure the questions cache is empty by assuming no prior call
    response = client.get(f"{settings.BASE_URL}/config/get-questions/")
    assert response.status_code == 404
    resp_json = response.json()
    logging.info(f"Get questions not set response: {resp_json}")
    assert resp_json.get("message") == "No questions set"


def test_confirm_questions(client: TestClient):
    """
    Test POST /config/confirm-questions/ to store quiz questions, then GET /config/get-questions/ to retrieve them.
    """
    questions_payload = {
        "questions": [
            {
                "question": "Which of the following is a common accessory for professionals in the tech industry?",
                "choiceA": "Headphones with noise-cancelling technology",
                "choiceB": "A leather-bound notebook",
                "choiceC": "A sleek tablet for presentations",
                "choiceD": "A wireless mouse",
                "answer": "A"
            }
        ]
    }

    # Set the questions
    response = client.post(f"{settings.BASE_URL}/config/confirm-questions/", json=questions_payload)
    assert response.status_code == 200
    resp_json = response.json()
    logging.info(f"Confirm questions response: {resp_json}")
    assert resp_json.get("message") == "success"

    # Get the questions
    response_get = client.get(f"{settings.BASE_URL}/config/get-questions/")
    assert response_get.status_code == 200
    resp_json_get = response_get.json()
    logging.info(f"Get questions response: {resp_json_get}")
    assert "questions" in resp_json_get
    assert resp_json_get["questions"] == questions_payload["questions"]


def test_confirm_background(client: TestClient):
    """
    Test POST /config/confirm-background/ with a valid image and then GET /config/get-background-image/.
    """
    # Create a dummy black image using numpy
    dummy_image = np.zeros((50, 50, 3), dtype=np.uint8)
    success, encoded_image = cv2.imencode('.png', dummy_image)
    assert success, "Failed to encode dummy image"
    image_bytes = encoded_image.tobytes()

    files = {
        "file": ("background.png", image_bytes, "image/png")
    }
    response = client.post(f"{settings.BASE_URL}/config/confirm-background/", files=files)
    assert response.status_code == 200
    resp_json = response.json()
    logging.info(f"Confirm background response: {resp_json}")
    assert resp_json.get("message") == "success"

    # Retrieve the background image
    response_get = client.get(f"{settings.BASE_URL}/config/get-background-image/")
    assert response_get.status_code == 200
    assert response_get.headers["content-type"] == "image/png"

    # Clean up the saved file
    if os.path.exists("static/background.png"):
        os.remove("static/background.png")


def test_confirm_background_wrong_media_type(client: TestClient):
    """
    Test POST /config/confirm-background/ with an unsupported media type.
    """
    files = {
        "file": ("dummy.txt", b"This is not an image", "text/plain")
    }
    response = client.post(f"{settings.BASE_URL}/config/confirm-background/", files=files)
    assert response.status_code == 400
    resp_json = response.json()
    logging.info(f"Confirm background wrong media type response: {resp_json}")
    assert resp_json.get("message") == "Unsupported Media Type"


def test_get_background_image_not_set(client: TestClient):
    """
    Test GET /config/get-background-image/ when no background image has been set.
    """
    # Ensure the background image file does not exist
    if os.path.exists("static/background.png"):
        os.remove("static/background.png")
    response = client.get(f"{settings.BASE_URL}/config/get-background-image/")
    assert response.status_code == 404
    resp_json = response.json()
    logging.info(f"Get background image not set response: {resp_json}")
    assert resp_json.get("message") == "No background image set"


def test_confirm_quiz_background(client: TestClient):
    """
    Test POST /config/confirm-quiz-background/ with a valid image and then GET /config/get-quiz-background-image/.
    """
    # Create a dummy white image using numpy
    dummy_image = np.ones((50, 50, 3), dtype=np.uint8) * 255
    success, encoded_image = cv2.imencode('.png', dummy_image)
    assert success, "Failed to encode dummy image"
    image_bytes = encoded_image.tobytes()

    files = {
        "file": ("quizBackground.png", image_bytes, "image/png")
    }
    response = client.post(f"{settings.BASE_URL}/config/confirm-quiz-background/", files=files)
    assert response.status_code == 200
    resp_json = response.json()
    logging.info(f"Confirm quiz background response: {resp_json}")
    assert resp_json.get("message") == "success"

    # Retrieve the quiz background image
    response_get = client.get(f"{settings.BASE_URL}/config/get-quiz-background-image/")
    assert response_get.status_code == 200
    assert response_get.headers["content-type"] == "image/png"

    # Clean up the saved file
    if os.path.exists("static/quizBackground.png"):
        os.remove("static/quizBackground.png")


def test_get_quiz_background_image_not_set(client: TestClient):
    """
    Test GET /config/get-quiz-background-image/ when no quiz background image has been set.
    """
    if os.path.exists("static/quizBackground.png"):
        os.remove("static/quizBackground.png")
    response = client.get(f"{settings.BASE_URL}/config/get-quiz-background-image/")
    assert response.status_code == 404
    resp_json = response.json()
    logging.info(f"Get quiz background image not set response: {resp_json}")
    assert resp_json.get("message") == "No quiz background image set"


def test_get_config_not_set(client: TestClient):
    """
    Test GET /config/get-config/ when no configuration has been set.
    """
    response = client.get(f"{settings.BASE_URL}/config/get-config/")
    assert response.status_code == 404
    resp_json = response.json()
    logging.info(f"Get config not set response: {resp_json}")
    assert resp_json.get("message") == "No configuration set"


def test_set_config(client: TestClient):
    """
    Test POST /config/set-config/ to store a configuration and then GET /config/get-config/ to retrieve it.
    """
    # Define a sample configuration payload. Adjust keys as required by ConfigModel.
    config_payload = {
        "timeLimit": 43,
        "teamMode": "FFA",
        "numberOfPlayers": 2,
        "quizMode": "BUZZ"
    }
    response = client.post(f"{settings.BASE_URL}/config/set-config/", json=config_payload)
    assert response.status_code == 200
    resp_json = response.json()
    logging.info(f"Set config response: {resp_json}")
    assert resp_json.get("message") == "success"

    # Retrieve the configuration
    response_get = client.get(f"{settings.BASE_URL}/config/get-config/")
    assert response_get.status_code == 200
    config_response = response_get.json()
    logging.info(f"Get config response: {config_response}")
    # Verify the configuration matches the payload
    assert config_response.get("timeLimit") == config_payload["timeLimit"]
    assert config_response.get("teamMode") == config_payload["teamMode"]
    assert config_response.get("numberOfPlayers") == config_payload["numberOfPlayers"]
    assert config_response.get("quizMode") == config_payload["quizMode"]
