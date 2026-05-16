from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from model import Card, Deck, DeckCard, DBCard, DBDeck, DBDeckCard
from repository import DBRepository
from database import engine, Base, get_db
from typing import List, Optional

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gwent Collection API")

card_repo = DBRepository(DBCard)
deck_repo = DBRepository(DBDeck)
deck_card_repo = DBRepository(DBDeckCard)

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
def create_card(card: Card, db:Session = Depends(get_db)):
    card_repo.save(db, item_data=card.model_dump())
    return {"message": "Carta guardada exitosamente", "card": card}

@app.get("/cards", response_model=List[Card], summary="Obtener todas las cartas o filtarlas")
def get_cards(
        id: Optional[int] = None,
        faction: Optional[str] = None,
        type: Optional[str] = None,
        power: Optional[int] = None,
        row: Optional[str] = None,
        db: Session = Depends(get_db)
):
    query = db.query(DBCard)
    if id is not None:
        query = query.filter(DBCard.id == id)
    if faction:
        query = query.filter(DBCard.faction.ilike(faction))
    if type:
        query = query.filter(DBCard.type.ilike(type))
    if power is not None:
        query = query.filter(DBCard.power == power)
    if row:
        query = query.filter(DBCard.row.ilike(row))

    return query.all()

@app.delete("/cards/{card_id}", summary = "Eliminar carta por ID")
def delete_card(card_id: int, db: Session = Depends(get_db)):
    deck_card_repo.delete(db, card_id=card_id)  # eliminar en mazos
    card_repo.delete(db,id=card_id)  # eliminar la carta
    return {"message": f"Carta {card_id} y sus referencias en mazos han sido eliminado."}

#endpoints de mazos
@app.post("/decks", summary="Crear una nueva baraja")
def create_deck(deck: Deck, db: Session = Depends(get_db)):
    deck_repo.save(db, item_data=deck.model_dump())
    return {"message": "Baraja creada", "deck": deck}

@app.delete("/decks/{deck_id}", summary="Eliminar una baraja")
def delete_deck(deck_id: int, db: Session = Depends(get_db)):
    # eliminar la baraja con sus cartas
    deck_repo.delete(db ,id=deck_id)
    deck_card_repo.delete(db, deck_id=deck_id)
    return {"message": f"Baraja {deck_id} y sus cartas han sido eliminadas."}

#endpoints de cartas en mazo
@app.post("/decks/cards", summary="Añadir cartas a una baraja")
def add_card_to_deck(deck_card: DeckCard, db: Session = Depends(get_db)):
    deck_card_repo.save(db, item_data=deck_card.model_dump())
    return {"message": "Carta(s) agregada(s) a la baraja", "deck_card": deck_card}

@app.get("/decks/{deck_id}/cards", summary="Obtener las cartas de una baraja específica")
def get_cards_from_deck(deck_id: int, db:Session = Depends(get_db)):
    decks = deck_repo.get_all(db)
    deck = next((d for d in decks if d.id == deck_id), None)
    if not deck:
        raise HTTPException(status_code=404, detail="Baraja no encontrada")
    deck_cards = [dc for dc in deck_card_repo.get_all(db) if dc.deck_id == deck_id]
    all_cards = {c.id: c for c in card_repo.get_all(db)}
    result = []
    for dc in deck_cards:
        card = all_cards.get(dc.card_id)
        if card:
            card_data = {
                "id": card.id,
                "power": card.power,
                "name": card.name,
                "type": card.type,
                "row": card.row,
                "faction": card.faction,
                "ability": card.ability,
                "quantity": dc.quantity
            }
            result.append(card_data)

    return result

@app.delete("/decks/{deck_id}/cards/{card_id}", summary="Eliminar carta de una baraja")
def remove_card_from_deck(deck_id: int, card_id: int, db:Session = Depends(get_db)):
    deck_card_repo.delete(db, deck_id=deck_id, card_id=card_id)
    return {"message": f"Carta {card_id} eliminada de la baraja {deck_id}."}

# endpoints validacion de mazo
@app.get("/decks/{deck_id}/validate", summary="Validar si una baraja cumple las reglas")
def validate_deck_endpoint(deck_id: int, db: Session = Depends(get_db)):
    decks = deck_repo.get_all(db)
    deck = next((d for d in decks if d.id == deck_id), None)
    if not deck:
        raise HTTPException(status_code=404, detail="Baraja no encontrada")

    deck_cards = [dc for dc in deck_card_repo.get_all(db) if dc.deck_id == deck_id]
    all_cards = card_repo.get_all(db)

    resultado = validate_gwent_deck(deck, deck_cards, all_cards)
    return {"validacion": resultado}

