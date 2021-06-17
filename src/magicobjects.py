import re
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from functools import cached_property
from typing import ClassVar, Literal, NewType, Optional

ObjectType = Literal["object", "card", "token"]
Color = Literal["W", "U", "B", "R", "G"]
CardType = NewType("Type", str)
Subtype = NewType("Subtype", str)
Supertype = NewType("Supertype", str)
Keyword = NewType("Keyword", str)
TypeKey = tuple[tuple[Supertype, ...], tuple[CardType, ...], tuple[Subtype, ...]]

COLOR_ORDER: dict[Color, int] = {"W": 0, "U": 1, "B": 2, "R": 3, "G": 4}

TYPE_ORDER: dict[CardType, int] = {
    "Tribal": 0,
    "Enchantment": 1,
    "Artifact": 2,
    "Land": 3,
    "Planeswalker": 4,
    "Creature": 5,
}

SUPERTYPE_ORDER: dict[Supertype, int] = {
    "Basic": 0,
    "Legendary": 0,
    "Ongoing": 0,
    "Snow": 1,
    "World": 0,
}


@dataclass
class MagicObject:
    all_creature_types: ClassVar[set[Subtype]]
    basic_land_types: ClassVar[set[Subtype]] = set(
        ["Forest", "Island", "Mountain", "Plains", "Swamp"]
    )
    name: str
    types: set[CardType]
    subtypes: set[Subtype]
    supertypes: set[Supertype]
    keywords: set[Keyword]
    set_code: str
    set_release_date: Optional[str]
    set_type: Optional[str]
    original_release_date: Optional[str]
    number: str
    border_color: str
    availability: set[str]
    layout: str
    subtype_order: dict[Subtype, int]

    @property
    def release_date(self) -> str:
        if self.original_release_date:
            return self.original_release_date

        return self.set_release_date

    @cached_property
    def is_every_creature_type(self) -> bool:
        return (
            "Changeling" in self.keywords
            or self.name == "Mistform Ultimus"
            or self.subtypes >= self.all_creature_types
        )

    @property
    def is_token(self) -> bool:
        return self.layout == "token"

    @cached_property
    def is_permanent(self) -> bool:
        return any(
            t in ("Artifact", "Creature", "Enchantment", "Land", "Planeswalker")
            for t in self.types
        )

    @cached_property
    def expanded_subtypes(self) -> set[Subtype]:
        if self.subtypes >= self.all_creature_types:
            return self.subtypes

        return (
            self.subtypes.union(self.all_creature_types)
            if self.is_every_creature_type
            else self.subtypes
        )

    @cached_property
    def type_str(self) -> str:
        formatted = " ".join(
            sorted(self.supertypes, key=lambda x: SUPERTYPE_ORDER[x])
            + sorted(
                self.types, key=lambda x: TYPE_ORDER[x] if x in TYPE_ORDER else 999
            )
        )

        subtypes = self.subtypes
        notes = []

        if self.basic_land_types <= subtypes:
            subtypes -= self.basic_land_types
            notes.append("(all basic land types)")

        if self.is_every_creature_type:
            subtypes -= self.all_creature_types
            notes.append("(all creature types)")

        notes_and_subtypes = (
            sorted(
                subtypes,
                key=lambda x: self.subtype_order[x] if x in self.subtype_order else 999,
            )
            + notes
        )

        if len(notes_and_subtypes) > 0:
            formatted = f"{formatted} — {' '.join(notes_and_subtypes)}"

        return formatted

    @cached_property
    def type_key(self) -> TypeKey:
        return (
            tuple(sorted(self.supertypes)),
            tuple(sorted(self.types)),
            tuple(sorted(self.expanded_subtypes)),
        )

    @cached_property
    def sort_key(self) -> tuple[datetime, str, int, str]:
        release_date = (
            datetime.fromisoformat(self.release_date)
            if self.release_date
            else datetime.max
        )
        parsed_number = int(re.sub(r"[^\d]+", "", self.number))
        return release_date, self.set_code, parsed_number, self.number

    def is_type_subset(self, other: "MagicObject") -> bool:
        return self.types.union(
            self.expanded_subtypes, self.supertypes
        ) < other.types.union(other.expanded_subtypes, other.supertypes)

    def get_copy(self) -> "MagicObject":
        return deepcopy(self)

    def clear_cached_properties(self) -> None:
        for attr in (
            "is_every_creature_type",
            "expanded_subtypes",
            "is_permanent",
            "type_str",
            "type_key",
        ):
            if hasattr(self, attr):
                delattr(self, attr)
        # del self.is_every_creature_type
        # del self.expanded_subtypes
        # del self.is_permanent
        # # del self.type_str
        # del self.type_key
