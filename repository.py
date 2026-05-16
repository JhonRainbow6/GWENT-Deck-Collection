from sqlalchemy.orm import Session
from typing import List, TypeVar, Type


T = TypeVar('T')


class DBRepository:
    def __init__(self, model: Type[T]):
        self.model = model

    def save(self, db: Session, item_data: dict):
        db_item = self.model(**item_data)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def get_all(self, db: Session) -> List[T]:
        return db.query(self.model).all()

    def delete(self, db: Session, **conditions):
        query = db.query(self.model)
        for key, value in conditions.items():
            query = query.filter(getattr(self.model, key) == value)

        deleted_count = query.delete()
        db.commit()
        return deleted_count