import pytest
from maximal_combinations import is_type_subset


test_cases = [
    ("Castle", "Animate Wall", True, False),
    ("Field of Dreams", "Castle", False, True),
    ("Field of Dreams", "Animate Wall", False, False),
    ("Honden of Cleansing Fire", "Night of Souls' Betrayal", False, True),
    ("Morophon, the Boundless", "Mistform Ultimus", False, False),
    ("Morophon, the Boundless", "Moritte of the Frost", True, False),
    ("Blades of Velis Vel", "Ego Erasure", False, False),
    ("Universal Automaton", "Realmwalker", False, True)
]


@pytest.mark.parametrize("name_a,name_b,expected_ab,expected_ba", test_cases)
def test_tokens(get_card, name_a, name_b, expected_ab, expected_ba):
    cardA = get_card(name_a)
    cardB = get_card(name_b)
    print(f"A) {name_a} supertypes:", cardA.supertypes)
    print(f"B) {name_b} supertypes:", cardB.supertypes)
    print(f"A) {name_a} types:", cardA.types)
    print(f"B) {name_b} types:", cardB.types)
    print(f"A) {name_a} subtypes:", cardA.subtypes)
    print(f"B) {name_b} subtypes:", cardB.subtypes)
    assert is_type_subset(cardA, cardB) == expected_ab
    assert is_type_subset(cardB, cardA) == expected_ba
