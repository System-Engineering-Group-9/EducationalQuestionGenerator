import os

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse

from app.models.configModel import ConfigModel
from app.models.questionModel import QuestionsModel
from app.models.resultModel import ResultModel

router = APIRouter(prefix="/config", tags=["config"])

cache = {}

# Confirm quiz questions
@router.post("/confirm-questions/")
def confirm_by_json(data: QuestionsModel):
    cache["questions"] = data.questions
    return ResultModel(message="success", data=None)


@router.get("/get-questions/", response_model=QuestionsModel)
def get_questions():
    questions = cache.get("questions", [])
    if not questions:
        return JSONResponse(content={"message": "No questions set", "data": None}, status_code=404)
    return QuestionsModel(questions=questions)


# Set Background Image
@router.post("/confirm-background/", response_model=ResultModel)
def confirm_background(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        return JSONResponse(content={"message": "Unsupported Media Type", "data": None}, status_code=400)
    # save the file
    with open("static/background.png", "wb") as f:
        f.write(file.file.read())
    return ResultModel(message="success", data=None)


@router.get("/get-background-image/")
def get_background_image():
    # check if the file exists
    if not os.path.exists("static/background.png"):
        return JSONResponse(content={"message": "No background image set", "data": None}, status_code=404)
    return FileResponse("static/background.png", media_type="image/png", filename="background.png")


# Confirm quiz panel background image
@router.post("/confirm-quiz-background/", response_model=ResultModel)
def confirm_quiz_background(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        return JSONResponse(content={"message": "Unsupported Media Type", "data": None}, status_code=400)
    # save the file
    with open("static/quizBackground.png", "wb") as f:
        f.write(file.file.read())
    return ResultModel(message="success", data=None)


# Get quiz panel background image
@router.get("/get-quiz-background-image/")
def get_background_image():
    # check if the file exists
    if not os.path.exists("static/quizBackground.png"):
        return JSONResponse(content={"message": "No quiz background image set", "data": None}, status_code=404)
    return FileResponse("static/quizBackground.png", media_type="image/png", filename="quizBackground.png")


@router.post("/set-config/")
def set_config(data: ConfigModel):
    cache["config"] = data
    return ResultModel(message="success", data=None)


@router.get("/get-config/", response_model=ConfigModel)
def get_config():
    config = cache.get("config", None)
    if config is None:
        return JSONResponse(content={"message": "No configuration set", "data": None}, status_code=404)
    return config
