from collections import defaultdict
from pathlib import Path

import regex
from lark import Lark, Token, Tree

from magicobjects import MagicCard, MagicToken


class TokenExtractor:
    has_investigate = (
        "Briarbridge Patrol",
        "Bygone Bishop",
        "Byway Courier",
        "Confirm Suspicions",
        "Confront the Unknown",
        "Daring Sleuth // Bearer of Overwhelming Truths",
        "Declaration in Stone",
        "Drownyard Explorers",
        # "Erdwal Illuminator",
        "Expose Evil",
        "Fleeting Memories",
        "Floodhound",
        "Funnel-Web Recluse",
        "Gone Missing",
        "Hard Evidence",
        "Humble the Brute",
        "Jace's Scrutiny",
        "Lonis, Cryptozoologist",
        "Magnifying Glass",
        "Ongoing Investigation",
        "Press for Answers",
        "Root Out",
        "Search the Premises",
        "Survive the Night",
        "Tamiyo's Journal",
        "Thraben Inspector",
        "Tireless Tracker",
        "Trail of Evidence",
        "Ulvenwald Mysteries",
        "Wavesifter",
        "Weirding Wood",
    )

    overrides = {
        "Master of the Wild Hunt Avatar": [
            {
                "colors": ["G"],
                "types": ["Creature"],
                "subtypes": ["Wolf"],
                "power": "2",
                "toughness": "2",
            },
            {
                "colors": ["G"],
                "types": ["Creature"],
                "subtypes": ["Antelope"],
                "power": "2",
                "toughness": "3",
                "keywords": ["Forestwalk"],
            },
            {
                "colors": ["G"],
                "types": ["Creature"],
                "subtypes": ["Cat"],
                "power": "3",
                "toughness": "2",
                "keywords": ["Shroud"],
            },
            {
                "colors": ["G"],
                "types": ["Creature"],
                "subtypes": ["Rhino"],
                "power": "4",
                "toughness": "4",
                "keywords": ["Trample"],
            },
        ],
        "Sarpadian Empires, Vol. VII": [
            {
                "colors": ["W"],
                "types": ["Creature"],
                "subtypes": ["Citizen"],
                "power": "1",
                "toughness": "1",
            },
            {
                "colors": ["U"],
                "types": ["Creature"],
                "subtypes": ["Camarid"],
                "power": "1",
                "toughness": "1",
            },
            {
                "colors": ["B"],
                "types": ["Creature"],
                "subtypes": ["Thrull"],
                "power": "1",
                "toughness": "1",
            },
            {
                "colors": ["R"],
                "types": ["Creature"],
                "subtypes": ["Goblin"],
                "power": "1",
                "toughness": "1",
            },
            {
                "colors": ["G"],
                "types": ["Creature"],
                "subtypes": ["Saproling"],
                "power": "1",
                "toughness": "1",
            },
        ],
        "Outlaws' Merriment": [
            {
                "colors": ["W", "R"],
                "types": ["Creature"],
                "subtypes": ["Human", "Warrior"],
                "power": "3",
                "toughness": "1",
                "keywords": ["Trample", "Haste"],
            },
            {
                "colors": ["W", "R"],
                "types": ["Creature"],
                "subtypes": ["Human", "Cleric"],
                "power": "2",
                "toughness": "1",
                "keywords": ["Lifelink", "Haste"],
            },
            {
                "colors": ["W", "R"],
                "types": ["Creature"],
                "subtypes": ["Human", "Rogue"],
                "power": "1",
                "toughness": "2",
                "keywords": ["Haste"],
                "text": "When this creature enters the battlefield, it deals 1 damage to any target.",
            },
        ],
    }

    color_map: dict[str, str] = {
        "white": "W",
        "blue": "U",
        "black": "B",
        "red": "R",
        "green": "G",
    }

    debug: bool

    def __init__(self, debug=False):
        self.debug = debug
        self._cache = {}
        with Path(__file__).with_name("grammar.lark").open("r") as f:
            self.parser = Lark(
                f.read(), regex=True, parser="earley", ambiguity="resolve"
            )

    def extract_from_text(self, text: str) -> list[MagicToken]:
        if not text:
            return []

        tree = self.parser.parse(text)
        if self.debug:
            print(tree.pretty())
        tokens = []

        for top_token in self.get_tokens_from_tree(tree):
            tokens.append(top_token)
            if top_token.text:
                if self.debug:
                    print(f"Parsing token text: {top_token.text}")

                # Replaced single-quoted rules with double quotes
                fixed_text = regex.sub(r"(?<!\w)'([^']+)'", r'"\1"', top_token.text)
                if self.debug:
                    print(f"With replaced quotes: {fixed_text}")

                # If the quoted text didn't end in a period, add one
                match = regex.search(r'"[^"]+[^.]"$', fixed_text)
                if self.debug:
                    print("Match:", match)
                if match:
                    fixed_text = fixed_text[:-1] + "." + fixed_text[-1:]

                if self.debug:
                    print(f"Token text changed to: {fixed_text}")
                subtokens = self.extract_from_text(fixed_text)
                tokens.extend(subtokens)

        return tokens

    def extract_from_card(self, card: MagicCard) -> list[MagicToken]:
        if card.name in TokenExtractor.overrides:
            return [
                MagicToken(**t, creator=card)
                for t in TokenExtractor.overrides[card.name]
            ]

        if card.name in self._cache:
            return [
                MagicToken(**{**t, "creator": card}) for t in self._cache[card.name]
            ]

        tokens = self.extract_from_text(card.text)

        if card.name in self.has_investigate:
            tokens.append(MagicToken.Clue)

        self._cache[card.name] = [t.asdict() for t in tokens]
        for t in tokens:
            t.creator = card
        return tokens

    def get_tokens_from_tree(self, tree):
        tokens = []
        for sentence in tree.find_data("sentence"):
            characteristics = defaultdict(list)
            rules = []

            for child in sentence.children:
                if isinstance(child, Tree) and (
                    child.data == "create" or child.data == "sentence_following_create"
                ):
                    for t in child.scan_values(lambda v: isinstance(v, Token)):
                        if t.type == "COLOR" and t in self.color_map:
                            characteristics["colors"].append(self.color_map[t])
                        elif t.type == "ALL_COLORS":
                            characteristics["colors"] = ["W", "U", "B", "R", "G"]
                        elif t.type == "SUBTYPE":
                            characteristics["subtypes"].append(str(t))
                        elif t.type == "TYPE":
                            characteristics["types"].append(str(t).capitalize())
                        elif t.type == "POWER":
                            characteristics["power"] = str(t)
                        elif t.type == "TOUGHNESS":
                            characteristics["toughness"] = str(t)
                        elif t.type == "KEYWORD":
                            keyword = str(t)
                            characteristics["keywords"].append(
                                keyword[0].upper() + keyword[1:]
                            )
                        elif t.type == "RULES_TEXT" or t.type == "INNER_RULES_TEXT":
                            # Replace a trailing comma with a period and uppercase the first letter
                            text = regex.sub(r",$", r".", str(t))
                            if text[-1] not in (".", '"', "'"):
                                text += "."
                            rules.append(text[0].upper() + text[1:])
                        elif t.type == "TOKEN_NAME" or t.type == "LEGENDARY_NAME":
                            characteristics["name"] = str(t)
                        elif t.type == "LEGENDARY":
                            characteristics["supertypes"].append(str("Legendary"))
                        elif t.type == "SNOW":
                            characteristics["supertypes"].append(str("Snow"))
                        elif t.type == "PREDEFINED_TOKEN":
                            tokens.append(getattr(MagicToken, str(t)))

            if rules:
                characteristics["text"] = "\n".join(rules)

            if characteristics:
                tokens.append(MagicToken(**characteristics))

        return tokens
