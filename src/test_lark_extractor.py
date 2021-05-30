import pytest
from magic_objects.token import MagicToken


test_cases = [
    ("Merfolk of the Pearl Trident", []),
    ("Akrasan Squire", []),
    ("Abhorrent Overlord", [MagicToken(colors=["B"], types=[
     "Creature"], subtypes=["Harpy"], power="1", toughness="1")]),
    ("Abstruse Interference",  [MagicToken(colors=[], types=[
        "Creature"], subtypes=["Eldrazi", "Scion"], power="1", toughness="1", text="Sacrifice this creature: Add {C}.")]),
    ("Abzan Ascendancy",  [MagicToken(colors=["W"], types=[
        "Creature"], subtypes=["Spirit"], power="1", toughness="1")]),
    ("Academy Manufactor", []),
    ("Acorn Catapult", [MagicToken(colors=["G"], types=[
        "Creature"], subtypes=["Squirrel"], power="1", toughness="1")]),
    ("Acorn Harvest", [MagicToken(colors=["G"], types=[
        "Creature"], subtypes=["Squirrel"], power="1", toughness="1")]),
    ("Advent of the Wurm", [MagicToken(colors=["G"], types=[
        "Creature"], subtypes=["Wurm"], power="5", toughness="5")]),
    ("Adverse Conditions",  [MagicToken(colors=[], types=[
        "Creature"], subtypes=["Eldrazi", "Scion"], power="1", toughness="1", text="Sacrifice this creature: Add {C}.")]),
    ("Aerie Worshippers",  [MagicToken(colors=["U"], types=[
        "Enchantment", "Creature"], subtypes=["Bird"], power="2", toughness="2")]),
    ("Aether Chaser", [MagicToken(colors=[], types=[
        "Artifact", "Creature"], subtypes=["Servo"], power="1", toughness="1")]),
    ("Aether Mutation", [MagicToken(colors=["G"], types=[
        "Creature"], subtypes=["Saproling"], power="1", toughness="1")])
]


@ pytest.mark.parametrize("name,expected", test_cases)
def test_tokens(get_card, extractor, name, expected):
    card = get_card(name)
    print(getattr(card, "text", "No text"))
    tokens = extractor.extract(card)
    assert tokens == expected
