import re
from collections import defaultdict
from pathlib import Path

from lark import Lark, Token

from magicobjects import MagicObject, MagicToken


class TokenExtractor:
    color_map = {"white": "W", "blue": "U", "black": "B", "red": "R", "green": "G"}

    def __init__(self):
        with Path(__file__).with_name("grammar.lark").open("r") as f:
            self.parser = Lark(
                f.read(), regex=True, parser="earley", ambiguity="resolve"
            )

    def extract_from_text(self, text: str) -> list[MagicToken]:
        if not text:
            return []

        tree = self.parser.parse(text)
        tokens = []

        for top_token in self.tree_to_tokens(tree):
            tokens.append(top_token)
            if top_token.text:
                fixed_text = re.sub(r"'([^']+)'", r'"\1"', top_token.text)
                subtokens = self.extract_from_text(fixed_text)
                tokens.extend(subtokens)

        return tokens

    def extract_from_card(self, card: MagicObject) -> list[MagicToken]:
        return self.extract_from_text(card.text)

    def tree_to_tokens(self, tree):
        tokens = []
        for creator in tree.find_data("creation_sentences"):
            characteristics = defaultdict(list)

            for t in creator.scan_values(lambda v: isinstance(v, Token)):
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
                    # Replace a trailing comma with a period and uppercase the first letter
                    text = re.sub(r",$", r".", str(t))
                    characteristics["text"] = text[0].upper() + text[1:]
                elif t.type == "TOKEN_NAME" or t.type == "LEGENDARY_NAME":
                    characteristics["name"] = str(t)
                elif t.type == "LEGENDARY":
                    characteristics["supertypes"].append(str("Legendary"))
                elif t.type == "SNOW":
                    characteristics["supertypes"].append(str("Snow"))
                elif t.type == "PREDEFINED_TOKEN":
                    tokens.append(getattr(MagicToken, str(t)))

            if characteristics:
                tokens.append(MagicToken(**characteristics))

        return tokens


if __name__ == "__main__":
    pass
