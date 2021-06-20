from functools import cached_property
from typing import Callable, Generator, Literal, Optional

from magicobjects import MagicObject, Subtype
from utils import get_data_json


def legal_card_filter(obj, sets):
    if "Card" in obj["types"]:
        return False

    if obj["borderColor"] in ("gold", "silver"):
        return False

    if "shandalar" in obj["availability"]:
        return False

    if obj["layout"] == "emblem":
        return False

    if obj["setCode"] in (
        "THP1",
        "THP2",
        "THP3",
        "PSAL",
        "TDAG",
        "TBTH",
        "TFTH",
        "TUND",
    ):
        return False

    if obj["setCode"] in sets:
        s = sets[obj["setCode"]]

        if s["type"] in ("funny", "memorabilia", "promo"):
            return False

    return True


def atomic_card_filter(obj, _):
    if "Card" in obj["types"]:
        return False

    # if obj["borderColor"] in ("gold", "silver"):
    #     return False

    # if "shandalar" in obj["availability"]:
    #     return False

    if obj["layout"] == "emblem":
        return False

    bad_sets = [
        "THP1",
        "THP2",
        "THP3",
        "PSAL",
        "TDAG",
        "TBTH",
        "TFTH",
        "TUND",
    ]

    # if obj["setCode"] in (
    #     "THP1",
    #     "THP2",
    #     "THP3",
    #     "PSAL",
    #     "TDAG",
    #     "TBTH",
    #     "TFTH",
    #     "TUND",
    # ):
    # return False

    # if obj["setCode"] in sets:
    #     s = sets[obj["setCode"]]

    #     if s["type"] in ("funny", "memorabilia", "promo"):
    #         return False

    return True


class MtgjsonData:
    def get_card_by_name(self, name: str):
        objects = self.load_objects()
        card = next(
            (c for c in objects if c.name == name),
            None,
        )
        assert card is not None
        return card

    @cached_property
    def all_identifiers(self) -> list[dict[str, any]]:
        return get_data_json("mtgjson/AllIdentifiers.json")["data"]

    @cached_property
    def atomic_cards(self) -> list[dict[str, any]]:
        return get_data_json("mtgjson/AtomicCards.json")["data"]

    @cached_property
    def set_list(self) -> list[dict[str, any]]:
        return get_data_json("mtgjson/SetList.json")["data"]

    @cached_property
    def creature_types(self) -> set[Subtype]:
        card_types_data = get_data_json("mtgjson/CardTypes.json")["data"]
        creature_types = card_types_data["creature"]["subTypes"]
        # mtgjson includes some illegal creature types
        unwanted_types = ("Chicken", "Head", "Hornet", "Reveler", "Rukh", "Wasp")
        return set(t for t in creature_types if t not in unwanted_types)

    def load_objects(
        self,
        source: Literal["AllIdentifiers", "AtomicCards"] = "AllIdentifiers",
        filterfunc: Optional[Callable[[MagicObject], bool]] = None,
    ) -> Generator[MagicObject, None, None]:
        MagicObject.all_creature_types = self.creature_types

        sets = {s["code"]: s for s in self.set_list}
        MagicObject.sets = sets

        if source == "AtomicCards":
            objects = [obj[0] for obj in self.atomic_cards.values()]
        else:
            objects = self.all_identifiers.values()

        for obj in objects:
            if callable(filterfunc) and not filterfunc(obj, sets):
                continue

            set_code = None
            set_release_date = None
            set_type = None
            if "setCode" in obj and obj["setCode"] in sets:
                set_code = obj["setCode"]
                s = sets[set_code]
                set_release_date = s["releaseDate"]
                set_type = s["type"]

            magic_obj = MagicObject(
                name=obj["name"],
                colors=obj["colors"],
                types=set(
                    t for t in obj["types"] if t != "Token"
                ),  # mtgjson adds a fake Token type to token objects
                subtypes=obj["subtypes"],
                supertypes=obj["supertypes"],
                keywords=obj["keywords"] if "keywords" in obj else {},
                set_code=set_code,
                set_release_date=set_release_date,
                set_type=set_type,
                original_release_date=obj["originalReleaseDate"]
                if "originalReleaseDate" in obj
                else None,
                number=obj["number"] if "number" in obj else None,
                border_color=obj["borderColor"] if "borderColor" in obj else None,
                availability=set(obj["availability"])
                if "availability" in obj
                else set(),
                layout=obj["layout"],
                text=obj["text"] if "text" in obj else None,
            )

            yield magic_obj


if __name__ == "__main__":
    mtgjsondata = MtgjsonData()
    print(len(mtgjsondata.all_identifiers))
