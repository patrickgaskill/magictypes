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
    ("Gluttonous Troll", [sn(supertypes=[], types=["Artifact"], subtypes=["Food"])]),
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
    # (
    #     "Replicating Ring",
    #     sn(name="Replicated Ring", supertypes=["Snow"], types=["Artifact"]),
    # ),
]


@pytest.mark.parametrize("name,expected", test_cases)
def test_tokens(get_card, extractor, name, expected):
    card = get_card(name)
    tokens = extractor.extract(card)
    assert tokens == expected
