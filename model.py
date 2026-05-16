from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

#modelos neon
class DBCard(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    power = Column(Integer)
    name = Column(String)
    type = Column(String)
    row = Column(String)
    faction = Column(String)
    ability = Column(String)

class DBDeck(Base):
    __tablename__ = "decks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    faction = Column(String)
    leader_id = Column(Integer)

class DBDeckCard(Base):
    __tablename__ = "deck_cards"
    deck_id = Column(Integer, primary_key=True)
    card_id = Column(Integer, primary_key=True)
    quantity = Column(Integer)


#esquemas Api
class Card(BaseModel):
    id: int
    power: int
    name: str
    type: str
    row: str
    faction: str
    ability: str
    class Config: from_attributes = True

class Deck(BaseModel):
    id: int
    name: str
    faction: str
    leader_id: int
    class Config: from_attributes = True

class DeckCard(BaseModel):
    deck_id: int
    card_id: int
    quantity: int
    class Config: from_attributes = True