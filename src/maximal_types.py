import csv
import json
import time
from copy import deepcopy
from progress.bar import Bar
from magictypes import load_cards, data_file
from card import Card
from magic_objects.token import MagicToken
from lark_token_extractor import TokenExtractor


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
        all_creature_types) if getattr(a, "is_every_creature_type", False) else set(a.subtypes)
    b_supertypes = set(b.supertypes)
    b_types = set(b.types)
    b_subtypes = set(b.subtypes).union(
        all_creature_types) if getattr(b, "is_every_creature_type", False) else set(b.subtypes)

    if a_supertypes < b_supertypes and a_types <= b_types and a_subtypes <= b_subtypes:
        return True

    if a_supertypes <= b_supertypes and a_types < b_types and a_subtypes <= b_subtypes:
        return True

    if a_supertypes <= b_supertypes and a_types <= b_types and a_subtypes < b_subtypes:
        return True

    return False


CardTypesKey = tuple[tuple[str], tuple[str], tuple[str], bool]


def update_maximals(card: Card, maximal: dict[CardTypesKey, Card], eliminated_keys: list[CardTypesKey]) -> None:
    if (card.object == "card" and not card.is_valid) or card.types_key in eliminated_keys:
        return

    # if the type already exists replace it only if this card is older
    if card.types_key in maximal and hasattr(card, "sort_key"):
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
             getattr(c, "number", ""), getattr(c, "release_date", ""))
            for c in sorted(cards, key=lambda v: getattr(v, "sort_key", v.type))
        ]
        writer.writerows(rows)


supertype_order: dict[str, int] = {

}

type_order: dict[str, int] = {
    "Tribal": 0,
    "Enchantment": 1,
    "Artifact": 2,
    "Land": 3,
    "Planeswalker": 4,
    "Creature": 5,
}


def sort_types(types: list[str]) -> list[str]:
    return sorted(types, key=lambda t: type_order[t] if t in type_order else 0)


subtype_order: dict[str, int] = {
    "Aura": 0,
    "Cartouche": 1,
    "Rune": 1,
    "Curse": 1,

    "Urza's": 0,
    "Mine": 1,
    "Tower": 1,
    "Power-Plant": 1,
    "Saga": 1
}


def sort_subtypes(subtypes: list[str]) -> list[str]:
    return sorted(subtypes, key=lambda t: subtype_order[t] if t in subtype_order else 0)


def format_type(card: Card) -> str:
    subtypes = card.subtypes

    has_all_basic_land_types = False
    if set(basic_land_types) <= set(card.subtypes):
        has_all_basic_land_types = True
        subtypes = list(set(subtypes).difference(basic_land_types))

    has_all_creature_types = False
    if set(all_creature_types) <= set(card.subtypes) or getattr(card, "is_every_creature_type", False):
        has_all_creature_types = True
        subtypes = list(set(subtypes).difference((all_creature_types)))

    formatted = " ".join(sort_types(card.types))
    if len(card.supertypes) > 0:
        formatted = f"{' '.join(card.supertypes)} {formatted}"

    subtypes = sort_subtypes(subtypes)

    if has_all_basic_land_types:
        subtypes.append("(all basic land types)")

    if has_all_creature_types:
        subtypes.append("(all creature types)")

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
    if getattr(card, "object", "") != "token" and "Creature" in card.types:
        dermotaxi_copy = deepcopy(card)
        add_types(dermotaxi_copy, ["Artifact"])
        add_subtypes(dermotaxi_copy, ["Vehicle"])
        returned_cards.append(dermotaxi_copy)

    for card_in_play in returned_cards:
        # Life and Limb (All Forests and all Saprolings are 1/1 green Saproling creatures and Forest lands in addition to their other types)
        # if "Forest" in card_in_play.subtypes or "Saproling" in card_in_play.subtypes:
        #     add_types(card_in_play, ["Creature", "Land"])
        #     add_subtypes(card_in_play, ["Saproling", "Forest"])

        # Enchanted Evening (all permanents are enchantments)
        if is_permanent(card_in_play):
            add_types(card_in_play, ["Enchantment"])

        # Mycosynth Lattice (all permanents are artifacts)
        if is_permanent(card_in_play):
            add_types(card_in_play, ["Artifact"])

        # March of the Machines (all noncreature artifacts are creatures)
        if "Artifact" in card_in_play.types and "Creature" not in card_in_play.types:
            add_types(card_in_play, ["Creature"])

        # Maskwood Nexus (creature gets all creature types)
        if "Creature" in card_in_play.types:
            add_subtypes(card_in_play, all_creature_types)

        # In Bolas's Clutches (permanent becomes legendary)
        if is_permanent(card_in_play):
            add_supertypes(card_in_play, ["Legendary"])

        # Ashaya, Soul of the Wild (nontoken creatures are Forest lands)
        # if getattr(card, "object", "") != "token" and "Creature" in card_in_play.types:
        #     add_types(card_in_play, ["Land"])
        #     add_subtypes(card_in_play, ["Forest"])

        # Prismatic Omen (lands are every basic land type)
        # if "Land" in card_in_play.types:
        #     add_subtypes(card_in_play, basic_land_types)

        # Life and Limb (All Forests and all Saprolings are 1/1 green Saproling creatures and Forest lands in addition to their other types)
        if "Forest" in card_in_play.subtypes or "Saproling" in card_in_play.subtypes:
            add_types(card_in_play, ["Creature", "Land"])
            add_subtypes(card_in_play, ["Saproling", "Forest"])

        # Prismatic Omen (lands are every basic land type)
        if "Land" in card_in_play.types:
            add_subtypes(card_in_play, basic_land_types)

        # Rimefeather Owl (permanents with ice counters are snow)
        if is_permanent(card_in_play):
            add_supertypes(card_in_play, ["Snow"])

        card_in_play.type = format_type(card_in_play)
        card_in_play.__dict__["types_key"] = (
            tuple(card_in_play.supertypes),
            tuple(card_in_play.types),
            tuple(card_in_play.subtypes),
        )

    return returned_cards


def main() -> None:
    # extractor = TokenExtractor()
    # token_exceptions = []
    cards = load_cards()
    maximal_cards = {}
    eliminated_card_keys = {}
    maximal_in_play = {}
    eliminated_in_play_keys = {}

    for card in Bar("Processing cards").iter(cards):
        if not card.is_valid:
            continue

        if card.name == "Grist, the Hunger Tide":
            grist_not_on_battlefield = deepcopy(card)
            add_types(grist_not_on_battlefield, ["Creature"])
            add_subtypes(grist_not_on_battlefield, ["Insect"])
            # update_maximals(grist_not_on_battlefield,
            #                 maximal_cards, eliminated_card_keys)
            for card_in_play in modify_card_in_play(grist_not_on_battlefield):
                update_maximals(card_in_play, maximal_in_play,
                                eliminated_in_play_keys)

        update_maximals(card, maximal_cards, eliminated_card_keys)

        # try:
        #     tokens = extractor.extract_from_card(card)
        # except Exception:
        #     token_exceptions.append(card)

        for card_in_play in modify_card_in_play(card):
            update_maximals(card_in_play, maximal_in_play,
                            eliminated_in_play_keys)

    # maximal_tokens = {}
    # eliminated_token_keys = {}
    # tokens = [
    #     # The Hive, LEA
    #     MagicToken(types=["Artifact", "Creature"], subtypes=[
    #                "Insect"], name="Wasp", power="1", toughness="1", keywords=["flying"]),

    #     # Bygone Bishop, SOI
    #     MagicToken(predefined="Clue"),

    #     # Depths of Desire, XLN
    #     MagicToken(predefined="Treasure"),

    #     # Niko Aris, KHM
    #     MagicToken(predefined="Shard"),

    #     # Bartered Cow, ELD
    #     MagicToken(predefined="Food"),

    #     # Gild, BNG
    #     MagicToken(predefined="Gold"),

    #     # Nahiri the Lithomancer, C14
    #     MagicToken(name="Stoneforged Blade", types=["Artifact"], subtypes=["Equipment"], keywords=[
    #                "indestructible", "equip {0}"], text="Equipped creature gets +5/+5 and has double strike")
    # ]
    # for token in Bar("Processing tokens").iter(tokens):
    #     for token_in_play in modify_card_in_play(token):
    #         update_maximals(token_in_play, maximal_tokens,
    #                         eliminated_token_keys)

    print("•", len(maximal_cards.keys()), "cards found")
    write_cards_to_csv(maximal_cards.values(), "maximal_cards")

    print("•", len(maximal_in_play.keys()), "cards in play found")
    write_cards_to_csv(maximal_in_play.values(), "maximal_in_play")

    # print("•", len(maximal_tokens.keys()), "tokens found")
    # write_cards_to_csv(maximal_tokens.values(), "maximal_tokens")

    # print("•", len(token_exceptions), "exceptions while parsing tokens")
    # write_cards_to_csv(token_exceptions, "token_exceptions")


if __name__ == "__main__":
    main()
