import csv
import json
from pathlib import Path
from types import SimpleNamespace
from card import Card


def load_cards():
    with Path("../data/SetList.json").resolve().open() as f:
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

    with Path("../data/AllIdentifiers.json").resolve().open() as f:
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

    print(len(card_firsts.keys()), "cards found")

    with Path("../data/card_firsts.csv").resolve().open("w") as csvfile:
        writer = csv.writer(csvfile)
        rows = [
            (getattr(c, "type", ""), c.name, getattr(c, "setCode", ""), c.number)
            for c in sorted(card_firsts.values(), key=lambda v: v.sort_key)
        ]
        writer.writerows(rows)


if __name__ == "__main__":
    main()
