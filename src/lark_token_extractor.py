import lark
from lark import Lark, v_args
from lark.visitors import Visitor_Recursive, Visitor, Interpreter, Discard
from magic_objects.token import Token
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
        with open("tokens.lark") as f:
            self.grammar = f.read()
        self.parser = Lark(grammar, ambiguity="explicit")

    def tree_to_tokens(self, tree: lark.Tree) -> list[Token]:
        tokens = []
        for creator in tree.find_data("token_creator"):
            characteristics = {"colors": [], "subtypes": [],
                               "types": [], "supertypes": []}

            for t in creator.scan_values(lambda v: isinstance(v, lark.Token)):
                if t.type == "COLOR" and t in self.color_map:
                    characteristics["colors"].append(self.color_map[t])
                elif t.type == "SUBTYPES":
                    characteristics["subtypes"].append(str(t))
                elif t.type == "TYPES":
                    characteristics["types"].append(str(t))
                elif t.type == "POWER":
                    characteristics["power"] = str(t)
                elif t.type == "TOUGHNESS":
                    characteristics["toughness"] = str(t)

            tokens.append(Token(**characteristics))
        return tokens

    def extract(self, card: Card) -> list[Token]:
        if not hasattr(card, "text"):
            return []

        tree = self.parser.parse(card.text)
        return self.tree_to_tokens(tree)


with open("tokens.lark") as f:
    grammar = f.read()

parser = Lark(grammar, ambiguity="explicit")

test_text = """Flying

When Abhorrent Overlord enters the battlefield, create a number of 1/1 black Harpy creature tokens with flying equal to your devotion to black. (Each {B} in the mana costs of permanents you control counts toward your devotion to black.)

At the beginning of your upkeep, sacrifice a creature."""


def tree_to_tokens(tree: lark.Tree) -> Token:
    color_map = {
        "white": "W",
        "blue": "U",
        "black": "B",
        "red": "R",
        "green": "G"
    }

    tokens = []

    for creator in tree.find_data("token_creator"):
        characteristics = {"colors": [], "subtypes": [],
                           "types": [], "supertypes": []}

        for t in creator.scan_values(lambda v: isinstance(v, lark.Token)):
            if t.type == "COLOR" and t in color_map:
                characteristics["colors"].append(color_map[t])
            elif t.type == "SUBTYPES":
                characteristics["subtypes"].append(str(t))
            elif t.type == "TYPES":
                characteristics["types"].append(str(t))
            elif t.type == "POWER":
                characteristics["power"] = str(t)
            elif t.type == "TOUGHNESS":
                characteristics["toughness"] = str(t)

        tokens.append(Token(**characteristics))

    return tokens


def test():
    tree = parser.parse(test_text)
    print(tree)
    print(tree.pretty())
    token = tree_to_tokens(tree)
    print(token)
    # extractor = TokenExtractor()
    # tokens = extractor.extract()


if __name__ == '__main__':
    test()
