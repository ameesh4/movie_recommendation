from fastapi import FastAPI
from components.utils import title_fetch, recommend
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from components.models import response

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/{title}")
async def movie_fetch(title: str):
    try:
        response = title_fetch(title)
    except Exception as e:
        return {"error": str(e)}
    
    return response

@app.post('/recommend')
async def selection(selected: list[response]):
    try:
        recommended = recommend(selected)
        return recommended
    except e:
        return {"error": str(e)}
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)