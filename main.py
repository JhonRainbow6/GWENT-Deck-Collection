from fastapi import FastAPI
from model import Card
from repository import CsvRepository
from typing import List

app = FastAPI(title="Gwent Collection API")

card_repo = CsvRepository('cards.csv', Card)



# endpoints de cartas
@app.post("/cards", summary="Crear una nueva carta")
def create_card(card: Card):
    card_repo.save(card)
    return {"message": "Carta guardada exitosamente", "card": card}

@app.get("/cards", response_model=List[Card], summary="Obtener todas las cartas")
def get_cards():
    return card_repo.get_all()


