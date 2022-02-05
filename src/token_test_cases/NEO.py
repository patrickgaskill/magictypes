import sys

sys.path.append("../src")
from magicobjects import MagicToken

NEO_test_cases = [
    (
        "Mechtitan Core",
        [
            MagicToken(
                name="Mechtitan",
                colors=["W", "U", "B", "R", "G"],
                supertypes=["Legendary"],
                types=["Artifact", "Creature"],
                subtypes=["Construct"],
                power="10",
                toughness="10",
                keywords=["Flying", "Vigilance", "Trample", "Lifelink", "Haste"],
            )
        ],
    ),
    (
        "Tamiyo, Compleated Sage",
        [
            MagicToken(
                name="Tamiyo's Notebook",
                supertypes=["Legendary"],
                types=["Artifact"],
                text="Spells you cast cost {2} less to cast.\n{T}: Draw a card.",
            )
        ],
    ),
    ("Roaring Earth", []),
    ("Enormous Energy Blade", []),
    (
        "Born to Drive",
        [
            MagicToken(
                colors=[],
                types=["Creature"],
                subtypes=["Pilot"],
                power="1",
                toughness="1",
                text="This creature crews Vehicles as though its power were 2 greater.",
            )
        ],
    ),
]
