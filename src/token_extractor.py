import json
import re
from types import SimpleNamespace


class TokenExtractor:
    def __init__(self):
        self._load_enum_values()
        self._make_pattern()

    def _load_enum_values(self):
        with open("data/EnumValues.json", "r") as f:
            self.enum_values = json.load(
                f, object_hook=lambda d: SimpleNamespace(**d)
            ).data

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
        types = "|".join(self.enum_values.card.types)
        supertypes = "|".join(self.enum_values.card.supertypes)
        subtypes = "|".join(self.enum_values.card.subtypes)

        pattern = re.compile(
            rf"""create\s
                (?:(?P<legendary_name>[^,]+),\s)?
                (?:{numbers})\s
                (?:tapped\s)?
                (?P<supertypes>(?:(?:{supertypes})\s)+)?
                (?:(?P<power>[\dX*]+)\/(?P<toughness>[\dX*]+)\s)?
                (?P<colors1>(?:(?:{colors})\s)+)?
                (?P<subtypes>(?:(?:{subtypes})\s)+)?
                (?P<types>(?:(?:{types})\s)+)
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
            legendary_name,
            supertypes,
            power,
            toughness,
            colors1,
            subtypes,
            types,
            colors2,
        ) = match

        return SimpleNamespace(
            types=self._format_matched_types(types),
            subtypes=self._format_matched_types(subtypes),
            supertypes=self._format_matched_types(supertypes),
        )

    def _format_matched_types(self, types):
        if types == "":
            return []

        return [t.capitalize() for t in types.strip().split(" ")]
