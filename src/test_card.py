import pytest


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
def test_is_every_creature_type(get_card, name, expected):
    assert get_card(name).is_every_creature_type == expected
