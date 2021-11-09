import sys

sys.path.append("../src")
from magicobjects import MagicToken

VOC_test_cases = [
    (
        "Millicent, Restless Revenant",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Spirit"],
                power="1",
                toughness="1",
                keywords=["Flying"],
            )
        ],
    ),
    (
        "Strefan, Maurer Progenitor",
        [MagicToken.Blood],
    ),
    (
        "Donal, Herald of Wings",
        [],
    ),
    (
        "Timothar, Baron of Bats",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Bat"],
                power="1",
                toughness="1",
                keywords=["Flying"],
                text="When this creature deals combat damage to a player, sacrifice it and return the exiled card to the battlefield tapped.",
            )
        ],
    ),
    (
        "Haunted Library",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Spirit"],
                power="1",
                toughness="1",
                keywords=["Flying"],
            )
        ],
    ),
    (
        "Priest of the Blessed Graf",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Spirit"],
                power="1",
                toughness="1",
                keywords=["Flying"],
            )
        ],
    ),
    (
        "Storm of Souls",
        [],
    ),
    (
        "Ethereal Investigator",
        [
            MagicToken.Clue,
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Spirit"],
                power="1",
                toughness="1",
                keywords=["Flying"],
            ),
        ],
    ),
    (
        "Haunted Imitation",
        [],
    ),
    (
        "Occult Epiphany",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Spirit"],
                power="1",
                toughness="1",
                keywords=["Flying"],
            )
        ],
    ),
    (
        "Glass-Cast Heart",
        [
            MagicToken.Blood,
            MagicToken(
                colors=["W", "B"],
                types=["Creature"],
                subtypes=["Vampire"],
                power="1",
                toughness="1",
                keywords=["Lifelink"],
            ),
        ],
    ),
    (
        "Kamber, the Plunderer",
        [
            MagicToken.Blood,
        ],
    ),
    (
        "Arterial Alchemy",
        [
            MagicToken.Blood,
        ],
    ),
    (
        "Markov Enforcer",
        [
            MagicToken.Blood,
        ],
    ),
    (
        "Scion of Opulence",
        [
            MagicToken.Treasure,
        ],
    ),
    (
        "Disorder in the Court",
        [
            MagicToken.Clue,
        ],
    ),
    (
        "Wedding Ring",
        [],
    ),
    (
        "Mirage Phalanx",
        [],
    ),
    (
        "Hollowhenge Overlord",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Wolf"],
                power="2",
                toughness="2",
            )
        ],
    ),
]
