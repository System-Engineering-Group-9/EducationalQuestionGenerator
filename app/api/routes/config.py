import json
import os

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse

from app.models.questionModel import QuestionsModel
from app.models.resultModel import ResultModel

router = APIRouter(prefix="/config", tags=["config"])


# Confirm quiz questions
@router.post("/confirm-questions/")
def confirm_by_json(data: QuestionsModel):
    # turn the data into a json file
    file = open("static/output.json", "w")
    file.write(json.dumps([question.__dict__ for question in data.questions], indent=4))
    file.close()
    return ResultModel(message="success", data=None)


# Set Background Image
@router.post("/confirm-background/", response_model=ResultModel)
def confirm_background(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        return JSONResponse(content={"message": "Unsupported Media Type", "data": None}, status_code=400)
    # save the file
    with open("static/background.png", "wb") as f:
        f.write(file.file.read())
    return ResultModel(message="success", data=None)

@router.get("/get-questions/")
def get_questions():
    # check if the file exists
    if not os.path.exists("static/output.json"):
        return JSONResponse(content={"message": "No questions set", "data":None}, status_code=404)
    return FileResponse("static/output.json", media_type="application/json", filename="quizQuestions.json")


@router.get("/get-background-image/")
def get_background_image():
    # check if the file exists
    if not os.path.exists("static/background.png"):
        return JSONResponse(content={"message": "No background image set", "data": None}, status_code=404)
    return FileResponse("static/background.png", media_type="image/png", filename="background.png")
