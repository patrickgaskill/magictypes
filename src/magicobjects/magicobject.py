from copy import deepcopy
from datetime import datetime
import re
from typing import Type, Literal, Union, Optional, Iterable, TypeVar, NewType, ClassVar
from dataclasses import dataclass
from ordered_set import OrderedSet

ObjectType = Literal["object", "card", "token"]
Color = Union["W", "U", "B", "R", "G"]
CardType = Union[
    "Tribal", "Enchantment", "Artifact", "Land", "Planeswalker", "Creature"
]
Subtype = NewType("Subtype", str)
Supertype = Union["Basic", "Legendary", "Ongoing", "Snow", "World"]
Keyword = NewType("Keyword", str)
TypeKey = tuple[tuple[Supertype, ...], tuple[CardType, ...], tuple[Subtype, ...]]
T = TypeVar("T")

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


def sorted_with_order(iterable: Iterable[T], order_dict: dict[T, int]) -> Iterable[T]:
    return sorted(iterable, key=lambda x: order_dict[x] if x in order_dict else 0)


@dataclass
class MagicObject:
    all_creature_types: ClassVar[set[Subtype]]
    basic_land_types: ClassVar[set[Subtype]] = set(
        ["Forest", "Island", "Mountain", "Plains", "Swamp"]
    )
    name: str
    types: OrderedSet[CardType]
    subtypes: OrderedSet[Subtype]
    supertypes: OrderedSet[Supertype]
    keywords: set[Keyword]
    set_code: str
    set_release_date: Optional[str]
    set_type: Optional[str]
    original_release_date: Optional[str]
    number: str
    border_color: str
    availability: set[str]
    layout: str

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

    def sort_types(self) -> None:
        self.supertypes = OrderedSet(
            sorted_with_order(self.supertypes, SUPERTYPE_ORDER)
        )
        self.types = OrderedSet(sorted_with_order(self.types, TYPE_ORDER))
        self.subtypes = OrderedSet(sorted(self.subtypes))

    @property
    def type_str(self) -> str:
        formatted = " ".join(list(self.supertypes) + list(self.types))

        subtypes = self.subtypes
        notes = []

        if self.basic_land_types <= subtypes:
            subtypes -= self.basic_land_types
            notes.append("(all basic land types)")

        if self.is_every_creature_type:
            subtypes -= self.all_creature_types
            notes.append("(all creature types)")

        notes_and_subtypes = list(subtypes) + notes

        if len(notes_and_subtypes) > 0:
            formatted = f"{formatted} — {' '.join(notes_and_subtypes)}"

        return formatted

    @property
    def type_key(self) -> TypeKey:
        return (
            tuple(self.supertypes),
            tuple(self.types),
            tuple(
                self.subtypes.union(self.all_creature_types)
                if self.is_every_creature_type
                else self.subtypes
            ),
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

    def is_type_subset(self, other: Type[any]) -> bool:
        self_subtypes = (
            self.subtypes.union(self.all_creature_types)
            if self.is_every_creature_type
            else self.subtypes
        )
        other_subtypes = (
            other.subtypes.union(self.all_creature_types)
            if other.is_every_creature_type
            else other.subtypes
        )
        return self.types.union(self_subtypes, self.supertypes) < other.types.union(
            other_subtypes, other.supertypes
        )

    def get_copy(self) -> "MagicObject":
        return deepcopy(self)
