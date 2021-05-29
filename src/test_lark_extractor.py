import pytest
from magic_objects.token import Token


test_cases = [
    ("Abhorrent Overlord", [Token(colors=["B"], types=[
     "creature"], subtypes=["Harpy"], power="1", toughness="1")])
]


@pytest.mark.parametrize("name,expected", test_cases)
def test_tokens(get_card, extractor, name, expected):
    card = get_card(name)
    tokens = extractor.extract(card)
    assert tokens == expected
