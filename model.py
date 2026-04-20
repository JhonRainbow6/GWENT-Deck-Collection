from pydantic import BaseModel

class Card(BaseModel):
    id: int
    power: int
    name: str
    type: str
    row: str
    faction: str
    ability: str

