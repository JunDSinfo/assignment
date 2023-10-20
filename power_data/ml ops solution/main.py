from fastapi import FastAPI

from forecasting import PowerForcasting, PowerConsumsionForecasting
from preprocess import PreProcess
import datetime
date_format = '%m/%d/%Y'

from typing import Any, Dict, AnyStr, List, Union

app = FastAPI()

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


def train_model(model_path):
    pre_process = PreProcess("power_data.csv")
    train_data, test_data = pre_process.create_test_train_dataset_by_ratio()
    PowerForcasting(train_data, test_data, model_path)
    return "Finished training model"




pcf = PowerConsumsionForecasting()


@app.post("/train")
async def train():
    # tuning not being used at all
    model_path = 'model.json'
    try:
        train_model(model_path)
    except Exception as err:
        print(err)



@app.post("/predict")
async def root(arbitrary_json: JSONStructure = None):

    date_obj = datetime.datetime.strptime(arbitrary_json[0], date_format)
    output = pcf.predict(date_obj)


    return output


