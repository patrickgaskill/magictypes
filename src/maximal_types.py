import csv
import json
import time
from copy import deepcopy
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

basic_land_types = ("Forest", "Island", "Mountain", "Plains", "Swamp")


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


CardTypesKey = tuple[tuple[str], tuple[str], tuple[str], bool]


def update_maximals(card: Card, maximal: dict[CardTypesKey, Card], eliminated_keys: list[CardTypesKey]) -> None:
    if not card.is_valid or card.types_key in eliminated_keys:
        return

    # if the type already exists replace it only if this card is older
    if card.types_key in maximal:
        if card.sort_key < maximal[card.types_key].sort_key:
            maximal[card.types_key] = card
        return

    # if card is a subset to any saved card go to next card
    if any(is_type_subset(card, v) for v in maximal.values()):
        return

    # if keys are a subset to card, delete those keys
    keys_to_delete = [
        k for k, v in maximal.items() if is_type_subset(v, card)]
    for key in keys_to_delete:
        eliminated_keys[key] = True
        del maximal[key]

    maximal[card.types_key] = card


def write_cards_to_csv(cards: list[Card], filename: str) -> None:
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{filename}-{timestr}.csv"
    with data_file(filename).open("w") as csvfile:
        writer = csv.writer(csvfile)
        rows = [
            (getattr(c, "type", ""), c.name, getattr(c, "setCode", ""),
             c.number, c.release_date)
            for c in sorted(cards.values(), key=lambda v: v.sort_key)
        ]
        writer.writerows(rows)


def format_type(card: Card) -> str:
    subtypes = card.subtypes

    has_all_basic_land_types = False
    if set(basic_land_types) <= set(card.subtypes):
        has_all_basic_land_types = True
        subtypes = list(set(subtypes).difference(basic_land_types))

    has_all_creature_types = False
    if set(all_creature_types) <= set(card.subtypes) or card.is_every_creature_type:
        has_all_creature_types = True
        subtypes = list(set(subtypes).difference((all_creature_types)))

    formatted = " ".join(card.types)
    if len(card.supertypes) > 0:
        formatted = f"{' '.join(card.supertypes)} {formatted}"

    if has_all_basic_land_types:
        subtypes = ["(all basic land types)"] + subtypes

    if has_all_creature_types:
        subtypes = ["(all creature types)"] + subtypes

    if len(subtypes) > 0:
        formatted = f"{formatted} — {' '.join(subtypes)}"

    return formatted


def union_lists(a: list[any], b: list[any]) -> list[any]:
    return sorted(list(set(a).union(b)))


def is_permanent(card: Card) -> bool:
    return any(t in card.types for t in ("Artifact", "Creature", "Enchantment", "Land", "Planeswalker"))


def add_supertypes(card: Card, new_supertypes: list[str]) -> None:
    card.supertypes = union_lists(
        card.supertypes, new_supertypes)


def add_types(card: Card, new_types: list[str]) -> None:
    card.types = union_lists(
        card.types, new_types)


def add_subtypes(card: Card, new_subtypes: list[str]) -> None:
    card.subtypes = union_lists(
        card.subtypes, new_subtypes)


def modify_card_in_play(card: Card) -> list[Card]:
    returned_cards = [deepcopy(card)]

    # Moritte of the Frost is a copy so doesn't see the following type-changing effects
    if is_permanent(card):
        moritte_copy = deepcopy(card)
        add_supertypes(moritte_copy, ["Legendary", "Snow"])
        if "Creature" in moritte_copy.types:
            add_subtypes(moritte_copy, all_creature_types)
        returned_cards.append(moritte_copy)

    # Dermotaxi (copy creature from GY and add Vehicle artifact)
    if "Creature" in card.types:
        dermotaxi_copy = deepcopy(card)
        add_types(dermotaxi_copy, ["Artifact"])
        add_subtypes(dermotaxi_copy, ["Vehicle"])
        returned_cards.append(dermotaxi_copy)

    for card_in_play in returned_cards:
        # Enchanted Evening (all permanents are enchantments)
        if is_permanent(card_in_play):
            add_types(card_in_play, ["Enchantment"])

        # Memnarch (permanent becomes an artifact)
        if is_permanent(card_in_play):
            add_types(card_in_play, ["Artifact"])

        # Ensoul Artifact (artifact is a creature)
        if "Artifact" in card_in_play.types:
            add_types(card_in_play, ["Creature"])

        # Maskwood Nexus (creature gets all creature types)
        if "Creature" in card_in_play.types:
            add_subtypes(card_in_play, all_creature_types)

        # In Bolas's Clutches (permanent becomes legendary)
        if is_permanent(card_in_play):
            add_supertypes(card_in_play, ["Legendary"])

        # Ashaya, Soul of the Wild (nontoken creatures are Forest lands)
        if "Creature" in card_in_play.types:
            add_types(card_in_play, ["Land"])
            add_subtypes(card_in_play, ["Forest"])

        # Prismatic Omen (lands are every basic land type)
        if "Land" in card_in_play.types:
            add_subtypes(card_in_play, basic_land_types)

        card_in_play.type = format_type(card_in_play)
        card_in_play.__dict__["types_key"] = (
            tuple(card_in_play.supertypes),
            tuple(card_in_play.types),
            tuple(card_in_play.subtypes),
        )

    return returned_cards


def main() -> None:
    cards = load_cards()
    maximal_cards = {}
    eliminated_card_keys = {}
    maximal_in_play = {}
    eliminated_in_play_keys = {}

    for card in Bar("Processing").iter(cards):
        update_maximals(card, maximal_cards, eliminated_card_keys)

        for card_in_play in modify_card_in_play(card):
            update_maximals(card_in_play, maximal_in_play,
                            eliminated_in_play_keys)

    print("•", len(maximal_cards.keys()), "cards found")
    write_cards_to_csv(maximal_cards, "maximal_cards")

    print("•", len(maximal_in_play.keys()), "cards in play found")
    write_cards_to_csv(maximal_in_play, "maximal_in_play")


if __name__ == "__main__":
    main()
