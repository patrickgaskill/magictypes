from functools import cached_property
from typing import Callable, Generator, Optional

from magicobjects import MagicObject, Subtype
from utils import get_data_json


def legal_card_filter(card, sets):
    if "Card" in card["types"]:
        return False

    if card["borderColor"] in ("gold", "silver"):
        return False

    if "shandalar" in card["availability"]:
        return False

    if card["layout"] == "emblem":
        return False

    if card["setCode"] in (
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

    if card["setCode"] in sets:
        s = sets[card["setCode"]]

        if s["type"] in ("funny", "memorabilia", "promo"):
            return False

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
        self, filterfunc: Optional[Callable[[MagicObject], bool]] = legal_card_filter
    ) -> Generator[MagicObject, None, None]:
        MagicObject.all_creature_types = self.creature_types

        sets = {s["code"]: s for s in self.set_list}
        MagicObject.sets = sets

        for card in self.all_identifiers.values():
            if callable(filterfunc) and not filterfunc(card, sets):
                continue

            set_release_date = None
            set_type = None
            if card["setCode"] in sets:
                s = sets[card["setCode"]]
                set_release_date = s["releaseDate"]
                set_type = s["type"]

            magic_obj = MagicObject(
                name=card["name"],
                types=set(
                    t for t in card["types"] if t != "Token"
                ),  # mtgjson adds a fake Token type to token objects
                subtypes=set(card["subtypes"]),
                supertypes=set(card["supertypes"]),
                keywords=set(card["keywords"]) if "keywords" in card else set(),
                set_code=card["setCode"],
                set_release_date=set_release_date,
                set_type=set_type,
                original_release_date=card["originalReleaseDate"]
                if "originalReleaseDate" in card
                else None,
                number=card["number"],
                border_color=card["borderColor"],
                availability=set(card["availability"]),
                layout=card["layout"],
                subtype_order={t: i for i, t in enumerate(card["subtypes"])},
            )

            yield magic_obj


if __name__ == "__main__":
    mtgjsondata = MtgjsonData()
    print(len(mtgjsondata.all_identifiers))
