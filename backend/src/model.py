from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List

class Athlete(BaseModel):
    id: int
    name: str
    age: int
    sport: str

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)
    
class Comment(BaseModel):
    name: str
    email: str
    text: str
    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)