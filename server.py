import os
from typing import List

import cv2
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ai.detection import Detection
import numpy as np
import uvicorn

from ai.genAI import GenAI, Topics
from models.question import Question

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


# Confirm Questions by CSV file
@app.post("/confirm-by-csv/")
def confirm_by_csv(file: UploadFile = File(...)):
    if not file.content_type.startswith("text/csv"):
        return JSONResponse(content={"message": "Unsupported Media Type", "data":None}, status_code=400)
    # save the file
    with open("static/output.csv", "wb") as f:
        f.write(file.file.read())
    return JSONResponse(content={"message": "success", "data":None})


# Confirm Questions by JSON
@app.post("/confirm-by-json/")
def confirm_by_json(data: List[Question]):
    # turn the data into a csv file
    csvHeader = ['question', 'choice A', 'choice B', 'choice C', 'choice D', 'answer']
    file = open("static/output.csv", "w")
    file.write(",".join(csvHeader)+'\n')
    for question in data:
        file.write(",".join(question.__dict__.values())+'\n')
    file.close()
    return JSONResponse(content={"message": "success", "data":None})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
