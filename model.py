from pydantic import BaseModel

class Card(BaseModel):
    id: int
    power: int
    name: str
    type: str
    row: str
    faction: str
    ability: str

class Deck(BaseModel):
    id: int
    name: str
    faction: str
    leader_id: int

class DeckCard(BaseModel):
    deck_id: int
    card_id: int
    quantity: int
