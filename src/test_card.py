import pytest
import magictypes


@pytest.fixture(scope="session")
def cards():
    return magictypes.load_cards()


@pytest.fixture
def get_card(cards):
    def _get_card(name):
        return next(
            (c for c in cards if c.name == name),
            None,
        )

    return _get_card


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