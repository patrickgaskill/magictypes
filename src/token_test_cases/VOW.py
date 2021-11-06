import sys

sys.path.append("../src")
from magicobjects import MagicToken

VOW_test_cases = [
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
        "Hallowed Haunting",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Spirit", "Cleric"],
                text="This creature's power and toughness are each equal to the number of Spirits you control.",
            )
        ],
    ),
    (
        "Heron-Blessed Geist",
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
        "Nuturing Presence",
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
    ("Sigarda's Imprisonment", [MagicToken.Blood]),
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
    ("Mirrorhall Mimic", []),
    ("Ghastly Mimicry", []),
    ("Necroduality", []),
    ("Syphon Essence", [MagicToken.Blood]),
    (
        "Whispering Wizard",
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
    ("Blood Fountain", [MagicToken.Blood]),
    ("Bloodcrazed Socialite", [MagicToken.Blood]),
    ("Bloodvial Purveyor", [MagicToken.Blood]),
    (
        "Doomed Dissenter",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Zombie"],
                power="2",
                toughness="2",
            )
        ],
    ),
    ("Dreadfeast Demon", []),
    (
        "Dying to Serve",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Zombie"],
                power="2",
                toughness="2",
            )
        ],
    ),
    ("Falkenrath Forebear", [MagicToken.Blood]),
    ("Gluttonous Guest", [MagicToken.Blood]),
    ("Grisly Ritual", [MagicToken.Blood]),
    (
        "Headless Rider",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Zombie"],
                power="2",
                toughness="2",
            )
        ],
    ),
    ("Pointed Discussion", [MagicToken.Blood]),
    ("Restless Bloodseeker", [MagicToken.Blood]),
    ("Bloodsoaked Reveler", [MagicToken.Blood]),
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
    (
        "Toxrill, the Corrosive",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Slug"],
                power="1",
                toughness="1",
            )
        ],
    ),
    ("Vampire's Kiss", [MagicToken.Blood]),
    ("Voldaren Bloodcaster", [MagicToken.Blood]),
    ("Belligerent Guest", [MagicToken.Blood]),
    ("Blood Petal Celebrant", [MagicToken.Blood]),
    ("Bloody Betrayal", [MagicToken.Blood]),
    ("Falkenrath Celebrants", [MagicToken.Blood]),
    (
        "Kessig Wolfrider",
        [
            MagicToken(
                colors=["R"],
                types=["Creature"],
                subtypes=["Wolf"],
                power="3",
                toughness="2",
            )
        ],
    ),
    ("Lacerate Flesh", [MagicToken.Blood]),
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
    ("Olivia's Attendants", [MagicToken.Blood]),
    ("Sanguine Statue", [MagicToken.Blood]),
    (
        "Stensia Uprising",
        [
            MagicToken(
                colors=["R"],
                types=["Creature"],
                subtypes=["Human"],
                power="1",
                toughness="1",
            )
        ],
    ),
    ("Vampires' Vengeance", [MagicToken.Blood]),
    ("Voldaren Epicure", [MagicToken.Blood]),
    (
        "Crawling Infestation",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Insect"],
                power="1",
                toughness="1",
            )
        ],
    ),
    (
        "Hiveheart Shaman",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Insect"],
                power="1",
                toughness="1",
            )
        ],
    ),
    (
        "Howling Moon",
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
        "Infestation Expert",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Insect"],
                power="1",
                toughness="1",
            )
        ],
    ),
    (
        "Infested Werewolf",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Insect"],
                power="1",
                toughness="1",
            )
        ],
    ),
    (
        "Rural Recruit",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Boar"],
                power="3",
                toughness="1",
            )
        ],
    ),
    ("Anje, Maid of Dishonor", [MagicToken.Blood]),
    ("Bloodtithe Harvester", [MagicToken.Blood]),
    (
        "Brine Comber",
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
        "Brinebound Gift",
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
        "Child of the Pack",
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
    (
        "Edgar Markov's Coffin",
        [
            MagicToken(
                colors=["W", "B"],
                types=["Creature"],
                subtypes=["Vampire"],
                power="1",
                toughness="1",
                keywords=["Lifelink"],
            )
        ],
    ),
    (
        "Kaya, Geist Hunter",
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
    ("Odric, Blood-Cursed", [MagicToken.Blood]),
    (
        "Old Rutstein",
        [
            MagicToken.Treasure,
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Insect"],
                power="1",
                toughness="1",
            ),
            MagicToken.Blood,
        ],
    ),
    (
        "Krothuss, Lord of the Deep",
        [],
    ),
    (
        "Skull Skaab",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Zombie"],
                power="2",
                toughness="2",
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
    (
        "Vilespawn Spider",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Insect"],
                power="1",
                toughness="1",
            )
        ],
    ),
    ("Blood Servitor", [MagicToken.Blood]),
    ("Ceremonial Knife", [MagicToken.Blood]),
    ("Dollhouse of Horrors", []),
    ("Voldaren Estate", [MagicToken.Blood]),
    ("Path of Peril", []),
]
