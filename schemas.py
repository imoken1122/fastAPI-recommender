from pydantic import BaseModel
from typing import List

class Data(BaseModel):
    anime_title:str
    num_item:int
    model:str

class Output(BaseModel):
    rank:int 
    recommend_title:str
    score:float

class Prediction(BaseModel):
    fortitle:str
    recommend:List[Output]