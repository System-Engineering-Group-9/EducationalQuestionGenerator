import os

import cv2
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from detection import Detection
import numpy as np
import uvicorn

from genAI import GenAI, Topics

# Initialize the server
app = FastAPI()
detection = Detection()
genAi = GenAI()

# Get the path of the html file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE_PATH = os.path.join(BASE_DIR, "static/html/index.html")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Recognition interface
@app.post("/recognize/")
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

@app.get("/generate/")
def generate(topic: Topics, number:int, ageGroup:str, item:str=None):
    questions = genAi.generateQuestions(number, topic, ageGroup, item)
    questions = [question.__dict__ for question in questions]
    return JSONResponse(content={
        "message": f"success",
        "data": questions
    })

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
