import json
import types
import re
import datetime
import csv


def load_allprintings():
    with open('AllPrintings.json', 'r') as allprintings_file:
        allprintings_data = allprintings_file.read()
    return json.loads(allprintings_data)['data']


def load_cardtypes():
    with open('CardTypes.json', 'r') as cardtypes_file:
        cardtypes_data = cardtypes_file.read()
    return json.loads(cardtypes_data)['data']


def has_every_creature_type(Card):
    if Card.name == 'Mistform Ultimus':
        return True
    if hasattr(Card, 'keywords') and 'Changeling' in Card.keywords:
        return True
    return False


def sort_key(Card, Set):
    release_date = datetime.date.fromisoformat(Set.releaseDate)
    parsed_number = int(re.sub(r'[^\d]+', '', Card.number))
    return release_date, parsed_number, Card.number


def main():
    allprintings = load_allprintings()
    cardtypes = load_cardtypes()

    card_firsts = {}

    for set_model in allprintings.values():
        Set = types.SimpleNamespace(**set_model)

        if Set.type in ('funny', 'memorabilia', 'promo'):
            continue

        if Set.code == 'PAST':
            continue

        for card_model in Set.cards:
            Card = types.SimpleNamespace(**card_model)

            if Card.borderColor == 'silver':
                continue

            # Split cards, adventure cards?

            # Handle Mistform Ultimus and changelings
            is_every_creature_type = has_every_creature_type(Card)

            # Does it add or change types in play or after activation?

            # Does it make any tokens?

            if is_every_creature_type:
                noncreature_subtypes = tuple(
                    st for st in Card.subtypes
                    if st not in cardtypes['creature']['subTypes'])
                key = (tuple(Card.supertypes), tuple(Card.types),
                       noncreature_subtypes, is_every_creature_type)
            else:
                key = (tuple(Card.supertypes), tuple(Card.types),
                       tuple(Card.subtypes), is_every_creature_type)

            if key not in card_firsts or sort_key(
                    Card, Set) < sort_key(*card_firsts[key]):
                card_firsts[key] = (Card, Set)

    print(len(card_firsts.keys()), 'cards found.')

    with open('card_firsts.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        values = card_firsts.values()
        values.sort(key=lambda v: sort_key(*v))
        rows = [(c.type, c.name, c.setCode, c.number) for (c, _) in values]
        writer.writerows(rows)


if __name__ == '__main__':
    main()