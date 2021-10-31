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
    (
        "Cemetery Protector",
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
    (
        "Krothuss, Lord of the Deep",
        [],
    ),
    (
        "Geralf, Visionary Stitcher",
        [
            MagicToken(
                colors=["U"],
                types=["Creature"],
                subtypes=["Zombie"],
                power="X",
                toughness="X",
            )
        ],
    ),
    (
        "Hallowed Haunting",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Spirit", "Cleric"],
                text=[
                    "This creature's power and toughness are each equal to the number of Spirits you control."
                ],
            )
        ],
    ),
    (
        "Manaform Hellkite",
        [
            MagicToken(
                colors=["R"],
                types=["Creature"],
                subtypes=["Dragon", "Illusion"],
                power="X",
                toughness="X",
                keywords=["Flying", "Haste"],
            )
        ],
    ),
    (
        "Torens, Fist of the Angels",
        [
            MagicToken(
                colors=["W", "G"],
                types=["Creature"],
                subtypes=["Human", "Soldier"],
                power="1",
                toughness="1",
                keywords=["Training"],
            )
        ],
    ),
]
