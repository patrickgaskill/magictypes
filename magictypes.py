import csv
import datetime
import itertools
import json
import re
from types import SimpleNamespace


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


def make_token_pattern(cardtypes):
    colors = '|'.join(
        ['white', 'blue', 'black', 'red', 'green', 'colorless', 'and'])
    numbers = '|'.join([
        'an?', r'a\ number\ of', 'X', 'two', 'three', 'four', 'five', 'six',
        'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen'
    ])
    types = '|'.join(cardtypes.keys())
    supertypes = '|'.join(cardtypes['artifact']['superTypes'])
    subtypes = '|'.join(
        itertools.chain(*[v['subTypes'] for v in cardtypes.values()]))

    pattern = re.compile(
        rf"""create\s
             (?:(?P<legendary_name>[^,]+),\s)?
             (?:{numbers})\s
             (?:tapped\s)?
             (?P<supertypes>(?:(?:{supertypes})\s)+)?
             (?:(?P<power>[\dX*]+)\/(?P<toughness>[\dX*]+)\s)?
             (?P<colors1>(?:(?:{colors})\s)+)?
             (?P<subtypes>(?:(?:{subtypes})\s)+)?
             (?P<types>(?:(?:{types})\s)+)
             tokens?
             (?:\ that’s\ (?P<colors2>(?:(?:{colors})[., ]+)+))?""",
        re.IGNORECASE | re.VERBOSE)
    return pattern


def extract_tokens(Card, pattern):
    if (Card.name == 'Master of the Wild Hunt Avatar'):
        return [
            SimpleNamespace(types=['Creature'],
                            subtypes=['Wolf'],
                            supertypes=[]),
            SimpleNamespace(types=['Creature'],
                            subtypes=['Antelope'],
                            supertypes=[]),
            SimpleNamespace(types=['Creature'],
                            subtypes=['Cat'],
                            supertypes=[]),
            SimpleNamespace(types=['Creature'],
                            subtypes=['Rhino'],
                            supertypes=[])
        ]

    if not hasattr(Card, 'text'):
        return []

    matches = re.findall(pattern, Card.text)
    tokens = []
    for m in matches:
        _, supertypes, _, _, _, subtypes, types, _ = m

        types_list = [t.capitalize() for t in types.strip().split(' ')
                      ] if len(types) > 0 else []
        subtypes_list = [s.capitalize() for s in subtypes.strip().split(' ')
                         ] if len(subtypes) > 0 else []
        supertypes_list = [
            s.capitalize() for s in supertypes.strip().split(' ')
        ] if len(supertypes) > 0 else []

        tokens.append(
            SimpleNamespace(types=types_list,
                            subtypes=subtypes_list,
                            supertypes=supertypes_list))

    if re.search(r'create a Food token', Card.text, re.IGNORECASE):
        tokens.append(
            SimpleNamespace(types=['Artifact'],
                            subtypes=['Food'],
                            supertypes=[]))

    return tokens


def sort_key(Card, Set):
    release_date = datetime.date.fromisoformat(Set.releaseDate)
    parsed_number = int(re.sub(r'[^\d]+', '', Card.number))
    return release_date, parsed_number, Card.number


def main():
    allprintings = load_allprintings()
    cardtypes = load_cardtypes()
    token_pattern = make_token_pattern(cardtypes)
    card_firsts = {}
    token_firsts = {}

    for set_model in allprintings.values():
        Set = SimpleNamespace(**set_model)

        if Set.type in ('funny', 'memorabilia', 'promo'):
            continue

        if Set.code == 'PAST':
            continue

        for card_model in Set.cards:
            Card = SimpleNamespace(**card_model)

            if Card.borderColor == 'silver':
                continue

            # Split cards, adventure cards?

            # Handle Mistform Ultimus and changelings
            is_every_creature_type = has_every_creature_type(Card)

            # Does it add or change types in play or after activation?

            # Does it make any tokens?
            tokens = extract_tokens(Card, token_pattern)
            for token in tokens:
                key = (tuple(token.supertypes), tuple(token.types),
                       tuple(token.subtypes))
                if key not in token_firsts or sort_key(Card, Set) < sort_key(
                        token_firsts[key][1], token_firsts[key][2]):
                    token_firsts[key] = (token, Card, Set)

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
        rows = [(c.type, c.name, c.setCode, c.number)
                for c, _ in sorted(card_firsts.values(),
                                   key=lambda v: sort_key(*v))]
        writer.writerows(rows)

    print(len(token_firsts.keys()), 'tokens found.')

    with open('token_firsts.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        rows = [(t.types, t.subtypes, t.supertypes, c.name, c.setCode,
                 c.number)
                for t, c, _ in sorted(token_firsts.values(),
                                      key=lambda v: sort_key(v[1], v[2]))]
        writer.writerows(rows)


if __name__ == '__main__':
    main()