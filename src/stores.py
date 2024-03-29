import csv
from pathlib import Path
from typing import Callable, Optional, Tuple

from magicobjects import MagicObject, TypeKey


class Store:
    def __init__(self, name: str):
        self.store: dict[TypeKey, MagicObject] = {}
        self.name = name

    def evaluate(self, obj: MagicObject) -> bool:
        # if apply_effects and callable(self.effects):
        #     for affected_card in self.effects(obj):
        #         self.evaluate(affected_card, False)

        self.store[obj.type_key] = True

        return False

    def write_csv(self, output_path: Path) -> str:
        csv_path = output_path / (self.name.replace(" ", "_") + ".csv")
        with csv_path.open("w") as csvfile:
            writer = csv.writer(csvfile)

            if any(obj.is_token for obj in self.store.values()):
                writer.writerow(
                    [
                        "Types",
                        "Token Name",
                        "Card Name",
                        "Set Code",
                        "Number",
                        "Release Date",
                    ]
                )
            else:
                writer.writerow(
                    ["Types", "Card Name", "Set Code", "Number", "Release Date"]
                )

            rows = [
                (
                    obj.type_str,
                    obj.name,
                    obj.creator.name,
                    obj.creator.set_code,
                    obj.creator.number,
                    obj.creator.release_date,
                )
                if obj.is_token
                else (
                    obj.type_str,
                    obj.name,
                    obj.set_code,
                    obj.number,
                    obj.release_date,
                )
                for obj in sorted(self.store.values(), key=lambda obj: obj.sort_key)
            ]
            writer.writerows(rows)
        return csv_path

    def write_decklist(self, output_path: Path) -> str:
        decklist_path = output_path / (self.name.replace(" ", "_") + "_decklist.txt")
        with decklist_path.open("w") as decklistfile:
            for card in self.store.values():
                decklistfile.write(f"1 [{card.set_code}] {card.name}\n")
        return decklist_path

    def __len__(self) -> int:
        return len(self.store.keys())


class UniqueStore(Store):
    def evaluate(self, obj: MagicObject) -> bool:
        # if apply_effects and callable(self.effects):
        #     for affected_card in self.effects(obj):
        #         self.evaluate(affected_card, False)

        if (
            obj.type_key not in self.store
            or obj.sort_key < self.store[obj.type_key].sort_key
        ):
            self.store[obj.type_key] = obj
            return True

        return False


class MaximalStore(Store):
    def __init__(self, name: str):
        super().__init__(name)
        self.eliminated_keys: dict[TypeKey, MagicObject] = {}

    def evaluate(self, obj: MagicObject) -> bool:
        # if apply_effects and callable(self.effects):
        #     for affected_card in self.effects(obj):
        #         self.evaluate(affected_card, False)

        if obj.type_key in self.eliminated_keys:
            return False

        # If the type already exists, replace it only if this card is older
        if obj.type_key in self.store:
            if obj.sort_key < self.store[obj.type_key].sort_key:
                self.store[obj.type_key] = obj
                return True
            return False

        # If card is a subset to any saved card then bail out
        # If any saved keys are a subset to this card, delete those keys
        keys_to_delete = []
        for other_key, other in self.store.items():
            if obj.is_type_subset(other):
                return False

            if other.is_type_subset(obj):
                keys_to_delete.append(other_key)

        for key in keys_to_delete:
            self.eliminated_keys[key] = True
            del self.store[key]

        self.store[obj.type_key] = obj
        return True


class UniquePowerToughnessStore(Store):
    def __init__(self, name: str):
        super().__init__(name)
        self.store: dict[Tuple[int, int], MagicObject] = {}

    def evaluate(self, obj: MagicObject) -> bool:
        if (
            obj.power is None
            or not obj.power.isdigit()
            or obj.toughness is None
            or not obj.toughness.isdigit()
        ):
            return False

        key = (int(obj.power), int(obj.toughness))

        if key in self.store:
            if obj.sort_key < self.store[key].sort_key:
                self.store[key] = obj
                return True
            return False

        self.store[key] = obj
        return True

    def write_csv(self, output_path: Path) -> str:
        csv_path = output_path / (self.name.replace(" ", "_") + ".csv")
        with csv_path.open("w") as csvfile:
            writer = csv.writer(csvfile)

            if any(obj.is_token for obj in self.store.values()):
                writer.writerow(
                    [
                        "Power",
                        "Toughness",
                        "Token Name",
                        "Card Name",
                        "Set Code",
                        "Number",
                        "Release Date",
                    ]
                )
            else:
                writer.writerow(
                    [
                        "Power",
                        "Toughness",
                        "Card Name",
                        "Set Code",
                        "Number",
                        "Release Date",
                    ]
                )

            rows = [
                (
                    obj.power,
                    obj.toughness,
                    obj.name,
                    obj.creator.name,
                    obj.creator.set_code,
                    obj.creator.number,
                    obj.creator.release_date,
                )
                if obj.is_token
                else (
                    obj.power,
                    obj.toughness,
                    obj.name,
                    obj.set_code,
                    obj.number,
                    obj.release_date,
                )
                for obj in sorted(self.store.values(), key=lambda obj: obj.sort_key)
            ]
            writer.writerows(rows)
        return csv_path
