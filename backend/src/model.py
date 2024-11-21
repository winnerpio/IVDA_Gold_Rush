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

class MedalTally(BaseModel):
    edition: str
    edition_id: int
    year: int
    sport: str
    country: str
    country_noc: str
    country_iso2: str
    gold: int
    silver: int
    bronze: int
    total: int

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)
