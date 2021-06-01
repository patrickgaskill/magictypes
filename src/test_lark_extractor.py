import pytest
from magic_objects.token import MagicToken


test_cases = [
    ("Merfolk of the Pearl Trident", []),
    ("Akrasan Squire", []),
    ("Abhorrent Overlord", [MagicToken(colors=["B"], types=[
     "Creature"], subtypes=["Harpy"], power="1", toughness="1", keywords=["flying"])]),
    ("Abstruse Interference",  [MagicToken(colors=[], types=["Creature"], subtypes=[
     "Eldrazi", "Scion"], power="1", toughness="1", text="Sacrifice this creature: Add {C}.")]),
    ("Abzan Ascendancy",  [MagicToken(colors=["W"], types=[
     "Creature"], subtypes=["Spirit"], power="1", toughness="1", keywords=["flying"])]),
    ("Academy Manufactor", []),
    ("Acorn Catapult", [MagicToken(colors=["G"], types=[
     "Creature"], subtypes=["Squirrel"], power="1", toughness="1")]),
    ("Acorn Harvest", [MagicToken(colors=["G"], types=[
     "Creature"], subtypes=["Squirrel"], power="1", toughness="1")]),
    ("Advent of the Wurm", [MagicToken(colors=["G"], types=[
     "Creature"], subtypes=["Wurm"], power="5", toughness="5", keywords=["trample"])]),
    ("Adverse Conditions",  [MagicToken(colors=[], types=[
     "Creature"], subtypes=["Eldrazi", "Scion"], power="1", toughness="1", text="Sacrifice this creature: Add {C}.")]),
    ("Aerie Worshippers",  [MagicToken(colors=["U"], types=[
     "Enchantment", "Creature"], subtypes=["Bird"], power="2", toughness="2", keywords=["flying"])]),
    ("Aether Chaser", [MagicToken(colors=[], types=[
     "Artifact", "Creature"], subtypes=["Servo"], power="1", toughness="1")]),
    ("Aether Mutation", [MagicToken(colors=["G"], types=[
     "Creature"], subtypes=["Saproling"], power="1", toughness="1")]),
    ("Ajani, Adversary of Tyrants", [MagicToken(colors=["W"], types=[
     "Creature"], subtypes=["Cat"], power="1", toughness="1", keywords=["lifelink"])]),
    ("Ajani, Caller of the Pride", [MagicToken(colors=["W"], types=[
     "Creature"], subtypes=["Cat"], power="2", toughness="2")]),
    ("Ajani Goldmane", [MagicToken(colors=["W"],
     types=["Creature"], subtypes=["Avatar"], text="This creature's power and toughness are each equal to your life total.")]),
    ("Stangg", [MagicToken(name="Stangg Twin", colors=["R", "G"], supertypes=["Legendary"],
     types=["Creature"], subtypes=["Human", "Warrior"], power="3", toughness="4")]),
    ("Estrid, the Masked", [MagicToken(name="Mask", colors=[
     "W"], types=["Enchantment"], subtypes=["Aura"])]),
    ("Valduk, Keeper of the Flame", [
     MagicToken(colors=["R"], types=["Creature"], subtypes=["Elemental"], power="3", toughness="1", keywords=["trample", "haste"])]),
    ("Kemba, Kha Regent", [
     MagicToken(colors=["W"], types=["Creature"], subtypes=["Cat"], power="2", toughness="2")]),
    ("Hazezon Tamar", [MagicToken(colors=["R", "G", "W"],
     types=["Creature"], subtypes=["Sand", "Warrior"], power="1", toughness="1")]),
    ("Dark Depths", [MagicToken(name="Marit Lage", colors=["B"], supertypes=["Legendary"], types=[
     "Creature"], subtypes=["Avatar"], power="20", toughness="20", keywords=["flying", "indestructible"])]),
    ("Drizzt Do'Urden", [MagicToken(name="Guenhwyvar", colors=["G"], supertypes=["Legendary"], types=[
     "Creature"], subtypes=["Cat"], power="4", toughness="1", keywords=["trample"])]),
    ("Aeve, Progenitor Ooze", []),
    ("Extus, Oriq Overlord // Awaken the Blood Avatar", [MagicToken(colors=["B", "R"], types=[
     "Creature"], subtypes=["Avatar"], power="3", toughness="6", keywords=["haste"], text="Whenever this creature attacks, it deals 3 damage to each opponent.")]),
    ("Boris Devilboon", [MagicToken(name="Minor Demon", colors=[
     "B", "R"], types=["Creature"], subtypes=["Demon"], power="1", toughness="1")]),
    ("Ajani, Strength of the Pride", [MagicToken(name="Ajani's Pridemate", colors=["W"], types=["Creature"], subtypes=[
     "Cat", "Soldier"], power="2", toughness="2", text="Whenever you gain life, put a +1/+1 counter on Ajani's Pridemate.")]),
    ("Cloudseeder", [MagicToken(name="Cloud Sprite", colors=["U"], types=[
     "Creature"], subtypes=["Faerie"], power="1", toughness="1", keywords=["flying"], text="Cloud Sprite can block only creatures with flying.")])
]


@ pytest.mark.parametrize("name,expected", test_cases)
def test_tokens(get_card, extractor, name, expected):
    card = get_card(name)
    print(getattr(card, "text", "(No card text)"))
    tokens = extractor.extract_from_card(card)
    assert tokens == expected
