def ageless_sentinels(card):
    copy = card.copy()
    new_subtypes = ["Bird", "Giant"]
    copy.subtype_order = {s: i for i, s in enumerate(new_subtypes)}
    copy.subtypes = set(new_subtypes)
    copy.clear_cached_properties()
    return [copy]


def grist_the_hunger_tide(card):
    copy = card.copy()
    copy.types.add("Creature")
    copy.subtypes.add("Insect")
    copy.clear_cached_properties()
    return [copy]


global_variations = {
    "Grist, the Hunger Tide": grist_the_hunger_tide,
}

activated_variations = {
    "Ageless Sentinels": ageless_sentinels,
}
