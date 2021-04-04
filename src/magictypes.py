import csv
import datetime
import json
import re
from types import SimpleNamespace


class Card(SimpleNamespace):
    @property
    def release_date(self):
        if hasattr(self, "originalReleaseDate"):
            return self.originalReleaseDate

        if hasattr(self, "set"):
            return self.set.releaseDate

        return None

    @property
    def is_every_creature_type(self):
        if "Changeling" in getattr(self, "keywords", []):
            return True

        if self.name == "Mistform Ultimus":
            return True

        return False

    @property
    def sort_key(self):
        release_date = None

        if self.release_date:
            release_date = datetime.date.fromisoformat(self.release_date)

        parsed_number = int(re.sub(r"[^\d]+", "", self.number))
        return release_date, parsed_number, self.number

    @property
    def types_key(self):
        return (
            tuple(self.supertypes),
            tuple(self.types),
            tuple(self.subtypes),
            self.is_every_creature_type,
        )

    @property
    def is_valid(self):
        if "shandalar" in self.availability:
            return False

        if self.layout == "token":
            return False

        if not self.release_date:
            return False

        if getattr(self, "borderColor", "") in ("gold", "silver"):
            return False

        if hasattr(self, "set") and self.set.type in ("funny", "memorabilia", "promo"):
            return False

        return True


def load_cards():
    with open("data/SetList.json", "r") as f:
        sets = json.load(f)

    set_map = {}
    for s in sets["data"]:
        set_map[s["code"]] = SimpleNamespace(**s)

    def object_hook(d):
        if "borderColor" in d:
            if "setCode" in d and d["setCode"] in set_map:
                return Card(**d, set=set_map[d["setCode"]])
            else:
                return Card(**d)
        return d

    with open("data/AllIdentifiers.json", "r") as f:
        return json.load(f, object_hook=object_hook)["data"].values()


def main():
    cards = load_cards()
    card_firsts = {}

    for card in cards:
        if not card.is_valid:
            continue

        k = card.types_key
        if k not in card_firsts or card.sort_key < card_firsts[k].sort_key:
            card_firsts[k] = card

    print(len(card_firsts.keys()), "cards found.")

    with open("data/card_firsts.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        rows = [
            (getattr(c, "type", ""), c.name, getattr(c, "setCode", ""), c.number)
            for c in sorted(card_firsts.values(), key=lambda v: v.sort_key)
        ]
        writer.writerows(rows)


if __name__ == "__main__":
    main()
