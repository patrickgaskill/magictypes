import json
import re
import csv
from types import SimpleNamespace
from datetime import date

with open('AllPrintings.json', 'r') as jsonfile:
    json_data = jsonfile.read()

data = json.loads(json_data)['data']


def does_card_have_every_creature_type(Card):
    if Card.name == 'Mistform Ultimus':
        return True
    if hasattr(Card, 'keywords') and 'Changeling' in Card.keywords:
        return True
    return False


def sort_key(Card):
    set_model = data[Card.setCode]
    release_date = date.fromisoformat(set_model['releaseDate'])
    parsed_number = int(re.sub(r'[^\d]+', '', Card.number))
    return (release_date, parsed_number, Card.number)


card_firsts = {}

for code, set_model in data.items():
    Set = SimpleNamespace(**set_model)

    if Set.type == 'funny' or Set.type == 'memorabilia' or Set.type == 'promo':
        continue

    if Set.code == 'PAST':
        continue

    for card_model in Set.cards:
        Card = SimpleNamespace(**card_model)

        if Card.borderColor == 'silver':
            continue

        # Handle Mistform Ultimus and changelings
        is_every_creature_type = does_card_have_every_creature_type(Card)

        # Does it add or change types in play or after activation?

        # Does it make any tokens?

        # This only works while changelings have no non-creature subtypes
        if is_every_creature_type:
            key = (tuple(Card.supertypes), tuple(Card.types))
        else:
            key = (tuple(Card.supertypes), tuple(Card.types),
                   tuple(Card.subtypes))

        if key not in card_firsts or sort_key(Card) < sort_key(
                card_firsts[key]):
            card_firsts[key] = Card

with open('card_firsts.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    rows = [(c.type, c.name, c.setCode, c.number)
            for c in sorted(card_firsts.values(), key=sort_key)]
    writer.writerows(rows)
