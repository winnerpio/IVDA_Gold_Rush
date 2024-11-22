from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List

class Athlete(BaseModel):
    id: int
    name: str
    country: str
    age: int
    sex: str
    height: int
    weight: int
    bmi: int
    h2w: int
    edition_id: int
    sport: str
    event: str
    medal: str

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)
    
class Comment(BaseModel):
    name: str
    email: str
    text: str
    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

class WorldHistory(BaseModel):
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
