from magicobjects import MagicObject


def after_effects(card: MagicObject) -> list[MagicObject]:
    returned_cards = [card.copy()]

    # Moritte of the Frost is a copy so doesn't see the following type-changing effects
    if card.is_permanent:
        moritte_copy = card.copy()
        moritte_copy.supertypes |= {"Legendary", "Snow"}
        if "Creature" in moritte_copy.types:
            # moritte_copy.subtypes |= card.all_creature_types
            moritte_copy.keywords.add("Changeling")
        returned_cards.append(moritte_copy)

    # Dermotaxi (copy creature from GY and add Vehicle artifact)
    if not card.is_token and "Creature" in card.types:
        dermotaxi_copy = card.copy()
        dermotaxi_copy.types.add("Artifact")
        dermotaxi_copy.subtypes.add("Vehicle")
        returned_cards.append(dermotaxi_copy)

    for affected_card in returned_cards:
        # Enchanted Evening (all permanents are enchantments)
        if affected_card.is_permanent:
            affected_card.types.add("Enchantment")

        # Mycosynth Lattice (all permanents are artifacts)
        if affected_card.is_permanent:
            affected_card.types.add("Artifact")

        # March of the Machines (all noncreature artifacts are creatures)
        if "Artifact" in affected_card.types and "Creature" not in affected_card.types:
            affected_card.types.add("Creature")

        # Maskwood Nexus (creature gets all creature types)
        if "Creature" in affected_card.types:
            affected_card.subtypes |= affected_card.all_creature_types

        # Life and Limb (All Forests and all Saprolings are 1/1 green Saproling creatures
        # and Forest lands in addition to their other types)
        if "Forest" in affected_card.subtypes or "Saproling" in affected_card.subtypes:
            affected_card.types |= {"Creature", "Land"}
            affected_card.subtypes |= {"Saproling", "Forest"}

        # Prismatic Omen (lands are every basic land type)
        if "Land" in affected_card.types:
            affected_card.subtypes |= affected_card.basic_land_types

        # In Bolas's Clutches (permanent becomes legendary)
        if affected_card.is_permanent:
            affected_card.supertypes.add("Legendary")

        # Rimefeather Owl (permanents with ice counters are snow)
        if affected_card.is_permanent:
            affected_card.supertypes.add("Snow")

        # Arterial Alchemy (Blood tokens are Equipment)
        if affected_card.is_token and "Blood" in affected_card.subtypes:
            affected_card.subtypes.add("Equipment")
            affected_card.text = " ".join(
                [affected_card.text, "Equipped creature gets +2/+0."]
            )
            affected_card.keywords.append("Equip {2}")

        affected_card.clear_cached_properties()

    return returned_cards
