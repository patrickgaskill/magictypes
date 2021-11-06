from functools import cached_property
from typing import Callable, Generator, Optional

from magicobjects import MagicCard, MagicObject, Subtype
from utils import get_data_json


def legal_card_filter(obj: dict[str, any], sets: dict[str, any]) -> bool:
    if "Card" in obj["types"]:
        return False

    if obj["borderColor"] in ("gold", "silver"):
        return False

    if "shandalar" in obj["availability"]:
        return False

    if obj["layout"] in ("token", "emblem"):
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


class MtgjsonData:
    def get_card_by_name(self, name: str, set_code: Optional[str] = None):
        cards = self.load_cards(filterfunc=legal_card_filter)
        if set_code:
            card = next(
                (
                    c
                    for c in cards
                    if name in (c.name, c.face_name) and (c.set_code == set_code)
                ),
                None,
            )
        else:
            card = next(
                (c for c in cards if name in (c.name, c.face_name)),
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

    def load_cards(
        self,
        filterfunc: Optional[Callable[[dict[str, any]], bool]] = None,
    ) -> Generator[MagicCard, None, None]:
        MagicObject.all_creature_types = self.creature_types

        sets = {s["code"]: s for s in self.set_list}
        MagicCard.sets = sets

        objects = self.all_identifiers.values()

        for obj in objects:
            if callable(filterfunc) and not filterfunc(obj, sets):
                continue

            set_code = None
            set_release_date = None
            set_type = None

            if "setCode" in obj:
                set_code = obj["setCode"]
                if set_code in sets:
                    s = sets[set_code]
                    set_release_date = s["releaseDate"]
                    set_type = s["type"]
                elif len(set_code) == 4:  # Handle token sets like TAFR
                    trimmed_set_code = set_code[-3:]
                    if trimmed_set_code in sets:
                        s = sets[trimmed_set_code]
                        set_release_date = s["releaseDate"]
                        set_type = s["type"]

            magic_card = MagicCard(
                name=obj["name"],
                face_name=obj["faceName"] if "faceName" in obj else None,
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

            yield magic_card


if __name__ == "__main__":
    mtgjsondata = MtgjsonData()
    print(len(mtgjsondata.all_identifiers))
