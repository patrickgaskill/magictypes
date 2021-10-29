import sys

sys.path.append("../src")
from magicobjects import MagicToken

MID_test_cases = [
    (
        "Adeline, Resplendent Cathar",
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
        "Blessed Defiance",
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
        "Cathar's Call",
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
        "Clarion Cathars",
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
        "Fateful Absence",
        [MagicToken.Clue],
    ),
    (
        "Sunset Revelry",
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
        "Falcon Abomination",
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
        "Flip the Switch",
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
        "Ominous Roost",
        [
            MagicToken(
                colors=["U"],
                types=["Creature"],
                subtypes=["Bird"],
                power="1",
                toughness="1",
                keywords=["Flying"],
                text="This creature can block only creatures with flying.",
            )
        ],
    ),
    (
        "Poppet Stitcher",
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
        "Revenge of the Drowned",
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
        "Secrets of the Key",
        [MagicToken.Clue],
    ),
    (
        "Startle",
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
        "Bat Whisperer",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Bat"],
                power="1",
                toughness="1",
                keywords=["Flying"],
            )
        ],
    ),
    (
        "Diregraf Horde",
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
        "Foul Play",
        [MagicToken.Clue],
    ),
    (
        "Hobbling Zombie",
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
        "Jadar, Ghoulcaller of Nephalia",
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
        "Jerren, Corrupted Bishop",
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
        "No Way Out",
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
        "Rotten Reunion",
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
        "Slaughter Specialist",
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
        "Tainted Adversary",
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
        "Burn Down the House",
        [
            MagicToken(
                colors=["R"],
                types=["Creature"],
                subtypes=["Devil"],
                power="1",
                toughness="1",
                text="When this creature dies, it deals 1 damage to any target.",
            )
        ],
    ),
    (
        "Seize the Storm",
        [
            MagicToken(
                colors=["R"],
                types=["Creature"],
                subtypes=["Elemental"],
                keywords=["Trample"],
                text="This creature's power and toughness are each equal to the number of instant and sorcery cards in your graveyard plus the number of cards with flashback you own in exile.",
            )
        ],
    ),
    (
        "Briarbridge Tracker",
        [MagicToken.Clue],
    ),
    (
        "Brood Weaver",
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
        "Consuming Blob",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Ooze"],
                text="This creature's power is equal to the number of card types among cards in your graveyard and its toughness is equal to that number plus 1.",
            )
        ],
    ),
    (
        "Dawnhart Mentor",
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
        "Rise of the Ants",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Insect"],
                power="3",
                toughness="3",
            )
        ],
    ),
    (
        "Shadowbeast Sighting",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Beast"],
                power="4",
                toughness="4",
            )
        ],
    ),
    (
        "Tovolar's Huntmaster",
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
    (
        "Tovolar's Packleader",
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
    (
        "Wrenn and Seven",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Treefolk"],
                keywords=["Reach"],
                text="This creature's power and toughness are each equal to the number of lands you control.",
            )
        ],
    ),
    (
        "Arlinn, the Pack's Hope",
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
    (
        "Corpse Cobble",
        [
            MagicToken(
                colors=["U", "B"],
                types=["Creature"],
                subtypes=["Zombie"],
                power="X",
                toughness="X",
                keywords=["Menace"],
            )
        ],
    ),
    (
        "Dennick, Pious Apparition",
        [MagicToken.Clue],
    ),
    (
        "Ghoulcaller's Harvest",
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
        "Hungry for More",
        [
            MagicToken(
                colors=["B", "R"],
                types=["Creature"],
                subtypes=["Vampire"],
                power="3",
                toughness="1",
                keywords=["Trample", "Lifelink", "Haste"],
            )
        ],
    ),
    (
        "Join the Dance",
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
