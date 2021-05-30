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
        self.parser = Lark(self.grammar, ambiguity="explicit")

    def _tree_to_tokens(self, tree: lark.Tree) -> list[MagicToken]:
        tokens = []
        for creator in tree.find_data("creation"):
            characteristics = {"colors": [], "subtypes": [],
                               "types": [], "supertypes": []}

            for t in creator.scan_values(lambda v: isinstance(v, lark.Token)):
                if t.type == "COLOR" and t in self.color_map:
                    characteristics["colors"].append(self.color_map[t])
                elif t.type == "SUBTYPES":
                    characteristics["subtypes"].append(str(t))
                elif t.type == "TYPES":
                    characteristics["types"].append(str(t).capitalize())
                elif t.type == "POWER":
                    characteristics["power"] = str(t)
                elif t.type == "TOUGHNESS":
                    characteristics["toughness"] = str(t)
                elif t.type == "RULES_TEXT":
                    characteristics["text"] = str(t)

            tokens.append(MagicToken(**characteristics))
        return tokens

    def extract(self, card: Card) -> list[MagicToken]:
        if not hasattr(card, "text"):
            return []

        tree = self.parser.parse(card.text)
        print(tree)
        print(tree.pretty())
        tokens = self._tree_to_tokens(tree)
        print(tokens)
        return tokens


if __name__ == "__main__":
    extractor = TokenExtractor()
    cards = load_cards()
    aerie = next(
        (c for c in cards if c.name == "Aerie Worshippers"),
        None,
    )
    print(aerie.text)
    tokens = extractor.extract(aerie)
    print(tokens)
