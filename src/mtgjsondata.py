import json
from typing import Optional, Callable
from ordered_set import OrderedSet
from utils import get_data_path
from magicobjects import MagicObject, Subtype


def load_objects(
    filterfunc: Optional[Callable[[MagicObject], bool]] = None
) -> list[MagicObject]:
    MagicObject.all_creature_types = load_creature_types()

    with get_data_path("mtgjson/SetList.json").open() as setlistfile:
        setlist = json.load(setlistfile)["data"]

    sets_map: dict[str, dict[str, any]] = {}
    for set_ in setlist:
        sets_map[set_["code"]] = set_

    with get_data_path("mtgjson/AllIdentifiers.json").open() as allidentifiersfile:
        allidentifiers = json.load(allidentifiersfile)["data"].values()

    for obj in allidentifiers:
        set_code = obj["setCode"]
        set_ = sets_map[set_code] if set_code in sets_map else None
        set_release_date = (
            set_["releaseDate"] if set_ and "releaseDate" in set_ else None
        )
        set_type = set_["type"] if set_ and "type" in set_ else None

        card = MagicObject(
            name=obj["name"],
            types=OrderedSet(obj["types"]),
            subtypes=OrderedSet(obj["subtypes"]),
            supertypes=OrderedSet(obj["supertypes"]),
            keywords=set(obj["keywords"]) if "keywords" in obj else set(),
            set_code=obj["setCode"],
            set_release_date=set_release_date,
            set_type=set_type,
            original_release_date=obj["originalReleaseDate"]
            if "originalReleaseDate" in obj
            else None,
            number=obj["number"],
            border_color=obj["borderColor"],
            availability=set(obj["availability"]),
            layout=obj["layout"],
        )

        if filterfunc and not filterfunc(card):
            continue

        yield card


def load_creature_types() -> set[Subtype]:
    with get_data_path("mtgjson/CardTypes.json").open() as f:
        card_types_data = json.load(f)["data"]
    creature_types = card_types_data["creature"]["subTypes"]
    # mtgjson includes some illegal creature types
    unwanted_types = ("Chicken", "Head", "Hornet", "Reveler", "Rukh", "Wasp")
    return set(t for t in creature_types if t not in unwanted_types)
