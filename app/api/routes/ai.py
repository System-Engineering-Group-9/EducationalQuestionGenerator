import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse

from app.ai.genAI import GenAI
from app.ai.detection import Detection
from app.models.generateModel import GenerateModel
from app.models.questionModel import QuestionsModel
from app.models.recognitionModel import RecognitionModel
from app.models.resultModel import ResultModel

router = APIRouter(prefix="/ai", tags=["ai"])


# Initialize the AI model
detection = Detection()
genAi = GenAI()

# Recognize the image
@router.post("/recognize/", response_model=ResultModel)
def recognize(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        return JSONResponse(content={"message": "Unsupported Media Type", "data":None}, status_code=400)
    # turn the image into a openCV format image
    image_bytes = file.file.read()
    np_image = np.frombuffer(image_bytes, np.uint8)
    bgr_image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
    return ResultModel(message="success", data=RecognitionModel(item=detection.detect(bgr_image)))


# Generate questions
@router.get("/generate/", response_model=ResultModel)
def generate(params: GenerateModel=Depends()):
    questions = genAi.generateQuestions(params.number, params.topic, params.ageGroup, params.item)
    questions = [question.__dict__ for question in questions]
    return ResultModel(message="success", data=QuestionsModel(questions=questions))