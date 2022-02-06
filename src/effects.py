from magicobjects import MagicObject


def apply_effects(target_obj: MagicObject) -> list[MagicObject]:
    returned_objs = [target_obj.copy()]

    # Moritte of the Frost is a copy so doesn't see the following type-changing effects
    if target_obj.is_permanent:
        moritte_copy = target_obj.copy()
        moritte_copy.supertypes |= {"Legendary", "Snow"}
        if "Creature" in moritte_copy.types:
            # moritte_copy.subtypes |= card.all_creature_types
            moritte_copy.keywords.add("Changeling")
        returned_objs.append(moritte_copy)

    # Dermotaxi (copy creature from GY and add Vehicle artifact)
    if not target_obj.is_token and "Creature" in target_obj.types:
        dermotaxi_copy = target_obj.copy()
        dermotaxi_copy.types.add("Artifact")
        dermotaxi_copy.subtypes.add("Vehicle")
        returned_objs.append(dermotaxi_copy)

    # Replication Technique (copy permanent as token)
    if target_obj.is_permanent:
        # replication_technique_copy = card.copy_as_token()
        # returned_cards.append(replication_technique_copy)
        if target_obj.object_type == "card":
            returned_objs.append(target_obj.copy_as_token())

        if target_obj.object_type == "token":
            returned_objs.append(target_obj.copy())

    for affected_obj in returned_objs:
        # Enchanted Evening (all permanents are enchantments)
        if affected_obj.is_permanent:
            affected_obj.types.add("Enchantment")

        # Mycosynth Lattice (all permanents are artifacts)
        if affected_obj.is_permanent:
            affected_obj.types.add("Artifact")

        # March of the Machines (all noncreature artifacts are creatures)
        if "Artifact" in affected_obj.types and "Creature" not in affected_obj.types:
            affected_obj.types.add("Creature")

        # Maskwood Nexus (creature gets all creature types)
        if "Creature" in affected_obj.types:
            affected_obj.subtypes |= affected_obj.all_creature_types

        # Life and Limb (All Forests and all Saprolings are 1/1 green Saproling creatures
        # and Forest lands in addition to their other types)
        if "Forest" in affected_obj.subtypes or "Saproling" in affected_obj.subtypes:
            affected_obj.types |= {"Creature", "Land"}
            affected_obj.subtypes |= {"Saproling", "Forest"}

        # Prismatic Omen (lands are every basic land type)
        if "Land" in affected_obj.types:
            affected_obj.subtypes |= affected_obj.basic_land_types

        # In Bolas's Clutches (permanent becomes legendary)
        if affected_obj.is_permanent:
            affected_obj.supertypes.add("Legendary")

        # Rimefeather Owl (permanents with ice counters are snow)
        if affected_obj.is_permanent:
            affected_obj.supertypes.add("Snow")

        # Arterial Alchemy (Blood tokens are Equipment)
        if affected_obj.is_token and "Blood" in affected_obj.subtypes:
            affected_obj.subtypes.add("Equipment")
            affected_obj.text = " ".join(
                [affected_obj.text, "Equipped creature gets +2/+0."]
            )
            affected_obj.keywords.add("Equip {2}")

        affected_obj.clear_cached_properties()

    return returned_objs
