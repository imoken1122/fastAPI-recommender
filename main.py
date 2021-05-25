from fastapi import FastAPI
import schemas
from recommender import AnimeRecommenderAPI
import utils 
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
ar = AnimeRecommenderAPI()
ar.load()
origins = [
    "https://arncmd.herokuapp.com",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/recommend" ,response_model=schemas.Prediction)
async def recommend_anime(request: schemas.Data):

    data = utils.convert_title(request.anime_title) 
    print(data)
    preds = ar.recommend(request.model,data, request.num_item) 

    return {"fortitle":request.anime_title,"recommend":preds}