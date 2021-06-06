from typing import Union, Optional

Color = Union["W", "U", "B", "R", "G"]
Type = Union["Tribal", "Enchantment",
             "Artifact", "Land", "Planeswalker", "Creature"]


class MagicToken:
    name: str
    colors: list[Color]
    supertypes: list[str]
    types: list[Type]
    subtypes: list[str]
    text: Optional[str]
    power: Optional[str]
    toughness: Optional[str]
    keywords: Optional[list[str]]

    color_order: dict[Color, int] = {
        "W": 0,
        "U": 1,
        "B": 2,
        "R": 3,
        "G": 4
    }

    type_order: dict[Type, int] = {
        "Tribal": 0,
        "Enchantment": 1,
        "Artifact": 2,
        "Land": 3,
        "Planeswalker": 4,
        "Creature": 5,
    }

    object: str = "token"

    def __init__(
        self,
        name: str = None,
        colors: list[Color] = [],
        supertypes: list[str] = [],
        types: list[Type] = [],
        subtypes: list[str] = [],
        text: Optional[str] = None,
        power: Optional[str] = None,
        toughness: Optional[str] = None,
        keywords: Optional[list[str]] = None,
        predefined: Optional[str] = None,
        creator: Optional[any] = None
    ):
        self.colors = sorted(
            colors, key=lambda color: self.color_order[color])
        self.supertypes = supertypes
        self.types = sorted(types, key=lambda t: self.type_order[t])
        self.subtypes = subtypes
        self.text = text
        self.power = power
        self.toughness = toughness
        self.keywords = keywords
        self.creator = creator

        if predefined == "Treasure":
            self.colors = []
            self.supertypes = []
            self.types = ["Artifact"]
            self.subtypes = ["Treasure"]
            self.text = "{T}, Sacrifice this artifact: Add one mana of any color."

        elif predefined == "Food":
            self.colors = []
            self.supertypes = []
            self.types = ["Artifact"]
            self.subtypes = ["Food"]
            self.text = "{2}, {T}, Sacrifice this artifact: You gain 3 life."

        elif predefined == "Gold":
            self.colors = []
            self.supertypes = []
            self.types = ["Artifact"]
            self.subtypes = ["Gold"]
            self.text = "Sacrifice this artifact: Add one mana of any color."

        elif predefined == "Walker":
            self.name = "Walker"
            self.colors = ["B"]
            self.supertypes = []
            self.types = ["Creature"]
            self.subtypes = ["Zombie"]
            self.power = "2"
            self.toughness = "2"

        elif predefined == "Shard":
            self.colors = []
            self.supertypes = []
            self.types = ["Enchantment"]
            self.subtypes = ["Shard"]
            self.text = "{2}, Sacrifice this enchantment: Scry 1, then draw a card."

        elif predefined == "Clue":
            self.colors = []
            self.supertypes = []
            self.types = ["Artifact"]
            self.subtypes = ["Clue"]
            self.text = "{2}, Sacrifice this artifact: Draw a card."

        self.name = name or " ".join(self.subtypes)

    def type(self) -> str:
        type_str = " ".join(self.types)

        if len(self.supertypes) > 0:
            type_str = f"{' '.join(self.supertypes)} {type_str}"

        if len(self.subtypes) > 0:
            type_str = f"{type_str} — {' '.join(self.subtypes)}"

        return type_str

    def __eq__(self, other):
        for k, v in vars(self).items():
            if v != getattr(other, k):
                return False
        return True

    def __repr__(self):
        return "MagicToken(" + ", ".join([f"{k}={v}" for k, v in vars(self).items()]) + ")"
