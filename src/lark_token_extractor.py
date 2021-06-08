import re
import lark
from collections import defaultdict
from lark import Lark, v_args
from lark.visitors import Visitor_Recursive, Visitor, Interpreter, Discard
from magic_objects.token import MagicToken
from magictypes import data_file, load_cards
from card import Card


class TokenExtractor:
    debug: bool
    grammar: str
    parser: Lark

    color_map = {
        "white": "W",
        "blue": "U",
        "black": "B",
        "red": "R",
        "green": "G"
    }

    overrides = {
        "Sarpadian Empires, Vol. VII": [
            MagicToken(types=["Creature"], power="1",
                       toughness="1", colors=["W"], subtypes=["Citizen"]),
            MagicToken(types=["Creature"], power="1",
                       toughness="1", colors=["U"], subtypes=["Camarid"]),
            MagicToken(types=["Creature"], power="1",
                       toughness="1", colors=["B"], subtypes=["Thrull"]),
            MagicToken(types=["Creature"], power="1",
                       toughness="1", colors=["R"], subtypes=["Goblin"]),
            MagicToken(types=["Creature"], power="1", toughness="1",
                       colors=["G"], subtypes=["Saproling"]),
        ]
    }

    def __init__(self, debug: bool = False):
        self.debug = debug
        with open("tokens4.lark") as f:
            self.grammar = f.read()
        self.parser = Lark(self.grammar, ambiguity="resolve")

    def _tree_to_tokens(self, tree: lark.Tree) -> list[MagicToken]:
        tokens = []
        for creator in tree.find_data("create"):
            characteristics = defaultdict(list)

            for t in creator.scan_values(lambda v: isinstance(v, lark.Token)):
                if t.type == "COLOR" and t in self.color_map:
                    characteristics["colors"].append(self.color_map[t])
                elif t.type == "SUBTYPE":
                    characteristics["subtypes"].append(str(t))
                elif t.type == "TYPE":
                    characteristics["types"].append(str(t).capitalize())
                elif t.type == "POWER":
                    characteristics["power"] = str(t)
                elif t.type == "TOUGHNESS":
                    characteristics["toughness"] = str(t)
                elif t.type == "KEYWORD":
                    characteristics["keywords"].append(str(t))
                elif t.type == "RULES_TEXT":
                    characteristics["text"] = str(t)
                elif t.type == "TOKEN_NAME":
                    characteristics["name"] = str(t)
                elif t.type == "LEGENDARY":
                    characteristics["supertypes"].append(str("Legendary"))
                elif t.type == "SNOW":
                    characteristics["supertypes"].append(str("Snow"))
                elif t.type == "PREDEFINED_SUBTYPE":
                    tokens.append(MagicToken(predefined=str(t)))

            if characteristics:
                # print("characteristics=", characteristics)
                tokens.append(MagicToken(**characteristics))
        return tokens

    def extract_from_text(self, text: str) -> list[MagicToken]:
        tree = self.parser.parse(text)
        if self.debug:
            print(tree)
            print(tree.pretty())
            assert len(list(tree.find_data("_ambig"))) == 0

        tokens = []
        new_tokens = self._tree_to_tokens(tree)

        for new_token in new_tokens:
            tokens.append(new_token)
            if new_token.text:
                subtokens = self.extract_from_text(
                    re.sub(r" '([^']+)'", r'"\1"', new_token.text))
                tokens.extend(subtokens)

        if self.debug:
            print(tokens)
        return tokens

    def extract_from_card(self, card: Card) -> list[MagicToken]:
        if card.name in self.overrides:
            return self.overrides[card.name]

        if not hasattr(card, "text"):
            return []
        return self.extract_from_text(card.text)


if __name__ == "__main__":
    extractor = TokenExtractor(debug=True)
    cards = load_cards()
    card = next(
        (c for c in cards if c.name == "Abhorrent Overlord"),
        None,
    )
    print(card.text)
    tokens = extractor.extract_from_card(card)
    text = "Flying\nWhen Abhorrent Overlord enters the battlefield, create a number of 1/1 black Harpy creature tokens with flying equal to your devotion to black. (Each {B} in the mana costs of permanents you control counts toward your devotion to black.)\nAt the beginning of your upkeep, sacrifice a creature."
    # text = "Dark Depths enters the battlefield with ten ice counters on it. {3}: Remove an ice counter from Dark Depths. When Dark Depths has no ice counters on it, sacrifice it. If you do, create a 20/20 black Avatar creature token with flying and indestructible."
    tokens = extractor.extract_from_text(text)
    # print(tokens)
