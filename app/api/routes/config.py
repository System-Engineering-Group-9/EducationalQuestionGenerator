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
    return QuestionsModel(questions=cache.get("questions", []))


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
