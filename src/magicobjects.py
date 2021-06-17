import re
from dataclasses import dataclass
from datetime import datetime
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

    @property
    def is_every_creature_type(self) -> bool:
        return (
            "Changeling" in self.keywords
            or self.name == "Mistform Ultimus"
            or self.subtypes >= self.all_creature_types
        )

    @property
    def is_token(self) -> bool:
        return self.layout == "token"

    @property
    def is_permanent(self) -> bool:
        return any(
            t in ("Artifact", "Creature", "Enchantment", "Land", "Planeswalker")
            for t in self.types
        )

    @property
    def expanded_subtypes(self) -> set[Subtype]:
        if self.subtypes >= self.all_creature_types:
            return self.subtypes

        return (
            self.subtypes.union(self.all_creature_types)
            if self.is_every_creature_type
            else self.subtypes
        )

    @property
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

    @property
    def type_key(self) -> TypeKey:
        return (
            tuple(sorted(self.supertypes)),
            tuple(sorted(self.types)),
            tuple(sorted(self.expanded_subtypes)),
        )

    @property
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
        return MagicObject(
            name=self.name,
            types=self.types.copy(),
            subtypes=self.subtypes.copy(),
            supertypes=self.supertypes.copy(),
            keywords=self.keywords.copy(),
            set_code=self.set_code,
            set_release_date=self.set_release_date,
            set_type=self.set_type,
            original_release_date=self.original_release_date,
            number=self.number,
            border_color=self.border_color,
            availability=self.availability.copy(),
            layout=self.layout,
            subtype_order=self.subtype_order.copy(),
        )
