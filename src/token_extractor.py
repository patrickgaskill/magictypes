import json
import re
from itertools import chain
from types import SimpleNamespace


class TokenExtractor:
    def __init__(self):
        self._load_enum_values()
        self._load_card_types()
        self._make_pattern()

    def _load_enum_values(self):
        with open("data/EnumValues.json", "r") as f:
            self.enum_values = json.load(
                f, object_hook=lambda d: SimpleNamespace(**d)
            ).data

    def _load_card_types(self):
        with open("data/CardTypes.json", "r") as f:
            self.card_types = json.load(f)["data"]

    def _make_pattern(self):
        colors = "|".join(
            ["white", "blue", "black", "red", "green", "colorless", "and"]
        )

        numbers = "|".join(
            [
                "an?",
                r"a\ number\ of",
                "X",
                "two",
                "three",
                "four",
                "five",
                "six",
                "seven",
                "eight",
                "nine",
                "ten",
                "eleven",
                "twelve",
                "thirteen",
            ]
        )
        types = "|".join(self.card_types.keys())
        supertypes = "|".join(self.card_types["artifact"]["superTypes"])
        subtypes = "|".join(chain(*[v["subTypes"] for v in self.card_types.values()]))

        pattern = re.compile(
            rf"""create\s
                (?:(?P<legendary_name>[^,]+),\s)?
                (?:{numbers})\s
                (?:tapped\s)?
                (?P<supertypes>(?:(?:{supertypes})\s)+)?
                (?:(?P<power>[\dX*]+)\/(?P<toughness>[\dX*]+)\s)?
                (?P<colors1>(?:(?:{colors})\s)+)?
                (?P<subtypes>(?:(?:{subtypes})\s)+)?
                (?P<types>(?:(?:{types})\s)+)?
                tokens?
                (?:\ that’s\ (?P<colors2>(?:(?:{colors})[., ]+)+))?""",
            re.IGNORECASE | re.VERBOSE,
        )

        self.pattern = pattern

    def extract(self, card):
        if not hasattr(card, "text"):
            return []

        matches = re.findall(self.pattern, card.text)
        tokens = [self._make_token_from_match(m) for m in matches]
        return tokens

    def _make_token_from_match(self, match):
        (
            name,
            supertypes,
            power,
            toughness,
            colors1,
            subtypes,
            types,
            colors2,
        ) = match

        token = SimpleNamespace(
            types=self._format_matched_types(types),
            subtypes=self._format_matched_types(subtypes),
            supertypes=self._format_matched_types(supertypes),
        )

        if "Food" in token.subtypes and "Artifact" not in token.types:
            token.types.append("Artifact")

        if name != "":
            token.name = name

        if power != "":
            token.power = power

        if toughness != "":
            token.toughness = toughness

        return token

    def _format_matched_types(self, types):
        if types == "":
            return []

        return [t.capitalize() for t in types.strip().split(" ")]