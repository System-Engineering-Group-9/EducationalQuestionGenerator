import tempfile

import cv2
import numpy as np
import torch
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse, FileResponse

from app.ai.detection import Detection
from app.ai.dreamShaper import DreamShaper
from app.ai.questionGenerator import QuestionGenerator
from app.models.dreamShaperModel import DreamShaperModel
from app.models.generateModel import GenerateModel
from app.models.questionModel import QuestionsModel
from app.models.recognitionModel import RecognitionsModel
from app.models.resultModel import ResultModel

router = APIRouter(prefix="/ai", tags=["ai"])

# Lazy load the AI models
detection = None
questionGenerator = None
dreamShaper = DreamShaper()


def get_detection():
    global detection
    if detection is None:
        detection = Detection()
    return detection


def get_question_generator():
    global questionGenerator
    if questionGenerator is None:
        questionGenerator = QuestionGenerator()
    return questionGenerator


# Recognize the image
@router.post("/recognize/", response_model=ResultModel)
def recognize(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        return JSONResponse(content={"message": "Unsupported Media Type", "data": None}, status_code=400)

    # Convert the uploaded image to OpenCV format
    image_bytes = file.file.read()
    np_image = np.frombuffer(image_bytes, np.uint8)
    bgr_image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    # Detect items in the image
    detection_model = get_detection()
    return ResultModel(message="success", data=RecognitionsModel(items=detection_model.detect(bgr_image)))


# Release the detection model
@router.post("/release-detection/", response_model=ResultModel)
def release_detection():
    global detection
    if detection is not None:
        detection.cpu()  # Switch to CPU mode
        del detection
        torch.cuda.empty_cache()
        detection = None
    return ResultModel(message="success", data=None)


# Release the question generator
@router.post("/release-question-generator/", response_model=ResultModel)
def release_question_generator():
    global questionGenerator
    questionGenerator = None
    return ResultModel(message="success", data=None)

# Generate questions
@router.get("/generate/", response_model=ResultModel)
def generate(params: GenerateModel = Depends()):
    # Generate questions based on the provided parameters
    question_generator = get_question_generator()
    questions = question_generator.generateQuestions(params.number, params.subject, params.ageGroup, params.item)
    questions = [question.__dict__ for question in questions]

    # Return the generated questions
    return ResultModel(message="success", data=QuestionsModel(questions=questions))


# Generate image
@router.get("/generate-background-image/")
def generate_background_image(params: DreamShaperModel = Depends()):
    image = dreamShaper.generate_background_image(params.subject, params.ageGroup)

    # Save the image to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        success = cv2.imwrite(tmp_file.name, np.array(image))
        if not success:
            return JSONResponse(content={"message": "Failed to save image", "data": None}, status_code=500)
        tmp_file_path = tmp_file.name

    return FileResponse(tmp_file_path, media_type="image/png", filename="generated_background_image.png")


@router.get("/generate-quiz-background-image/")
def generate_background_image(params: DreamShaperModel = Depends()):
    image = dreamShaper.generate_quiz_panel_background_image(params.subject, params.ageGroup)

    # Save the image to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        success = cv2.imwrite(tmp_file.name, np.array(image))
        if not success:
            return JSONResponse(content={"message": "Failed to save image", "data": None}, status_code=500)
        tmp_file_path = tmp_file.name

    return FileResponse(tmp_file_path, media_type="image/png", filename="generated_quiz_background_image.png")
