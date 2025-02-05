import os
from app.models.resultModel import ResultModel
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse

from app.models.questionModel import QuestionsModel

router = APIRouter(prefix="/config", tags=["config"])


# Confirm Questions by CSV file
@router.post("/confirm-by-csv/", response_model=ResultModel)
def confirm_by_csv(file: UploadFile = File(...)):
    if not file.content_type.startswith("text/csv"):
        return JSONResponse(content={"message": "Unsupported Media Type", "data":None}, status_code=400)
    # save the file
    with open("static/output.csv", "wb") as f:
        f.write(file.file.read())
    return ResultModel(message="success", data=None)

@router.post("/confirm-by-json/")
def confirm_by_json(data: QuestionsModel):
    # turn the data into a csv file
    csvHeader = ['question', 'choice A', 'choice B', 'choice C', 'choice D', 'answer']
    file = open("static/output.csv", "w")
    file.write(",".join(csvHeader)+'\n')
    for question in data.questions:
        file.write(",".join(question.__dict__.values())+'\n')
    file.close()
    return ResultModel(message="success", data=None)

@router.get("/get-questions/")
def get_questions():
    # check if the file exists
    if not os.path.exists("static/output.csv"):
        return JSONResponse(content={"message": "No questions set", "data":None}, status_code=404)
    return FileResponse("static/output.csv")