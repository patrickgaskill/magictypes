import lark
from lark import Lark, v_args
from lark.visitors import Visitor_Recursive, Visitor, Interpreter, Discard
from magic_objects.token import MagicToken
from magictypes import data_file, load_cards
from card import Card


class TokenExtractor:
    grammar: str
    parser: Lark

    color_map = {
        "white": "W",
        "blue": "U",
        "black": "B",
        "red": "R",
        "green": "G"
    }

    def __init__(self):
        with open("tokens2.lark") as f:
            self.grammar = f.read()
        self.parser = Lark(self.grammar, debug=True)

    def _tree_to_tokens(self, tree: lark.Tree) -> list[MagicToken]:
        tokens = []
        for creator in tree.find_data("creation"):
            characteristics = {"colors": [], "subtypes": [],
                               "types": [], "supertypes": []}

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
                elif t.type == "RULES_TEXT":
                    characteristics["text"] = str(t)
                elif t.type == "TOKEN_NAME":
                    characteristics["name"] = str(t)
                elif t.type == "LEGENDARY" and t == "legendary":
                    characteristics["supertypes"].append(str("Legendary"))
            print("characteristics=", characteristics)
            tokens.append(MagicToken(**characteristics))
        return tokens

    def extract_from_text(self, text: str) -> list[MagicToken]:
        tree = self.parser.parse(text)
        print(tree)
        print(tree.pretty())
        tokens = self._tree_to_tokens(tree)
        print(tokens)
        return tokens

    def extract_from_card(self, card: Card) -> list[MagicToken]:
        if not hasattr(card, "text"):
            return []
        return self.extract_from_text(card.text)


if __name__ == "__main__":
    extractor = TokenExtractor()
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
