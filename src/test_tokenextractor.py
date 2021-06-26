import pytest

from magicobjects import MagicToken

test_cases = [
    (
        "Master of the Wild Hunt Avatar",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Wolf"],
                power="2",
                toughness="2",
            ),
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Antelope"],
                power="2",
                toughness="3",
                keywords=["forestwalk"],
            ),
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Cat"],
                power="3",
                toughness="2",
                keywords=["shroud"],
            ),
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Rhino"],
                power="4",
                toughness="4",
                keywords=["trample"],
            ),
        ],
    ),
    (
        "Verix Bladewing",
        [
            MagicToken(
                name="Karox Bladewing",
                colors=["R"],
                supertypes=["Legendary"],
                types=["Creature"],
                subtypes=["Dragon"],
                power="4",
                toughness="4",
                keywords=["flying"],
            )
        ],
    ),
    (
        "Tuktuk the Explorer",
        [
            MagicToken(
                name="Tuktuk the Returned",
                supertypes=["Legendary"],
                types=["Artifact", "Creature"],
                subtypes=["Goblin", "Golem"],
                power="5",
                toughness="5",
            )
        ],
    ),
    (
        "Tomb of Urami",
        [
            MagicToken(
                name="Urami",
                colors=["B"],
                supertypes=["Legendary"],
                types=["Creature"],
                subtypes=["Demon", "Spirit"],
                power="5",
                toughness="5",
                keywords=["flying"],
            )
        ],
    ),
    (
        "Tolsimir Wolfblood",
        [
            MagicToken(
                name="Voja",
                colors=["W", "G"],
                supertypes=["Legendary"],
                types=["Creature"],
                subtypes=["Wolf"],
                power="2",
                toughness="2",
            )
        ],
    ),
    (
        "Kari Zev, Skyship Raider",
        [
            MagicToken(
                name="Ragavan",
                colors=["R"],
                supertypes=["Legendary"],
                types=["Creature"],
                subtypes=["Monkey"],
                power="2",
                toughness="1",
            )
        ],
    ),
    (
        "Helm of Kaldra",
        [
            MagicToken(
                name="Kaldra",
                supertypes=["Legendary"],
                types=["Creature"],
                subtypes=["Avatar"],
                power="4",
                toughness="4",
            )
        ],
    ),
    (
        "Jiang Yanggu",
        [
            MagicToken(
                name="Mowu",
                colors=["G"],
                supertypes=["Legendary"],
                types=["Creature"],
                subtypes=["Dog"],
                power="3",
                toughness="3",
            )
        ],
    ),
    (
        "Brood Birthing",
        [
            MagicToken(
                types=["Creature"],
                subtypes=["Eldrazi", "Spawn"],
                power="0",
                toughness="1",
                text="Sacrifice this creature: Add {C}.",
            )
        ],
    ),
    ("Rage Extractor", []),
    (
        "Planewide Celebration",
        [
            MagicToken(
                colors=["W", "U", "B", "R", "G"],
                types=["Creature"],
                subtypes=["Citizen"],
                power="2",
                toughness="2",
            )
        ],
    ),
    (
        "Silverwing Squadron",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Knight"],
                power="2",
                toughness="2",
                keywords=["vigilance"],
            )
        ],
    ),
    (
        "Militant Angel",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Knight"],
                power="2",
                toughness="2",
                keywords=["vigilance"],
            )
        ],
    ),
    (
        "Nissa, Sage Animist",
        [
            MagicToken(
                name="Ashaya, the Awoken World",
                colors=["G"],
                supertypes=["Legendary"],
                types=["Creature"],
                subtypes=["Elemental"],
                power="4",
                toughness="4",
            )
        ],
    ),
    (
        "From Under the Floorboards",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Zombie"],
                power="2",
                toughness="2",
            )
        ],
    ),
    (
        "Akim, the Soaring Wind",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Bird"],
                power="1",
                toughness="1",
                keywords=["flying"],
            ),
        ],
    ),
    (
        "Throne of Empires",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Soldier"],
                power="1",
                toughness="1",
            ),
        ],
    ),
    (
        "Old-Growth Troll",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Troll", "Warrior"],
                power="4",
                toughness="4",
                keywords=["trample"],
            )
        ],
    ),
    ("Arcbound Wanderer", []),
    (
        "Tolsimir, Friend to Wolves",
        [
            MagicToken(
                name="Voja, Friend to Elves",
                colors=["W", "G"],
                supertypes=["Legendary"],
                types=["Creature"],
                subtypes=["Wolf"],
                power="3",
                toughness="3",
            )
        ],
    ),
    (
        "Basri Ket",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Soldier"],
                power="1",
                toughness="1",
            ),
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Soldier"],
                power="1",
                toughness="1",
            ),
        ],
    ),
    (
        "Sporoloth Ancient",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Saproling"],
                power="1",
                toughness="1",
            )
        ],
    ),
    (
        "Toggo, Goblin Weaponsmith",
        [
            MagicToken(
                types=["Artifact"],
                subtypes=["Equipment"],
                name="Rock",
                text="Equipped creature has '{1}, {T}, Sacrifice Rock: This creature deals 2 damage to any target'",
                keywords=["equip {1}"],
            )
        ],
    ),
    (
        "Outlaws' Merriment",
        [
            MagicToken(
                colors=["R", "W"],
                types=["Creature"],
                subtypes=["Human", "Warrior"],
                power="3",
                toughness="1",
                keywords=["trample", "haste"],
            ),
            MagicToken(
                colors=["R", "W"],
                types=["Creature"],
                subtypes=["Human", "Cleric"],
                power="2",
                toughness="1",
                keywords=["lifelink", "haste"],
            ),
            MagicToken(
                colors=["R", "W"],
                types=["Creature"],
                subtypes=["Human", "Rogue"],
                power="1",
                toughness="2",
                keywords=["haste"],
                text="When this creature enters the battlefield, it deals 1 damage to any target.",
            ),
        ],
    ),
    # (
    #     "Outlaws' Merriment",
    #     [
    #         MagicToken(
    #             colors=["W", "R"],
    #             types=["Creature"],
    #         )
    #     ],
    # ),
    (
        "Rise from the Tides",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Zombie"],
                power="2",
                toughness="2",
            )
        ],
    ),
    ("Esix, Fractal Bloom", []),
    (
        "Urza's Saga",
        [
            MagicToken(
                types=["Artifact", "Creature"],
                subtypes=["Construct"],
                power="0",
                toughness="0",
                text="This creature gets +1/+1 for each artifact you control.",
            )
        ],
    ),
    (
        "Blot Out the Sky",
        [
            MagicToken(
                colors=["W", "B"],
                types=["Creature"],
                subtypes=["Inkling"],
                power="2",
                toughness="1",
                keywords=["flying"],
            )
        ],
    ),
    (
        "Pest Infestation",
        [
            MagicToken(
                colors=["B", "G"],
                types=["Creature"],
                subtypes=["Pest"],
                power="1",
                toughness="1",
                text="When this creature dies, you gain 1 life.",
            )
        ],
    ),
    (
        "Invocation of Saint Traft",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Angel"],
                power="4",
                toughness="4",
                keywords=["flying"],
            )
        ],
    ),
    (
        "Assemble the Rank and Vile",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Zombie"],
                power="2",
                toughness="2",
            )
        ],
    ),
    ("Koth of the Hammer", []),
    ("Gadrak, the Crown-Scourge", [MagicToken.Treasure]),
    (
        "Voice of Resurgence",
        [
            MagicToken(
                colors=["W", "G"],
                types=["Creature"],
                subtypes=["Elemental"],
                text="This creature's power and toughness are each equal to the number of creatures you control.",
            )
        ],
    ),
    (
        "Evangel of Heliod",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Soldier"],
                power="1",
                toughness="1",
            )
        ],
    ),
    (
        "Soul Separator",
        [MagicToken(colors=["B"], types=["Creature"], subtypes=["Zombie"])],
    ),
    (
        "Nested Shambler",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Squirrel"],
                power="1",
                toughness="1",
            )
        ],
    ),
    ("Tireless Provisioner", [MagicToken.Food, MagicToken.Treasure]),
    ("Merfolk of the Pearl Trident", []),
    ("Akrasan Squire", []),
    (
        "Abhorrent Overlord",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Harpy"],
                power="1",
                toughness="1",
                keywords=["flying"],
            )
        ],
    ),
    (
        "Abstruse Interference",
        [
            MagicToken(
                types=["Creature"],
                subtypes=["Eldrazi", "Scion"],
                power="1",
                toughness="1",
                text="Sacrifice this creature: Add {C}.",
            )
        ],
    ),
    (
        "Abzan Ascendancy",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Spirit"],
                power="1",
                toughness="1",
                keywords=["flying"],
            )
        ],
    ),
    ("Academy Manufactor", []),
    (
        "Acorn Catapult",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Squirrel"],
                power="1",
                toughness="1",
            )
        ],
    ),
    (
        "Acorn Harvest",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Squirrel"],
                power="1",
                toughness="1",
            )
        ],
    ),
    (
        "Advent of the Wurm",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Wurm"],
                power="5",
                toughness="5",
                keywords=["trample"],
            )
        ],
    ),
    (
        "Adverse Conditions",
        [
            MagicToken(
                colors={},
                types=["Creature"],
                subtypes=["Eldrazi", "Scion"],
                power="1",
                toughness="1",
                text="Sacrifice this creature: Add {C}.",
            )
        ],
    ),
    (
        "Aerie Worshippers",
        [
            MagicToken(
                colors=["U"],
                types=["Enchantment", "Creature"],
                subtypes=["Bird"],
                power="2",
                toughness="2",
                keywords=["flying"],
            )
        ],
    ),
    (
        "Aether Chaser",
        [
            MagicToken(
                colors=[],
                types=["Artifact", "Creature"],
                subtypes=["Servo"],
                power="1",
                toughness="1",
            )
        ],
    ),
    (
        "Aether Mutation",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Saproling"],
                power="1",
                toughness="1",
            )
        ],
    ),
    (
        "Ajani, Adversary of Tyrants",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Cat"],
                power="1",
                toughness="1",
                keywords=["lifelink"],
            )
        ],
    ),
    (
        "Ajani, Caller of the Pride",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Cat"],
                power="2",
                toughness="2",
            )
        ],
    ),
    (
        "Ajani Goldmane",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Avatar"],
                text="This creature's power and toughness are each equal to your life total.",
            )
        ],
    ),
    (
        "Stangg",
        [
            MagicToken(
                name="Stangg Twin",
                colors=["R", "G"],
                supertypes=["Legendary"],
                types=["Creature"],
                subtypes=["Human", "Warrior"],
                power="3",
                toughness="4",
            )
        ],
    ),
    (
        "Estrid, the Masked",
        [
            MagicToken(
                name="Mask",
                colors=["W"],
                types=["Enchantment"],
                subtypes=["Aura"],
                keywords=["enchant permanent", "totem armor"],
            )
        ],
    ),
    (
        "Valduk, Keeper of the Flame",
        [
            MagicToken(
                colors=["R"],
                types=["Creature"],
                subtypes=["Elemental"],
                power="3",
                toughness="1",
                keywords=["trample", "haste"],
            )
        ],
    ),
    (
        "Kemba, Kha Regent",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Cat"],
                power="2",
                toughness="2",
            )
        ],
    ),
    (
        "Hazezon Tamar",
        [
            MagicToken(
                colors=["R", "G", "W"],
                types=["Creature"],
                subtypes=["Sand", "Warrior"],
                power="1",
                toughness="1",
            )
        ],
    ),
    (
        "Dark Depths",
        [
            MagicToken(
                name="Marit Lage",
                colors=["B"],
                supertypes=["Legendary"],
                types=["Creature"],
                subtypes=["Avatar"],
                power="20",
                toughness="20",
                keywords=["flying", "indestructible"],
            )
        ],
    ),
    (
        "Drizzt Do'Urden",
        [
            MagicToken(
                name="Guenhwyvar",
                colors=["G"],
                supertypes=["Legendary"],
                types=["Creature"],
                subtypes=["Cat"],
                power="4",
                toughness="1",
                keywords=["trample"],
            )
        ],
    ),
    ("Aeve, Progenitor Ooze", []),
    (
        "Awaken the Blood Avatar",
        [
            MagicToken(
                colors=["B", "R"],
                types=["Creature"],
                subtypes=["Avatar"],
                power="3",
                toughness="6",
                keywords=["haste"],
                text="Whenever this creature attacks, it deals 3 damage to each opponent.",
            )
        ],
    ),
    (
        "Boris Devilboon",
        [
            MagicToken(
                name="Minor Demon",
                colors=["B", "R"],
                types=["Creature"],
                subtypes=["Demon"],
                power="1",
                toughness="1",
            )
        ],
    ),
    (
        "Ajani, Strength of the Pride",
        [
            MagicToken(
                name="Ajani's Pridemate",
                colors=["W"],
                types=["Creature"],
                subtypes=["Cat", "Soldier"],
                power="2",
                toughness="2",
                text="Whenever you gain life, put a +1/+1 counter on Ajani's Pridemate.",
            )
        ],
    ),
    (
        "Cloudseeder",
        [
            MagicToken(
                name="Cloud Sprite",
                colors=["U"],
                types=["Creature"],
                subtypes=["Faerie"],
                power="1",
                toughness="1",
                keywords=["flying"],
                text="Cloud Sprite can block only creatures with flying.",
            )
        ],
    ),
    (
        "Decree of Justice",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Angel"],
                power="4",
                toughness="4",
                keywords=["flying"],
            ),
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Soldier"],
                power="1",
                toughness="1",
            ),
        ],
    ),
    (
        "Reef Worm",
        [
            MagicToken(
                colors=["U"],
                types=["Creature"],
                subtypes=["Fish"],
                power="3",
                toughness="3",
                text="When this creature dies, create a 6/6 blue Whale creature token with 'When this creature dies, create a 9/9 blue Kraken creature token.'",
            ),
            MagicToken(
                colors=["U"],
                types=["Creature"],
                subtypes=["Whale"],
                power="6",
                toughness="6",
                text="When this creature dies, create a 9/9 blue Kraken creature token.",
            ),
            MagicToken(
                colors=["U"],
                types=["Creature"],
                subtypes=["Kraken"],
                power="9",
                toughness="9",
            ),
        ],
    ),
    (
        "Anax, Hardened in the Forge",
        [
            MagicToken(
                colors=["R"],
                types=["Creature"],
                subtypes=["Satyr"],
                power="1",
                toughness="1",
                text="This creature can't block.",
            )
        ],
    ),
    (
        "Court of Grace",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Spirit"],
                power="1",
                toughness="1",
                keywords=["flying"],
            ),
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Angel"],
                power="4",
                toughness="4",
                keywords=["flying"],
            ),
        ],
    ),
    ("Doubling Season", []),
    ("Bake into a Pie", [MagicToken.Food]),
    (
        "Fae Offering",
        [
            MagicToken.Clue,
            MagicToken.Food,
            MagicToken.Treasure,
        ],
    ),
    ("Gluttonous Troll", [MagicToken.Food]),
    (
        "Army of the Damned",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Zombie"],
                power="2",
                toughness="2",
            )
        ],
    ),
    ("Nacatl War-Pride", []),
    (
        "Everquill Phoenix",
        [
            MagicToken(
                name="Feather",
                colors=["R"],
                types=["Artifact"],
                text="{1}, Sacrifice Feather: Return target Phoenix card from your graveyard to the battlefield tapped.",
            )
        ],
    ),
    (
        "Gemini Engine",
        [
            MagicToken(
                name="Twin", types=["Artifact", "Creature"], subtypes=["Construct"]
            )
        ],
    ),
    (
        "Goblin Kaboomist",
        [
            MagicToken(
                name="Land Mine",
                types=["Artifact"],
                text="{R}, Sacrifice this artifact: This artifact deals 2 damage to target attacking creature without flying.",
            )
        ],
    ),
    (
        "Goldmeadow Lookout",
        [
            MagicToken(
                name="Goldmeadow Harrier",
                colors=["W"],
                types=["Creature"],
                subtypes=["Kithkin", "Soldier"],
                power="1",
                toughness="1",
                text="{W}, {T}: Tap target creature.",
            )
        ],
    ),
    (
        "Jungle Patrol",
        [
            MagicToken(
                name="Wood",
                colors=["G"],
                types=["Creature"],
                subtypes=["Wall"],
                keywords=["defender"],
                power="0",
                toughness="1",
            )
        ],
    ),
    (
        "Kher Keep",
        [
            MagicToken(
                name="Kobolds of Kher Keep",
                colors=["R"],
                types=["Creature"],
                subtypes=["Kobold"],
                power="0",
                toughness="1",
            )
        ],
    ),
    (
        "Koma, Cosmos Serpent",
        [
            MagicToken(
                name="Koma's Coil",
                colors=["U"],
                types=["Creature"],
                subtypes=["Serpent"],
                power="3",
                toughness="3",
            )
        ],
    ),
    (
        "Llanowar Mentor",
        [
            MagicToken(
                name="Llanowar Elves",
                colors=["G"],
                types=["Creature"],
                subtypes=["Elf", "Druid"],
                power="1",
                toughness="1",
                text="{T}: Add {G}.",
            )
        ],
    ),
    (
        "Replicating Ring",
        [
            MagicToken(
                name="Replicated Ring",
                supertypes=["Snow"],
                types=["Artifact"],
                text="{T}: Add one mana of any color.",
            )
        ],
    ),
    (
        "Marit Lage's Slumber",
        [
            MagicToken(
                name="Marit Lage",
                colors=["B"],
                supertypes=["Legendary"],
                types=["Creature"],
                subtypes=["Avatar"],
                power="20",
                toughness="20",
                keywords=["flying", "indestructible"],
            )
        ],
    ),
    (
        "Svella, Ice Shaper",
        [
            MagicToken(
                name="Icy Manalith",
                supertypes=["Snow"],
                types=["Artifact"],
                text="{T}: Add one mana of any color.",
            )
        ],
    ),
    (
        "Master of the Hunt",
        [
            MagicToken(
                name="Wolves of the Hunt",
                colors=["G"],
                types=["Creature"],
                subtypes=["Wolf"],
                power="1",
                toughness="1",
                text="Bands with other creatures named Wolves of the Hunt.",
            )
        ],
    ),
    (
        "Nahiri, the Lithomancer",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Kor", "Soldier"],
                power="1",
                toughness="1",
            ),
            MagicToken(
                name="Stoneforged Blade",
                types=["Artifact"],
                subtypes=["Equipment"],
                keywords=["indestructible", "equip {0}"],
                text="Equipped creature gets +5/+5 and has double strike.",
            ),
        ],
    ),
    (
        "Prossh, Skyraider of Kher",
        [
            MagicToken(
                name="Kobolds of Kher Keep",
                colors=["R"],
                types=["Creature"],
                subtypes=["Kobold"],
                power="0",
                toughness="1",
            )
        ],
    ),
    (
        "Domri, Chaos Bringer",
        [
            MagicToken(
                colors=["R", "G"],
                types=["Creature"],
                subtypes=["Beast"],
                power="4",
                toughness="4",
                keywords=["trample"],
            )
        ],
    ),
    (
        "Godsire",
        [
            MagicToken(
                colors=["W", "R", "G"],
                types=["Creature"],
                subtypes=["Beast"],
                power="8",
                toughness="8",
            )
        ],
    ),
    (
        "Sarpadian Empires, Vol. VII",
        [
            MagicToken(
                types=["Creature"],
                power="1",
                toughness="1",
                colors=["W"],
                subtypes=["Citizen"],
            ),
            MagicToken(
                types=["Creature"],
                power="1",
                toughness="1",
                colors=["U"],
                subtypes=["Camarid"],
            ),
            MagicToken(
                types=["Creature"],
                power="1",
                toughness="1",
                colors=["B"],
                subtypes=["Thrull"],
            ),
            MagicToken(
                types=["Creature"],
                power="1",
                toughness="1",
                colors=["R"],
                subtypes=["Goblin"],
            ),
            MagicToken(
                types=["Creature"],
                power="1",
                toughness="1",
                colors=["G"],
                subtypes=["Saproling"],
            ),
        ],
    ),
    # (
    #     "Sarpadian Empires, Vol. VII",
    #     [MagicToken(types=["Creature"], power="1", toughness="1")],
    # ),
    (
        "Wasitora, Nekoru Queen",
        [
            MagicToken(
                colors=["B", "R", "G"],
                types=["Creature"],
                subtypes=["Cat", "Dragon"],
                power="3",
                toughness="3",
                keywords=["flying"],
            )
        ],
    ),
    ("Niko Aris", [MagicToken.Shard, MagicToken.Shard]),
    ("Michonne, Ruthless Survivor", [MagicToken.Walker]),
    ("Farmstead", []),
    ("Dandân", []),
    (
        "Rukh Egg",
        [
            MagicToken(
                colors=["R"],
                types=["Creature"],
                subtypes=["Bird"],
                power="4",
                toughness="4",
                keywords=["flying"],
            )
        ],
    ),
    (
        "Tetravus",
        [
            MagicToken(
                types=["Artifact", "Creature"],
                subtypes=["Tetravite"],
                power="1",
                toughness="1",
                keywords=["flying"],
                text="This creature can't be enchanted.",
            )
        ],
    ),
    ("Dance of Many", []),
    (
        "Phantasmal Sphere",
        [
            MagicToken(
                colors=["U"],
                types=["Creature"],
                subtypes=["Orb"],
                power="X",
                toughness="X",
                keywords=["flying"],
            )
        ],
    ),
    (
        "Giant Caterpillar",
        [
            MagicToken(
                name="Butterfly",
                colors=["G"],
                types=["Creature"],
                subtypes=["Insect"],
                power="1",
                toughness="1",
                keywords=["flying"],
            )
        ],
    ),
    ("Dual Nature", []),
    (
        "Elephant Resurgence",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Elephant"],
                text="This creature's power and toughness are each equal to the number of creature cards in its controller's graveyard.",
            )
        ],
    ),
    ("Parallel Evolution", []),
    (
        "Grizzly Fate",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Bear"],
                power="2",
                toughness="2",
            ),
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Bear"],
                power="2",
                toughness="2",
            ),
        ],
    ),
    ("Chandra Nalaar", []),
    ("Academy at Tolaria West", []),
    ("Nemesis Trap", []),
    (
        "Kazuul, Tyrant of the Cliffs",
        [
            MagicToken(
                colors=["R"],
                types=["Creature"],
                subtypes=["Ogre"],
                power="3",
                toughness="3",
            )
        ],
    ),
    (
        "Nature Shields Its Own",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Plant"],
                power="0",
                toughness="1",
            )
        ],
    ),
    (
        "Rotted Ones, Lay Siege",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Zombie"],
                power="2",
                toughness="2",
            )
        ],
    ),
    (
        "Lolth, Spider Queen",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Spider"],
                power="2",
                toughness="1",
                keywords=["menace", "reach"],
            )
        ],
    ),
    (
        "Hofri Ghostforge",
        [
            # MagicToken(
            #     subtypes=["Spirit"],
            #     text="When this creature leaves the battlefield, return the exiled card to its owner's graveyard.",
            # )
        ],
    ),
    ("Kaboom!", []),
    ("Riptide Replicator", [MagicToken(types=["Creature"], power="X", toughness="X")]),
    (
        "Hunted Horror",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Centaur"],
                power="3",
                toughness="3",
                keywords=["protection from black"],
            )
        ],
    ),
    (
        "Hunted Dragon",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Knight"],
                power="2",
                toughness="2",
                keywords=["first strike"],
            )
        ],
    ),
    (
        "Flash Foliage",
        [
            MagicToken(
                colors=["G"],
                types=["Creature"],
                subtypes=["Saproling"],
                power="1",
                toughness="1",
            )
        ],
    ),
    (
        "Omen of the Sun",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Human", "Soldier"],
                power="1",
                toughness="1",
            )
        ],
    ),
    ("Infiltrator il-Kor", []),
    (
        "Phyrexian Processor",
        [
            MagicToken(
                colors=["B"],
                types=["Creature"],
                subtypes=["Phyrexian", "Minion"],
                power="X",
                toughness="X",
            )
        ],
    ),
    (
        "Retreat to Emeria",
        [
            MagicToken(
                colors=["W"],
                types=["Creature"],
                subtypes=["Kor", "Ally"],
                power="1",
                toughness="1",
            )
        ],
    ),
    ("Ragavan, Nimble Pilferer", [MagicToken.Treasure]),
    ("Caravan Escort", []),
]


@pytest.mark.parametrize("name,expected", test_cases)
def test_tokens(mtgjsondata, extractor, name, expected):
    card = mtgjsondata.get_card_by_name(name)
    print(card.text)
    tokens = extractor.extract_from_card(card)
    assert tokens == expected
