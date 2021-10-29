import sys

sys.path.append("../src")
from magicobjects import MagicToken

MIC_test_cases = [
    (
        "Cleaver Skaab",
        [],
    ),
    (
        "Crowded Crypt",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Zombie"],
                power="2",
                toughness="2",
                keywords=["Decayed"],
            )
        ],
    ),
    (
        "Curse of Clinging Webs",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Spider"],
                power="1",
                toughness="2",
                keywords=["Reach"],
            )
        ],
    ),
    (
        "Curse of the Restless Dead",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Zombie"],
                power="2",
                toughness="2",
                keywords=["Decayed"],
            )
        ],
    ),
    (
        "Somberwald Beastmaster",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Wolf"],
                power="2",
                toughness="2",
            ),
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Beast"],
                power="3",
                toughness="3",
            ),
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Beast"],
                power="4",
                toughness="4",
            ),
        ],
    ),
    (
        "Visions of Glory",
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
    ("Visions of Ruin", [MagicToken.Treasure]),
    (
        "Wilhelt, the Rotcleaver",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Zombie"],
                power="2",
                toughness="2",
                keywords=["Decayed"],
            )
        ],
    ),
]
