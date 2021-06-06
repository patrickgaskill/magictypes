from lark import Lark

texts = [
    # create, it has quoted text
    """Devoid (This card has no color.)
Counter target spell unless its controller pays {1}. You create a 1/1 colorless Eldrazi Scion creature token. It has \"Sacrifice this creature: Add {C}.\" ({C} represents colorless mana.)""",

    # create inside quotes
    """+1: Put a +1/+1 counter on each of up to two target creatures.
−2: Return target creature card with mana value 2 or less from your graveyard to the battlefield.
−7: You get an emblem with \"At the beginning of your end step, create three 1/1 white Cat creature tokens with lifelink.\"""",

    # create, create, it has quoted text in the middle
    """+2: Create a 1/1 white Kor Soldier creature token. You may attach an Equipment you control to it.
−2: You may put an Equipment card from your hand or graveyard onto the battlefield.
−10: Create a colorless Equipment artifact token named Stoneforged Blade. It has indestructible, "Equipped creature gets +5/+5 and has double strike," and equip {0}.
Nahiri, the Lithomancer can be your commander.""",

    # create, then unrelated quoted text
    """Whenever a creature you control dies, put a loyalty counter on Lolth, Spider Queen.
0: You draw a card and you lose 1 life.
−3: Create two 2/1 black Spider creature tokens with menace and reach.
−8: You get an emblem with \"Whenever an opponent is dealt combat damage by one or more creatures you control, if that player lost less than 8 life this turn, they lose life equal to the difference.\"""",

    # unrelated quoted text
    """Until end of turn, target creature gets +2/+0 and gains \"When this creature dies, return it to the battlefield tapped under its owner's control.\"""",

    # create, no quoted text
    """Create a 5/5 green Wurm creature token with trample."""

    # unrelated text
    """Target player draws three cards."""
]

grammar = """
start: /\w+/

%import common.WS
%ignore WS
"""

parser = Lark(grammar, ambiguity="explicit")

for text in texts:
    tree = parser.parse(text)
    print(tree.pretty())
