import csv
import os
from typing import List, TypeVar, Type
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class CsvRepository:
    def __init__(self, filename: str, model: Type[T]):
        self.filename = filename
        self.model = model
        self.fieldnames = list(model.model_fields.keys())
        self._init_file()

    def _init_file(self):
        if not os.path.isfile(self.filename):
            with open(self.filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.fieldnames)

    def save(self, item: T):
        with open(self.filename, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(item.model_dump())

    def get_all(self) -> List[T]:
        items = []
        with open(self.filename, mode='r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                items.append(self.model(**row))
        return items

    def delete(self, **conditions):
        items = self.get_all()
        items_to_keep = []
        for item in items:
            match = all(str(getattr(item, k)) == str(v) for k, v in conditions.items())
            if not match:
                items_to_keep.append(item)

        with open(self.filename, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            for item in items_to_keep:
                writer.writerow(item.model_dump())