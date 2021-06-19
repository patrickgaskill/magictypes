import pytest

from magicobjects import MagicToken


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Mistform Ultimus", True),
        ("Amorphous Axe", False),
        ("Runed Stalactite", False),
        ("Crib Swap", True),
        ("Amoeboid Changeling", True),
        ("Moritte of the Frost", True),
    ],
)
def test_is_every_creature_type(mtgjsondata, name, expected):
    assert mtgjsondata.get_card_by_name(name).is_every_creature_type == expected


@pytest.mark.parametrize(
    "name_a,name_b,expected_ab,expected_ba",
    [
        ("Castle", "Animate Wall", True, False),
        ("Field of Dreams", "Castle", False, True),
        ("Field of Dreams", "Animate Wall", False, False),
        ("Honden of Cleansing Fire", "Night of Souls' Betrayal", False, True),
        ("Morophon, the Boundless", "Mistform Ultimus", False, False),
        ("Morophon, the Boundless", "Moritte of the Frost", True, False),
        ("Blades of Velis Vel", "Ego Erasure", False, False),
        ("Universal Automaton", "Realmwalker", False, True),
    ],
)
def test_is_type_subset(mtgjsondata, name_a, name_b, expected_ab, expected_ba):
    card_a = mtgjsondata.get_card_by_name(name_a)
    card_b = mtgjsondata.get_card_by_name(name_b)
    print(f"A) {name_a} supertypes:", card_a.supertypes)
    print(f"B) {name_b} supertypes:", card_b.supertypes)
    print(f"A) {name_a} types:", card_a.types)
    print(f"B) {name_b} types:", card_b.types)
    print(f"A) {name_a} subtypes:", card_a.subtypes)
    print(f"B) {name_b} subtypes:", card_b.subtypes)
    assert card_a.is_type_subset(card_b) == expected_ab
    assert card_b.is_type_subset(card_a) == expected_ba


@pytest.mark.parametrize(
    "name,expected",
    [
        (
            "Balefire Liege",
            (
                (),
                ("Creature",),
                ("Horror", "Spirit"),
            ),
        ),
        (
            "Krovikan Horror",
            (
                (),
                ("Creature",),
                ("Horror", "Spirit"),
            ),
        ),
    ],
)
def test_type_key(mtgjsondata, name, expected):
    card = mtgjsondata.get_card_by_name(name)
    assert card.type_key == expected


@pytest.mark.parametrize(
    "token,expected",
    [
        (
            MagicToken.Gold,
            MagicToken(
                types=["Artifact"],
                subtypes=["Gold"],
                text="Sacrifice this artifact: Add one mana of any color.",
            ),
        ),
        (
            MagicToken.Walker,
            MagicToken(
                name="Walker",
                colors=["B"],
                types=["Creature"],
                subtypes=["Zombie"],
                power="2",
                toughness="2",
            ),
        ),
    ],
)
def test_predefined_tokens(token, expected):
    assert token == expected
