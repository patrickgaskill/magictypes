def grist_the_hunger_tide(card):
    grist_copy = card.copy()
    grist_copy.types.add("Creature")
    grist_copy.subtypes.add("Insect")
    grist_copy.clear_cached_properties()
    return [grist_copy]


variations = {"Grist, the Hunger Tide": grist_the_hunger_tide}
