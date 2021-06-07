from lark import Lark

texts = [
    # create, it has quoted text
    """Devoid (This card has no color.)
Counter target spell unless its controller pays {1}. You create a 1/1 colorless Eldrazi Scion creature token. It has \"Sacrifice this creature: Add {C}.\" ({C} represents colorless mana.)""",

    # create inside quotes
    """+1: Put a +1/+1 counter on each of up to two target creatures.
-2: Return target creature card with mana value 2 or less from your graveyard to the battlefield.
-7: You get an emblem with \"At the beginning of your end step, create three 1/1 white Cat creature tokens with lifelink.\"""",

    # create, create, it has quoted text in the middle
    """+2: Create a 1/1 white Kor Soldier creature token. You may attach an Equipment you control to it.
-2: You may put an Equipment card from your hand or graveyard onto the battlefield.
-10: Create a colorless Equipment artifact token named Stoneforged Blade. It has indestructible, "Equipped creature gets +5/+5 and has double strike," and equip {0}.
Nahiri, the Lithomancer can be your commander.""",

    # create, then unrelated quoted text
    """Whenever a creature you control dies, put a loyalty counter on Lolth, Spider Queen.
0: You draw a card and you lose 1 life.
-3: Create two 2/1 black Spider creature tokens with menace and reach.
-8: You get an emblem with \"Whenever an opponent is dealt combat damage by one or more creatures you control, if that player lost less than 8 life this turn, they lose life equal to the difference.\"""",

    # unrelated quoted text
    """Until end of turn, target creature gets +2/+0 and gains \"When this creature dies, return it to the battlefield tapped under its owner's control.\"""",

    # create, no quoted text
    """Create a 5/5 green Wurm creature token with trample.""",

    # unrelated text
    """Target player draws three cards.""",

    # vanilla
    "",

    # french vanilla
    "Flying",

    """Create two 1/1 green Squirrel creature tokens.
Flashback—{1}{G}, Pay 3 life. (You may cast this card from your graveyard for its flashback cost. Then exile it.)""",

    """Creatures you control get +1/+1 until end of turn.
Fateful hour — If you have 5 or less life, those creatures gain indestructible until end of turn. (Damage and effects that say "destroy" don't destroy them.)""",

    """Creatures you control have menace.
-2: Amass 2. (Put two +1/+1 counters on an Army you control. If you don't control one, create a 0/0 black Zombie Army creature token first.)"""
]

grammar = r"""
start: [paragraph (_NEWLINE paragraph)*]
paragraph: (keywords reminder?) | loyalty_ability | (sentence | reminder)+
keywords: WORD+ ("," WORD+)*
sentence: (WORD~1..2 "—" | WORD | SYMBOL) (WORD | INT | ":" | "," | "'" | SYMBOL | power_toughness | power_toughness_modifier | quoted_text)+ (quoted_ending | ".")
reminder: "(" sentence+ ")"
loyalty_ability: LOYALTY_COST ":" sentence (sentence)* reminder?
LOYALTY_COST: ["+" | "-"] INT
SYMBOL: "{" (INT | "C" | "G") "}"
power_toughness: INT "/" INT
power_toughness_modifier: ("+" | "-") INT "/" ("+" | "-") INT
quoted_text: "\"" (WORD | INT | ":" | "," | "'" | SYMBOL | power_toughness | power_toughness_modifier)* "\""
quoted_ending: "\"" (WORD | INT | ":" | "," | "'" | SYMBOL | power_toughness | power_toughness_modifier)+ ".\""

WORD: /\b[^\d\W]+\b/
%import common.INT
%import common.NEWLINE -> _NEWLINE
%import common.WS_INLINE
%ignore WS_INLINE
"""

parser = Lark(grammar, ambiguity="explicit", debug=True)

for text in texts:
    print(text)
    tree = parser.parse(text)
    print(tree)
    print(tree.pretty())
