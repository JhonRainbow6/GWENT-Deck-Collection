from fastapi import FastAPI, HTTPException
from model import Card, Deck, DeckCard
from repository import CsvRepository
from typing import List

app = FastAPI(title="Gwent Collection API")

card_repo = CsvRepository('cards.csv', Card)
deck_repo = CsvRepository('decks.csv', Deck)
deck_card_repo = CsvRepository('deck_cards.csv', DeckCard)

#reglas de validacion mazo
def validate_gwent_deck(deck: Deck, deck_cards: list[DeckCard], all_cards: list[Card]) -> str:
    leader = next((c for c in all_cards if c.id == deck.leader_id), None)
    if not leader or leader.type.lower() != "leader":
        return "Error: El leader_id debe pertenecer a una carta de tipo 'Leader'"

    units_count = 0
    specials_count = 0

    for dc in deck_cards:
        card = next((c for c in all_cards if c.id == dc.card_id), None)
        if not card:
            return f"Error: La carta ID {dc.card_id} no existe."

        if card.type == 'Unit':
            units_count += dc.quantity
        elif card.type == 'Special':
            specials_count += dc.quantity

        if hasattr(card, 'faction') and card.faction != deck.faction and card.faction != "Neutral":
            return f"Error: La carta {card.name} no pertenece a la facción."

    if units_count < 22:
        return f"Error: Necesitas al menos 22 cartas de unidad. Tienes {units_count}."
    if specials_count > 10:
        return f"Error: No puedes tener más de 10 cartas especiales. Tienes {specials_count}."

    return "Mazo válido"


# endpoints de cartas
@app.post("/cards", summary="Crear una nueva carta")
def create_card(card: Card):
    card_repo.save(card)
    return {"message": "Carta guardada exitosamente", "card": card}

@app.get("/cards", response_model=List[Card], summary="Obtener todas las cartas")
def get_cards():
    return card_repo.get_all()


