import pytest
from magic_objects.token import Token


test_cases = [
    ("Abhorrent Overlord", [Token(colors=["B"], types=[
     "creature"], subtypes=["Harpy"], power="1", toughness="1")]),
    ("Abstruse Interference",  [Token(colors=[], types=[
        "creature"], subtypes=["Eldrazi", "Scion"], power="1", toughness="1", text="Sacrifice this creature: Add {C}.")]),
    ("Abzan Ascendancy",  [Token(colors=["W"], types=[
        "creature"], subtypes=["Spirit"], power="1", toughness="1")]),
    ("Academy Manufactor", []),
    ("Acorn Catapult", [Token(colors=["G"], types=[
        "creature"], subtypes=["Squirrel"], power="1", toughness="1")]),
    ("Acorn Harvest", [Token(colors=["G"], types=[
        "creature"], subtypes=["Squirrel"], power="1", toughness="1")]),
    ("Advent of the Wurm", [Token(colors=["G"], types=[
        "creature"], subtypes=["Wurm"], power="5", toughness="5")]),
    ("Adverse Conditions",  [Token(colors=[], types=[
        "creature"], subtypes=["Eldrazi", "Scion"], power="1", toughness="1", text="Sacrifice this creature: Add {C}.")]),
    ("Aerie Worshippers",  [Token(colors=[], types=[
        "enchantment", "creature"], subtypes=["Bird"], power="2", toughness="2")]),
]


@pytest.mark.parametrize("name,expected", test_cases)
def test_tokens(get_card, extractor, name, expected):
    card = get_card(name)
    tokens = extractor.extract(card)
    assert tokens == expected
