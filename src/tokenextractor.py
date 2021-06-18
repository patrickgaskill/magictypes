from pathlib import Path

from lark import Lark

from magicobjects import MagicObject


class TokenExtractor:
    def __init__(self):
        p = Path(__file__).with_name("grammar.lark")
        with p.open("r") as f:
            self.parser = Lark(f.read(), parser="earley")

    def extract(self, card: MagicObject) -> list[MagicObject]:
        return []


if __name__ == "__main__":
    pass
