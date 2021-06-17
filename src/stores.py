import csv
from pathlib import Path

from magicobjects import MagicObject, TypeKey


class UniqueStore:
    def __init__(self, name: str):
        self.store: dict[TypeKey, MagicObject] = {}
        self.name: str = name

    def evaluate(self, card: MagicObject) -> bool:
        if (
            card.type_key not in self.store
            or card.sort_key < self.store[card.type_key].sort_key
        ):
            self.store[card.type_key] = card
            return True

        return False

    def write_csv(self, output_path: Path) -> str:
        csv_path = output_path / (self.name.replace(" ", "_") + ".csv")
        with csv_path.open("w") as csvfile:
            writer = csv.writer(csvfile)
            rows = [
                (
                    card.type_str,
                    card.name,
                    card.set_code,
                    card.number,
                    card.release_date,
                )
                for card in sorted(self.store.values(), key=lambda card: card.sort_key)
            ]
            writer.writerows(rows)
        return csv_path

    def write_decklist(self, output_path: Path) -> str:
        decklist_path = output_path / (self.name.replace(" ", "_") + "_decklist.txt")
        with decklist_path.open("w") as decklistfile:
            for card in self.store.values():
                decklistfile.write(f"1 {card.name} [{card.set_code}] {card.number}\n")
        return decklist_path

    @property
    def count(self) -> int:
        return len(self.store.keys())


class MaximalStore(UniqueStore):
    def __init__(self, name: str):
        super().__init__(name)
        self.eliminated_keys: dict[TypeKey, MagicObject] = {}

    def evaluate(self, card: MagicObject) -> bool:
        if card.type_key in self.eliminated_keys:
            return False

        # if the type already exists replace it only if this card is older
        if card.type_key in self.store:
            if card.sort_key < self.store[card.type_key].sort_key:
                self.store[card.type_key] = card
                return True
            return False

        # if card is a subset to any saved card then bail out
        # if keys are a subset to card, delete those keys
        keys_to_delete = []
        for other_key, other in self.store.items():
            if card.is_type_subset(other):
                return False

            if other.is_type_subset(card):
                keys_to_delete.append(other_key)

        for key in keys_to_delete:
            self.eliminated_keys[key] = True
            del self.store[key]

        self.store[card.type_key] = card
        return True
