import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from app.ai.genAI import GenAI, Topics
from app.ai.detection import Detection

router = APIRouter(prefix="/ai", tags=["ai"])


# Initialize the AI model
detection = Detection()
genAi = GenAI()

@router.post("/recognize/")
def recognize(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        return JSONResponse(content={"message": "Unsupported Media Type", "data":None}, status_code=400)
    # turn the image into a openCV format image
    image_bytes = file.file.read()
    np_image = np.frombuffer(image_bytes, np.uint8)
    bgr_image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
    return JSONResponse(content={
        "message": "success",
        "data": detection.detect(bgr_image)
    })

@router.get("/generate/")
def generate(topic: Topics, number:int, ageGroup:str, item:str=None):
    questions = genAi.generateQuestions(number, topic, ageGroup, item)
    questions = [question.__dict__ for question in questions]
    return JSONResponse(content={
        "message": f"success",
        "data": questions
    })