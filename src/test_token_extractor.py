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
                colors=["W"]
            ),
            sn(
                power="1",
                toughness="1",
                supertypes=[],
                types=["Creature"],
                subtypes=["Soldier"],
                colors=["W"]
            ),
        ],
    ),
    ("Gluttonous Troll", [
     sn(supertypes=[], types=["Artifact"], subtypes=["Food"], colors=[])]),
    (
        "Army of the Damned",
        [
            sn(
                power="2",
                toughness="2",
                supertypes=[],
                types=["Creature"],
                subtypes=["Zombie"],
                colors=["B"]
            )
        ],
    ),
    ("Nacatl War-Pride",
     [sn(supertypes=[], types=[], subtypes=[], colors=[])]),
    (
        "Aether Chaser",
        [
            sn(
                power="1",
                toughness="1",
                supertypes=[],
                types=["Artifact", "Creature"],
                subtypes=["Servo"],
                colors=[]
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
                colors=["R", "G"]
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
                colors=["W"]
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
                colors=["B", "R"]
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
                colors=["U"]
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
                colors=["W"]
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
                colors=["R"]
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
                colors=[]
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
                colors=[]
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
                colors=["W"]
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
                colors=["G"]
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
                colors=["R"]
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
                colors=["U"]
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
                colors=["G"]
            )
        ],
    ),
    (
        "Replicating Ring",
        [sn(name="Replicated Ring", supertypes=[
            "Snow"], types=["Artifact"], subtypes=[], colors=[])],
    ),
    (
        "Marit Lage's Slumber",
        [sn(name="Marit Lage", power="20", toughness="20", supertypes=[
            "Legendary"], types=["Creature"], subtypes=["Avatar"], colors=["B"])]
    ),
    (
        "Svella, Ice Shaper",
        [sn(name="Icy Manalith", supertypes=["Snow"],
            types=["Artifact"], subtypes=[], colors=[])]
    ),
    (
        "Master of the Hunt",
        [sn(name="Wolves of the Hunt", power="1", toughness="1",
            supertypes=[], types=["Creature"], subtypes=["Wolf"], colors=["G"])]
    ),
    (
        "Nahiri, the Lithomancer",
        [sn(power="1", toughness="1", supertypes=[], types=["Creature"], subtypes=["Kor", "Soldier"], colors=["W"]),
         sn(name="Stoneforged Blade", supertypes=[], types=["Artifact"], subtypes=["Equipment"], colors=[])]
    ),
    (
        "Prossh, Skyraider of Kher",
        [sn(name="Kobolds of Kher Keep", power="0", toughness="1",
            supertypes=[], types=["Creature"], subtypes=["Kobold"], colors=["R"])]
    ),
    (
        "Domri, Chaos Bringer",
        [sn(power="4", toughness="4", supertypes=[], types=[
            "Creature"], subtypes=["Beast"], colors=["R", "G"])]
    ),
    # (
    #     "Godsire",
    #     [sn(power="8", toughness="8", supertypes=[], types=[
    #         "Creature"], subtypes=["Beast"], colors=["W", "R", "G"])]
    # ),
    # (
    #     "Hazezon Tamar",
    #     [sn(power="1", toughness="1", supertypes=[], types=[
    #         "Creature"], subtypes=["Sand", "Warrior"], colors=["W", "R", "G"])]
    # ),
    # (
    #     "Sarpadian Empires, Vol. VII",
    #     [sn(power="1", toughness="1", supertypes=[], types=[
    #         "Creature"], subtypes=["Citizen"], colors=["W"]),
    #         sn(power="1", toughness="1", supertypes=[], types=[
    #             "Creature"], subtypes=["Camarid"], colors=["U"]),
    #         sn(power="1", toughness="1", supertypes=[], types=[
    #             "Creature"], subtypes=["Thrull"], colors=["B"]),
    #         sn(power="1", toughness="1", supertypes=[], types=[
    #             "Creature"], subtypes=["Goblin"], colors=["R"]),
    #         sn(power="1", toughness="1", supertypes=[], types=[
    #             "Creature"], subtypes=["Saproling"], colors=["G"])]
    # ),
    (
        "Wasitora, Nekoru Queen",
        [sn(power="3", toughness="3", supertypes=[], types=[
            "Creature"], subtypes=["Cat", "Dragon"], colors=["B", "R", "G"])]
    ),
]


@pytest.mark.parametrize("name,expected", test_cases)
def test_tokens(get_card, extractor, name, expected):
    card = get_card(name)
    tokens = extractor.extract(card)
    assert tokens == expected
