import re
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import datetime
from functools import cached_property
from typing import ClassVar, Literal, NewType, Optional

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
    object_type: ClassVar[str] = "object"
    all_creature_types: ClassVar[set[Subtype]]
    basic_land_types: ClassVar[set[Subtype]] = {
        "Forest",
        "Island",
        "Mountain",
        "Plains",
        "Swamp",
    }
    name: str
    text: Optional[str] = None
    power: Optional[str] = None
    toughness: Optional[str] = None
    colors: set[Color] = field(default_factory=set)
    types: set[CardType] = field(default_factory=set)
    subtypes: set[Subtype] = field(default_factory=set)
    supertypes: set[Supertype] = field(default_factory=set)
    keywords: set[Keyword] = field(default_factory=set)
    subtype_order: dict[Subtype, int] = field(
        init=False, repr=False, default_factory=dict
    )

    def __post_init__(self):
        if isinstance(self.subtypes, Sequence):
            self.subtype_order = {s: i for i, s in enumerate(self.subtypes)}

        self.colors = set(self.colors)
        self.types = set(self.types)
        self.subtypes = set(self.subtypes)
        self.supertypes = set(self.supertypes)
        self.keywords = set(self.keywords)

    @property
    def release_date(self) -> str:
        raise NotImplementedError("Generic Magic objects do not have a release date.")

    @cached_property
    def is_every_creature_type(self) -> bool:
        return (
            "Changeling" in self.keywords
            or (self.text and f"{self.name} is every creature type" in self.text)
            or self.subtypes >= MagicObject.all_creature_types
        )

    @property
    def is_token(self) -> bool:
        return self.object_type == "token"

    @cached_property
    def is_permanent(self) -> bool:
        return any(
            t in ("Artifact", "Creature", "Enchantment", "Land", "Planeswalker")
            for t in self.types
        )

    @cached_property
    def expanded_subtypes(self) -> set[Subtype]:
        if self.subtypes >= MagicObject.all_creature_types:
            return self.subtypes

        return (
            self.subtypes.union(self.all_creature_types)
            if self.is_every_creature_type
            else self.subtypes
        )

    @cached_property
    def sorted_supertypes(self) -> list[Supertype]:
        return sorted(self.supertypes, key=lambda x: SUPERTYPE_ORDER[x])

    @cached_property
    def sorted_types(self) -> list[CardType]:
        return sorted(
            self.types, key=lambda x: TYPE_ORDER[x] if x in TYPE_ORDER else 999
        )

    @cached_property
    def sorted_subtypes(self) -> list[Subtype]:
        return sorted(
            self.subtypes,
            key=lambda x: self.subtype_order[x] if x in self.subtype_order else 999,
        )

    @cached_property
    def type_str(self) -> str:
        formatted = " ".join(self.sorted_supertypes + self.sorted_types)

        subtypes = self.subtypes
        notes = []

        if self.basic_land_types <= subtypes:
            subtypes -= self.basic_land_types
            notes.append("(all basic land types)")

        if self.is_every_creature_type:
            subtypes -= MagicObject.all_creature_types
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
        raise NotImplementedError("Generic Magic objects do not have a sort key.")

    def is_type_subset(self, other: "MagicObject") -> bool:
        return self.types.union(
            self.expanded_subtypes, self.supertypes
        ) < other.types.union(other.expanded_subtypes, other.supertypes)

    def copy(self) -> "MagicObject":
        return MagicObject(
            name=self.name,
            types=self.types.copy(),
            subtypes=self.sorted_subtypes,
            supertypes=self.supertypes.copy(),
            keywords=self.keywords.copy(),
            text=self.text,
        )

    def clear_cached_properties(self) -> None:
        for value in vars(self).values():
            if hasattr(value, "cache_clear"):
                value.cache_clear()


@dataclass
class MagicCard(MagicObject):
    object_type: ClassVar[str] = "card"
    face_name: Optional[str] = None
    set_code: Optional[str] = None
    number: Optional[str] = None
    border_color: Optional[str] = None
    layout: Optional[str] = None
    set_release_date: Optional[str] = None
    set_type: Optional[str] = None
    original_release_date: Optional[str] = None
    availability: set[str] = field(default_factory=set)

    def __post_init__(self):
        super().__post_init__()
        self.availability = set(self.availability)

    @property
    def release_date(self) -> str:
        if self.original_release_date:
            return self.original_release_date

        return self.set_release_date

    @cached_property
    def sort_key(self) -> tuple[datetime, str, int, str]:
        release_date = (
            datetime.fromisoformat(self.release_date)
            if self.release_date
            else datetime.max
        )
        parsed_number = int(re.sub(r"[^\d]+", "", self.number))
        return release_date, self.set_code, parsed_number, self.number

    def copy(self) -> "MagicCard":
        return MagicCard(
            name=self.name,
            types=self.types.copy(),
            subtypes=self.sorted_subtypes,
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
            text=self.text,
        )


@dataclass
class MagicToken(MagicObject):
    object_type: ClassVar[str] = "token"
    name: str = None
    creator: Optional[MagicObject] = field(compare=False, default=None)

    def __post_init__(self):
        super().__post_init__()
        if not self.name:
            self.name = " ".join(self.sorted_subtypes)

    @property
    def release_date(self) -> str:
        if self.creator:
            return self.creator.release_date

        raise AttributeError("This instance of MagicToken does not have a creator set")

    @cached_property
    def sort_key(self) -> tuple[datetime, str, int, str]:
        if self.creator:
            return self.creator.sort_key

        raise AttributeError("This instance of MagicToken does not have a creator set")

    def __copy__(self):
        return self.copy()

    def copy(self) -> "MagicToken":
        return MagicToken(
            name=self.name,
            colors=self.colors.copy(),
            types=self.types.copy(),
            subtypes=self.sorted_subtypes,
            supertypes=self.supertypes.copy(),
            keywords=self.keywords.copy(),
            text=self.text,
            power=self.power,
            toughness=self.toughness,
            creator=self.creator.copy(),
        )

    def asdict(self):
        return {
            "name": self.name,
            "colors": self.colors.copy(),
            "types": self.types.copy(),
            "subtypes": self.sorted_subtypes,
            "supertypes": self.supertypes.copy(),
            "keywords": self.keywords.copy(),
            "text": self.text,
            "power": self.power,
            "toughness": self.toughness,
        }

    @classmethod
    @property
    def Gold(cls):
        return cls(
            types=["Artifact"],
            subtypes=["Gold"],
            text="Sacrifice this artifact: Add one mana of any color.",
        )

    @classmethod
    @property
    def Clue(cls):
        return cls(
            types=["Artifact"],
            subtypes=["Clue"],
            text="{2}, Sacrifice this artifact: Draw a card.",
        )

    @classmethod
    @property
    def Treasure(cls):
        return cls(
            types=["Artifact"],
            subtypes=["Treasure"],
            text="{T}, Sacrifice this artifact: Add one mana of any color.",
        )

    @classmethod
    @property
    def Food(cls):
        return cls(
            types=["Artifact"],
            subtypes=["Food"],
            text="{2}, {T}, Sacrifice this artifact: You gain 3 life.",
        )

    @classmethod
    @property
    def Shard(cls):
        return cls(
            types=["Enchantment"],
            subtypes=["Shard"],
            text="{2}, Sacrifice this enchantment: Scry 1, then draw a card.",
        )

    @classmethod
    @property
    def Walker(cls):
        return cls(
            name="Walker",
            colors=["B"],
            types=["Creature"],
            subtypes=["Zombie"],
            power="2",
            toughness="2",
        )
