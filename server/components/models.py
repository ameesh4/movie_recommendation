from pydantic import BaseModel

class response(BaseModel):
    id: int
    title: str
    genre_names: list
    release_date: str
    overview: str
    poster_path: str
    vote_average: float
