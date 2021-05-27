import csv
import json
from progress.bar import Bar
from magictypes import load_cards, data_file
from card import Card


def load_creature_types() -> list[str]:
    with data_file("CardTypes.json").open() as f:
        card_types_data = json.load(f)["data"]
    creature_types = card_types_data["creature"]["subTypes"]
    # mtgjson includes some illegal creature types
    for subtype in ("Chicken", "Head", "Hornet", "Reveler", "Rukh", "Wasp"):
        creature_types.remove(subtype)
    return creature_types


all_creature_types = set(load_creature_types())


def is_type_subset(a: Card, b: Card) -> bool:
    a_supertypes = set(a.supertypes)
    a_types = set(a.types)
    a_subtypes = set(a.subtypes).union(
        all_creature_types) if a.is_every_creature_type else set(a.subtypes)
    b_supertypes = set(b.supertypes)
    b_types = set(b.types)
    b_subtypes = set(b.subtypes).union(
        all_creature_types) if b.is_every_creature_type else set(b.subtypes)

    if a_supertypes < b_supertypes and a_types <= b_types and a_subtypes <= b_subtypes:
        return True

    if a_supertypes <= b_supertypes and a_types < b_types and a_subtypes <= b_subtypes:
        return True

    if a_supertypes <= b_supertypes and a_types <= b_types and a_subtypes < b_subtypes:
        return True

    return False


def main() -> None:
    cards = load_cards()
    maximal_cards = {}
    eliminated_keys = {}

    for card in Bar("Processing").iter(cards):
        if not card.is_valid or card.types_key in eliminated_keys:
            continue

        # if the type already exists replace it only if this card is older
        if card.types_key in maximal_cards:
            if card.sort_key < maximal_cards[card.types_key].sort_key:
                maximal_cards[card.types_key] = card
            continue

        # if card is a subset to any saved card go to next card
        if any(is_type_subset(card, v) for v in maximal_cards.values()):
            continue

        # if keys are a subset to card, delete those keys
        keys_to_delete = [
            k for k, v in maximal_cards.items() if is_type_subset(v, card)]
        for key in keys_to_delete:
            eliminated_keys[key] = True
            del maximal_cards[key]

        maximal_cards[card.types_key] = card

    print(len(maximal_cards.keys()), "cards found")

    # for card in sorted(maximal.values(), key=lambda v: v.sort_key):
    #     if hasattr(card, "set") and card.set.type == "promo":
    #         print(getattr(card, "type", ""), card.name,
    #               getattr(card, "setCode", ""))

    with data_file("maximal_combinations_cards.csv").open("w") as csvfile:
        writer = csv.writer(csvfile)
        rows = [
            (getattr(c, "type", ""), c.name, getattr(c, "setCode", ""),
             c.number, c.release_date)
            for c in sorted(maximal_cards.values(), key=lambda v: v.sort_key)
        ]
        writer.writerows(rows)


if __name__ == "__main__":
    main()
