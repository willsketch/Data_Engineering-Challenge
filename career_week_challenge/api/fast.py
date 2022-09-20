import pandas as pd
from io import StringIO
from typing import Union
from fastapi import FastAPI,  UploadFile
from fastapi.responses import FileResponse
from career_week_challenge.interface.main import pred
app = FastAPI()

@app.get('/')
def index():
    return "Your api is local for now"

@app.post("/upload/")
def upload_file(file:  Union[UploadFile, None] = None):
    if not file:
        return FileResponse('raw_data/predicted.csv')
    else:
        #read bytes data
        data = file.file.read()
        #turn bytes into string
        #TODO find more efficient way to d this
        s=str(data,'utf-8')
        #turn it into data frame
        pred_data = pd.read_csv(StringIO(s))
        print(f'#################### {type(pred_data)}##############################')

        pred(pred_data)
        print(f'#################### PREDICTIONS SAVED ##############################')

        return FileResponse('raw_data/predicted.csv')
