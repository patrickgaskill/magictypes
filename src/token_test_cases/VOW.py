import sys

sys.path.append("../src")
from magicobjects import MagicToken

VOW_test_cases = [
    ("Anje, Maid of Dishonor", [MagicToken.Blood]),
    (
        "Dorothea's Retribution",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Spirit"],
                power="4",
                toughness="4",
                keywords=["Flying"],
            )
        ],
    ),
    ("Gluttonous Guest", [MagicToken.Blood]),
    (
        "Sorin the Mirthless",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Vampire"],
                power="2",
                toughness="3",
                keywords=["Flying", "Lifelink"],
            )
        ],
    ),
    ("Vampire's Vengeance", [MagicToken.Blood]),
    ("Voldaren Bloodcaster", [MagicToken.Blood]),
    ("Voldaren Estate", [MagicToken.Blood]),
    (
        "Wedding Announcement",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Human"],
                power="1",
                toughness="1",
            )
        ],
    ),
]
