import pytest
from types import SimpleNamespace

sn = SimpleNamespace

test_cases = [
    (
        "Decree of Justice",
        [
            sn(
                power="4",
                toughness="4",
                supertypes=[],
                types=["Creature"],
                subtypes=["Angel"],
            ),
            sn(
                power="1",
                toughness="1",
                supertypes=[],
                types=["Creature"],
                subtypes=["Soldier"],
            ),
        ],
    ),
    ("Gluttonous Troll", [
     sn(supertypes=[], types=["Artifact"], subtypes=["Food"])]),
    (
        "Army of the Damned",
        [
            sn(
                power="2",
                toughness="2",
                supertypes=[],
                types=["Creature"],
                subtypes=["Zombie"],
            )
        ],
    ),
    ("Nacatl War-Pride", [sn(supertypes=[], types=[], subtypes=[])]),
    (
        "Aether Chaser",
        [
            sn(
                power="1",
                toughness="1",
                supertypes=[],
                types=["Artifact", "Creature"],
                subtypes=["Servo"],
            )
        ],
    ),
    (
        "Stangg",
        [
            sn(
                name="Stangg Twin",
                power="3",
                toughness="4",
                supertypes=["Legendary"],
                types=["Creature"],
                subtypes=["Human", "Warrior"],
            )
        ],
    ),
    (
        "Ajani, Strength of the Pride",
        [
            sn(
                name="Ajani's Pridemate",
                power="2",
                toughness="2",
                supertypes=[],
                types=["Creature"],
                subtypes=["Cat", "Soldier"],
            )
        ],
    ),
    (
        "Boris Devilboon",
        [
            sn(
                name="Minor Demon",
                power="1",
                toughness="1",
                supertypes=[],
                types=["Creature"],
                subtypes=["Demon"],
            )
        ],
    ),
    (
        "Cloudseeder",
        [
            sn(
                name="Cloud Sprite",
                power="1",
                toughness="1",
                supertypes=[],
                types=["Creature"],
                subtypes=["Faerie"],
            )
        ],
    ),
    (
        "Estrid, the Masked",
        [
            sn(
                name="Mask",
                supertypes=[],
                types=["Enchantment"],
                subtypes=["Aura"],
            )
        ],
    ),
    (
        "Everquill Phoenix",
        [
            sn(
                name="Feather",
                supertypes=[],
                types=["Artifact"],
                subtypes=[],
            )
        ],
    ),
    (
        "Gemini Engine",
        [
            sn(
                name="Twin",
                supertypes=[],
                types=["Artifact", "Creature"],
                subtypes=["Construct"],
            )
        ],
    ),
    (
        "Goblin Kaboomist",
        [
            sn(
                name="Land Mine",
                supertypes=[],
                types=["Artifact"],
                subtypes=[],
            )
        ],
    ),
    (
        "Goldmeadow Lookout",
        [
            sn(
                name="Goldmeadow Harrier",
                power="1",
                toughness="1",
                supertypes=[],
                types=["Creature"],
                subtypes=["Kithkin", "Soldier"],
            )
        ],
    ),
    (
        "Jungle Patrol",
        [
            sn(
                name="Wood",
                power="0",
                toughness="1",
                supertypes=[],
                types=["Creature"],
                subtypes=["Wall"],
            )
        ],
    ),
    (
        "Kher Keep",
        [
            sn(
                name="Kobolds of Kher Keep",
                power="0",
                toughness="1",
                supertypes=[],
                types=["Creature"],
                subtypes=["Kobold"],
            )
        ],
    ),
    (
        "Koma, Cosmos Serpent",
        [
            sn(
                name="Koma's Coil",
                power="3",
                toughness="3",
                supertypes=[],
                types=["Creature"],
                subtypes=["Serpent"],
            )
        ],
    ),
    (
        "Llanowar Mentor",
        [
            sn(
                name="Llanowar Elves",
                power="1",
                toughness="1",
                supertypes=[],
                types=["Creature"],
                subtypes=["Elf", "Druid"],
            )
        ],
    ),
    (
        "Replicating Ring",
        [sn(name="Replicated Ring", supertypes=[
            "Snow"], types=["Artifact"], subtypes=[])],
    ),
    (
        "Marit Lage's Slumber",
        [sn(name="Marit Lage", power="20", toughness="20", supertypes=[
            "Legendary"], types=["Creature"], subtypes=["Avatar"])]
    ),
    (
        "Svella, Ice Shaper",
        [sn(name="Icy Manalith", supertypes=["Snow"], types=["Artifact"], subtypes=[])]
    ),
    (
        "Master of the Hunt",
        [sn(name="Wolves of the Hunt", power="1", toughness="1",
            supertypes=[], types=["Creature"], subtypes=["Wolf"])]
    ),
    (
        "Nahiri, the Lithomancer",
        [sn(power="1", toughness="1", supertypes=[], types=["Creature"], subtypes=["Kor", "Soldier"]),
         sn(name="Stoneforged Blade", supertypes=[], types=["Artifact"], subtypes=["Equipment"])]
    ),
    (
        "Prossh, Skyraider of Kher",
        [sn(name="Kobolds of Kher Keep", power="0", toughness="1",
            supertypes=[], types=["Creature"], subtypes=["Kobold"])]
    )
]


@pytest.mark.parametrize("name,expected", test_cases)
def test_tokens(get_card, extractor, name, expected):
    card = get_card(name)
    tokens = extractor.extract(card)
    assert tokens == expected
