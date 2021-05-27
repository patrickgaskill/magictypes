import json
from itertools import chain, combinations
from magictypes import data_file


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


with data_file("CardTypes.json").open() as f:
    card_types_data = json.load(f)["data"]

supertypes = card_types_data["artifact"]["superTypes"]
supertypes.remove("Ongoing")
print(supertypes)

types = list(card_types_data.keys())
types.remove("conspiracy")
types.remove("phenomenon")
types.remove("plane")
types.remove("scheme")
types.remove("vanguard")
print(types)

card_types_data["planeswalker"]["subTypes"].remove("Abian")
card_types_data["planeswalker"]["subTypes"].remove("B.O.B.")
card_types_data["planeswalker"]["subTypes"].remove("Duck")
card_types_data["planeswalker"]["subTypes"].remove("Dungeon")
card_types_data["planeswalker"]["subTypes"].remove("Inzerva")
card_types_data["planeswalker"]["subTypes"].remove("Master")
card_types_data["planeswalker"]["subTypes"].remove("Urza")

for t in types:
    print(card_types_data[t]["subTypes"])

type_combos = list(
    powerset([*supertypes, *card_types_data["enchantment"]["subTypes"]]))
for combo in type_combos:
    print(combo)

print(len(type_combos))
