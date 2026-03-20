"""
WORLDHATCH — Complete Creature Roster
══════════════════════════════════════════════════════════════
100 Creatures across 10 Regions
Every region has 10 creatures spanning ALL element types.
Each region's creatures are geographically flavored but
elementally diverse — so players must trade globally to
collect every element type they want.

RARITY SPREAD PER REGION:
  4 Common     (C)
  3 Uncommon   (U)
  2 Rare       (R)
  1 Legendary  (L)

ELEMENTS:
  fire, ice, nature, spirit, dark, storm,
  water, sand, magma, crystal

REGIONS:
  1.  suncrest_expanse      — US West Coast
  2.  sakurami_highlands    — Japan
  3.  verdeluna_jungle      — Brazil / Amazon
  4.  frostspire_reach      — Norway / Scandinavia
  5.  ashenveil_steppe      — Central Asia
  6.  coralhaven_shoals     — Pacific / Southeast Asia
  7.  dunecrown_expanse     — Sahara / Middle East
  8.  emberveil_depths      — Volcanic / Iceland
  9.  shadowmere_hollows    — Eastern Europe / Carpathians
  10. crystalpeak_range     — Himalayas / Tibet
"""

FULL_ROSTER = {

    # ══════════════════════════════════════════════════════
    #  REGION 1 — SUNCREST EXPANSE (US West Coast)
    #  Flavor: canyon lands, redwood forests, coastal cliffs,
    #          desert heat, ocean fog
    # ══════════════════════════════════════════════════════
    "suncrest_expanse": {
        "display_name":   "Suncrest Expanse",
        "real_world_ref": "United States West Coast",
        "dominant_element": "fire",
        "creatures": [
            # COMMON
            {"id": "emberback_rumbler",   "name": "Emberback Rumbler",   "element": "fire",    "rarity": "common",    "description": "Stocky lizard with glowing ember spines on its back. Roams sun-scorched canyon ridgelines."},
            {"id": "dustfin_drifter",     "name": "Dustfin Drifter",     "element": "fire",    "rarity": "common",    "description": "Slender glider that rides canyon thermals. Fins shimmer like heated glass."},
            {"id": "tidewatcher",         "name": "Tidewatcher",         "element": "water",   "rarity": "common",    "description": "Round seal-like creature that watches coastal tide pools with enormous patient eyes."},
            {"id": "fogcrawler",          "name": "Fogcrawler",          "element": "spirit",  "rarity": "common",    "description": "A pale crab-like creature that emerges only in coastal fog. Translucent shell."},
            # UNCOMMON
            {"id": "cinderclaw",          "name": "Cinderclaw",          "element": "fire",    "rarity": "uncommon",  "description": "Fast predator with superheated claws. Leaves scorch marks on everything it touches."},
            {"id": "stormhawk",           "name": "Stormhawk",           "element": "storm",   "rarity": "uncommon",  "description": "A broad-winged hawk that generates static charge in its feathers during coastal winds."},
            {"id": "redshard_gecko",      "name": "Redshard Gecko",      "element": "crystal", "rarity": "uncommon",  "description": "Tiny gecko with ruby-red crystal growths along its spine. Clings to canyon walls."},
            # RARE
            {"id": "sunshell_crawler",    "name": "Sunshell Crawler",    "element": "fire",    "rarity": "rare",      "description": "Encased in a brilliant golden shell that absorbs sunlight. Nearly impossible to crack."},
            {"id": "darkwood_stalker",    "name": "Darkwood Stalker",    "element": "dark",    "rarity": "rare",      "description": "A black panther-like creature that hunts in the shadows of ancient redwood forests."},
            # LEGENDARY
            {"id": "solarcrown_wyrm",     "name": "Solarcrown Wyrm",     "element": "magma",   "rarity": "legendary", "description": "An enormous serpent whose scales are molten rock. Said to have formed from a volcanic rift in the California coast millions of years ago."},
        ]
    },

    # ══════════════════════════════════════════════════════
    #  REGION 2 — SAKURAMI HIGHLANDS (Japan)
    #  Flavor: mountain shrines, cherry blossom forests,
    #          bamboo groves, deep ocean trenches, neon cities
    # ══════════════════════════════════════════════════════
    "sakurami_highlands": {
        "display_name":   "Sakurami Highlands",
        "real_world_ref": "Japan",
        "dominant_element": "spirit",
        "creatures": [
            # COMMON
            {"id": "misthare",            "name": "Misthare",            "element": "spirit",  "rarity": "common",    "description": "Nimble spirit-rabbit that phases briefly through solid objects."},
            {"id": "blossomwing",         "name": "Blossomwing",         "element": "spirit",  "rarity": "common",    "description": "Winged creature with petals woven into its feathers. Migrates with cherry blossom season."},
            {"id": "bambooshell_tortoise","name": "Bambooshell Tortoise","element": "nature",  "rarity": "common",    "description": "A calm tortoise with a shell made of interlocked bamboo segments. Very patient."},
            {"id": "tidepulse_jellyfish", "name": "Tidepulse Jellyfish", "element": "water",   "rarity": "common",    "description": "A bioluminescent jellyfish found in deep ocean trenches. Pulses with soft blue light."},
            # UNCOMMON
            {"id": "inkfox",              "name": "Inkfox",              "element": "dark",    "rarity": "uncommon",  "description": "Fox whose fur shifts between deep black and shimmering silver. Leaves vanishing ink footprints."},
            {"id": "stonepetal_wyrm",     "name": "Stonepetal Wyrm",     "element": "crystal", "rarity": "uncommon",  "description": "Long serpent with stone-hard scales etched with floral patterns. Guards mountain shrines."},
            {"id": "thunderkoi",          "name": "Thunderkoi",          "element": "storm",   "rarity": "uncommon",  "description": "A large koi fish that generates electrical charges when it leaps from water."},
            # RARE
            {"id": "ashveil_crane",       "name": "Ashveil Crane",       "element": "fire",    "rarity": "rare",      "description": "An elegant crane with feathers tipped in pale ash. Dances in volcanic updrafts near Mount Fuji."},
            {"id": "frostpetal_oni",      "name": "Frostpetal Oni",      "element": "ice",     "rarity": "rare",      "description": "A small fierce oni creature with ice-blue skin and cherry blossom patterns frozen into its horns."},
            # LEGENDARY
            {"id": "ryujin_serpent",      "name": "Ryujin Serpent",      "element": "spirit",  "rarity": "legendary", "description": "A colossal sea dragon said to rule the tides of Sakurami. Its scales hold the memory of every storm for a thousand years."},
        ]
    },

    # ══════════════════════════════════════════════════════
    #  REGION 3 — VERDELUNA JUNGLE (Brazil / Amazon)
    #  Flavor: dense canopy, river systems, bioluminescent
    #          fungi, flooded forests, hidden ruins
    # ══════════════════════════════════════════════════════
    "verdeluna_jungle": {
        "display_name":   "Verdeluna Jungle",
        "real_world_ref": "Brazil / Amazon Basin",
        "dominant_element": "nature",
        "creatures": [
            # COMMON
            {"id": "thornback_brute",     "name": "Thornback Brute",     "element": "nature",  "rarity": "common",    "description": "Massive armored creature covered in venomous thorns. Tank of the jungle floor."},
            {"id": "mosswhisper",         "name": "Mosswhisper",         "element": "nature",  "rarity": "common",    "description": "Entirely covered in living moss. Nearly invisible on the jungle floor."},
            {"id": "rivercoil_serpent",   "name": "Rivercoil Serpent",   "element": "water",   "rarity": "common",    "description": "Long water snake that coils around submerged logs. Scales shimmer like river reflections."},
            {"id": "canopy_glider",       "name": "Canopy Glider",       "element": "storm",   "rarity": "common",    "description": "A sugar-glider-like creature that generates static charge when it leaps between trees."},
            # UNCOMMON
            {"id": "venomcap_toad",       "name": "Venomcap Toad",       "element": "nature",  "rarity": "uncommon",  "description": "Bloated toad with toxic mushroom caps growing from its back. Releases paralytic spores."},
            {"id": "ruinglow_beetle",     "name": "Ruinglow Beetle",     "element": "crystal", "rarity": "uncommon",  "description": "Enormous beetle with a shell that refracts light into crystal patterns. Found near ancient ruins."},
            {"id": "ashvine_creeper",     "name": "Ashvine Creeper",     "element": "dark",    "rarity": "uncommon",  "description": "A vine-covered serpent that moves through shadow. Its vines slowly drain energy from prey."},
            # RARE
            {"id": "luminleaf_sprite",    "name": "Luminleaf Sprite",    "element": "nature",  "rarity": "rare",      "description": "Bioluminescent creature with leaf-like wings. Appears only when the jungle is in perfect balance."},
            {"id": "magmagrub",           "name": "Magmagrub",           "element": "magma",   "rarity": "rare",      "description": "A larval creature that feeds on volcanic minerals carried by Amazonian rivers. Glows deep orange."},
            # LEGENDARY
            {"id": "verdant_colossus",    "name": "Verdant Colossus",    "element": "nature",  "rarity": "legendary", "description": "An ancient behemoth so large the jungle has grown into its back. Trees sprout from its shoulders. It has not moved in three centuries."},
        ]
    },

    # ══════════════════════════════════════════════════════
    #  REGION 4 — FROSTSPIRE REACH (Norway / Scandinavia)
    #  Flavor: fjords, permafrost, aurora borealis,
    #          deep mountain caves, arctic tundra
    # ══════════════════════════════════════════════════════
    "frostspire_reach": {
        "display_name":   "Frostspire Reach",
        "real_world_ref": "Norway / Scandinavia",
        "dominant_element": "ice",
        "creatures": [
            # COMMON
            {"id": "glacierfang",         "name": "Glacierfang",         "element": "ice",     "rarity": "common",    "description": "Fierce predator with crystalline fangs formed from permafrost."},
            {"id": "rimewolve",           "name": "Rimewolve",           "element": "ice",     "rarity": "common",    "description": "Pack hunter with frost-laced fur. Hunts in coordinated groups and shares body heat."},
            {"id": "aurorawing",          "name": "Aurorawing",          "element": "spirit",  "rarity": "common",    "description": "A moth-like creature whose wings display aurora borealis patterns when it flies at night."},
            {"id": "fjordpup",            "name": "Fjordpup",            "element": "water",   "rarity": "common",    "description": "A playful otter-like creature that surfs fjord currents. Incredibly curious and friendly."},
            # UNCOMMON
            {"id": "coldcrest_raptor",    "name": "Coldcrest Raptor",    "element": "ice",     "rarity": "uncommon",  "description": "Swift aerial hunter with ice-crystal feathers sharp enough to shear rock."},
            {"id": "stormtusk_boar",      "name": "Stormtusk Boar",      "element": "storm",   "rarity": "uncommon",  "description": "A boar with tusks that crackle with lightning. Charges through blizzards without slowing."},
            {"id": "cavern_darkbear",     "name": "Cavern Darkbear",     "element": "dark",    "rarity": "uncommon",  "description": "A bear that lives deep in mountain caves. Eyes glow faintly. Rarely seen above ground."},
            # RARE
            {"id": "avalanche_golem",     "name": "Avalanche Golem",     "element": "ice",     "rarity": "rare",      "description": "Ancient construct of compacted glacier ice and mountain stone. Dormant for centuries until disturbed."},
            {"id": "runefire_elk",        "name": "Runefire Elk",        "element": "fire",    "rarity": "rare",      "description": "A massive elk with antlers that glow with ancient runic fire. Worshipped in old Frostspire mythology."},
            # LEGENDARY
            {"id": "jormunveil",          "name": "Jormunveil",          "element": "ice",     "rarity": "legendary", "description": "A serpent of impossible length that sleeps coiled beneath the deepest fjord. Its breath is the source of all blizzards in the Reach."},
        ]
    },

    # ══════════════════════════════════════════════════════
    #  REGION 5 — ASHENVEIL STEPPE (Central Asia)
    #  Flavor: vast grasslands, dust storms, ancient trade
    #          routes, underground cave cities, meteor craters
    # ══════════════════════════════════════════════════════
    "ashenveil_steppe": {
        "display_name":   "Ashenveil Steppe",
        "real_world_ref": "Central Asia / Kazakh Steppe",
        "dominant_element": "storm",
        "creatures": [
            # COMMON
            {"id": "dustmane_runner",     "name": "Dustmane Runner",     "element": "storm",   "rarity": "common",    "description": "A horse-like creature with a mane made of compressed dust. Outruns every storm on the steppe."},
            {"id": "ashprowl_cat",        "name": "Ashprowl Cat",        "element": "storm",   "rarity": "common",    "description": "A lean steppe cat coated in grey-brown ash-fur. Silent and impossibly fast."},
            {"id": "cragback_tortoise",   "name": "Cragback Tortoise",   "element": "sand",    "rarity": "common",    "description": "A tortoise with a shell made of compressed steppe earth and rock. Extremely durable."},
            {"id": "embervole",           "name": "Embervole",           "element": "fire",    "rarity": "common",    "description": "A small burrowing rodent that keeps warm through internal heat generation. Cozy and round."},
            # UNCOMMON
            {"id": "thunderhoof_bison",   "name": "Thunderhoof Bison",   "element": "storm",   "rarity": "uncommon",  "description": "A massive bison that creates rolling thunder with every hoofstrike. Herd stampedes shake the earth."},
            {"id": "crater_lurker",       "name": "Crater Lurker",       "element": "crystal", "rarity": "uncommon",  "description": "A spider-like creature that nests in meteor impact craters. Its body contains embedded meteorite crystals."},
            {"id": "voidstep_wolf",       "name": "Voidstep Wolf",       "element": "dark",    "rarity": "uncommon",  "description": "A wolf that leaves no tracks. Seems to step between shadows rather than run through them."},
            # RARE
            {"id": "sandwhirl_djinn",     "name": "Sandwhirl Djinn",     "element": "sand",    "rarity": "rare",      "description": "A being of pure animated sandstorm. Ancient trade routes say meeting one brings either great fortune or great misery."},
            {"id": "icevein_stallion",    "name": "Icevein Stallion",    "element": "ice",     "rarity": "rare",      "description": "A wild horse with ice-blue veins visible through its white coat. Runs across frozen rivers without cracking the ice."},
            # LEGENDARY
            {"id": "stormfather_eagle",   "name": "Stormfather Eagle",   "element": "storm",   "rarity": "legendary", "description": "An eagle of terrifying wingspan. A single beat of its wings triggers a three-day storm across the entire steppe. Nomads consider it a god."},
        ]
    },

    # ══════════════════════════════════════════════════════
    #  REGION 6 — CORALHAVEN SHOALS (Pacific / Southeast Asia)
    #  Flavor: coral reefs, tropical islands, monsoon coasts,
    #          volcanic island chains, deep sea trenches
    # ══════════════════════════════════════════════════════
    "coralhaven_shoals": {
        "display_name":   "Coralhaven Shoals",
        "real_world_ref": "Pacific Islands / Southeast Asia",
        "dominant_element": "water",
        "creatures": [
            # COMMON
            {"id": "coralback_crab",      "name": "Coralback Crab",      "element": "water",   "rarity": "common",    "description": "A crab whose shell has actual living coral growing from it. Slow but unyielding."},
            {"id": "shimmerscale_fish",   "name": "Shimmerscale Fish",   "element": "water",   "rarity": "common",    "description": "A tropical fish with iridescent scales that blind attackers. Schools of thousands move as one."},
            {"id": "mangrove_toad",       "name": "Mangrove Toad",       "element": "nature",  "rarity": "common",    "description": "A fat, content toad that sits in mangrove roots. Its belly secretes a calming herbal scent."},
            {"id": "riftglow_eel",        "name": "Riftglow Eel",        "element": "magma",   "rarity": "common",    "description": "An eel that lives near underwater volcanic vents. Warm to the touch. Glows faintly orange."},
            # UNCOMMON
            {"id": "stormcaller_manta",   "name": "Stormcaller Manta",   "element": "storm",   "rarity": "uncommon",  "description": "A giant manta ray that leaps from the water during storms and flies through lightning clouds."},
            {"id": "phantom_seahorse",    "name": "Phantom Seahorse",    "element": "spirit",  "rarity": "uncommon",  "description": "A translucent seahorse that can become completely invisible in still water."},
            {"id": "abyssal_hunter",      "name": "Abyssal Hunter",      "element": "dark",    "rarity": "uncommon",  "description": "A deep-sea predator with no eyes and bioluminescent lures. Rises to shallow water only at night."},
            # RARE
            {"id": "tidalcrystal_turtle", "name": "Tidalcrystal Turtle", "element": "crystal", "rarity": "rare",      "description": "An ancient sea turtle with a shell made of sea-crystal that took two centuries to form."},
            {"id": "typhoon_serpent",     "name": "Typhoon Serpent",     "element": "water",   "rarity": "rare",      "description": "A sea serpent that creates whirlpools and waterspouts as it moves. Sailors both fear and revere it."},
            # LEGENDARY
            {"id": "leviathan_bloom",     "name": "Leviathan Bloom",     "element": "water",   "rarity": "legendary", "description": "A creature so vast it is mistaken for an island. Coral reefs have grown on its back over millennia. When it dives, entire coastlines flood."},
        ]
    },

    # ══════════════════════════════════════════════════════
    #  REGION 7 — DUNECROWN EXPANSE (Sahara / Middle East)
    #  Flavor: vast sand seas, oases, ancient buried cities,
    #          night sky deserts, sandstone canyons
    # ══════════════════════════════════════════════════════
    "dunecrown_expanse": {
        "display_name":   "Dunecrown Expanse",
        "real_world_ref": "Sahara / Middle East",
        "dominant_element": "sand",
        "creatures": [
            # COMMON
            {"id": "dune_skitter",        "name": "Dune Skitter",        "element": "sand",    "rarity": "common",    "description": "A tiny lizard that runs across sand at astonishing speed. Barely leaves tracks."},
            {"id": "heatpulse_scorpion",  "name": "Heatpulse Scorpion", "element": "fire",    "rarity": "common",    "description": "A scorpion with a tail that radiates intense heat. Prey is cooked before the sting lands."},
            {"id": "oasis_spirit",        "name": "Oasis Spirit",        "element": "water",   "rarity": "common",    "description": "A gentle deer-like creature that always knows where the nearest water source is."},
            {"id": "stargazer_moth",      "name": "Stargazer Moth",      "element": "spirit",  "rarity": "common",    "description": "A moth that navigates by starlight. Its wings display accurate star maps of the desert night sky."},
            # UNCOMMON
            {"id": "sandvault_beetle",    "name": "Sandvault Beetle",    "element": "sand",    "rarity": "uncommon",  "description": "A beetle with a shell so dense it can survive being buried under ten meters of sand for years."},
            {"id": "miragecat",           "name": "Miragecat",           "element": "spirit",  "rarity": "uncommon",  "description": "A cat that creates heat mirage illusions of itself. Hunters always aim at the wrong one."},
            {"id": "thunderdust_hawk",    "name": "Thunderdust Hawk",    "element": "storm",   "rarity": "uncommon",  "description": "A hawk that dives through sandstorms for prey. Static charge in its feathers turns sand to glass on impact."},
            # RARE
            {"id": "buried_colossus",     "name": "Buried Colossus",     "element": "sand",    "rarity": "rare",      "description": "A golem made of ancient compressed sandstone. Rises from buried cities when disturbed. Covered in hieroglyphic carvings."},
            {"id": "nightcrystal_viper",  "name": "Nightcrystal Viper",  "element": "crystal", "rarity": "rare",      "description": "A viper whose scales are made of desert crystal that only forms under extreme night cold. Invisible during the day."},
            # LEGENDARY
            {"id": "dunecrown_sphinx",    "name": "Dunecrown Sphinx",    "element": "sand",    "rarity": "legendary", "description": "The original creature. Half great cat, half stormbird. Speaks in riddles. Said to be older than the desert itself and to have watched every civilization rise and fall."},
        ]
    },

    # ══════════════════════════════════════════════════════
    #  REGION 8 — EMBERVEIL DEPTHS (Volcanic / Iceland)
    #  Flavor: active volcanoes, lava tubes, geothermal
    #          vents, obsidian fields, underground magma lakes
    # ══════════════════════════════════════════════════════
    "emberveil_depths": {
        "display_name":   "Emberveil Depths",
        "real_world_ref": "Iceland / Volcanic Regions",
        "dominant_element": "magma",
        "creatures": [
            # COMMON
            {"id": "lavapup",             "name": "Lavapup",             "element": "magma",   "rarity": "common",    "description": "A roly-poly puppy-like creature made of cooling lava. Warm and affectionate. Loves to be pet despite the heat."},
            {"id": "obsidian_crab",       "name": "Obsidian Crab",       "element": "magma",   "rarity": "common",    "description": "A crab with a shell of pure obsidian. Pinches hard enough to cut through rock."},
            {"id": "steamvent_frog",      "name": "Steamvent Frog",      "element": "fire",    "rarity": "common",    "description": "A frog that lives around geothermal vents. Exhales jets of scalding steam when scared."},
            {"id": "ashdrift_bird",       "name": "Ashdrift Bird",       "element": "storm",   "rarity": "common",    "description": "A small grey bird that rides volcanic ash clouds. Nests inside dormant craters."},
            # UNCOMMON
            {"id": "magmahorn_ram",       "name": "Magmahorn Ram",       "element": "magma",   "rarity": "uncommon",  "description": "A ram with horns of solid magma rock. Head-butts create small eruptions."},
            {"id": "voidflame_salamander","name": "Voidflame Salamander","element": "dark",    "rarity": "uncommon",  "description": "A salamander that absorbs both heat and light. Its body is a void of pure darkness that radiates cold fire."},
            {"id": "crystalite_mole",     "name": "Crystalite Mole",     "element": "crystal", "rarity": "uncommon",  "description": "A blind mole that navigates entirely by sensing crystal formations underground. Its claws mine crystal effortlessly."},
            # RARE
            {"id": "cinder_wyvern",       "name": "Cinder Wyvern",       "element": "fire",    "rarity": "rare",      "description": "A two-legged dragon coated in glowing cinders. Breathes a rolling wave of superheated ash."},
            {"id": "glacial_intruder",    "name": "Glacial Intruder",    "element": "ice",     "rarity": "rare",      "description": "An ice creature that has somehow adapted to volcanic heat. Its body is a paradox of ice and steam. Extremely rare."},
            # LEGENDARY
            {"id": "magma_titan",         "name": "Magma Titan",         "element": "magma",   "rarity": "legendary", "description": "A walking volcano. Its footsteps open fissures in the earth. Has been erupting continuously for 400 years. Classified as both creature and natural disaster."},
        ]
    },

    # ══════════════════════════════════════════════════════
    #  REGION 9 — SHADOWMERE HOLLOWS (Eastern Europe)
    #  Flavor: dark forests, ancient castles, misty marshes,
    #          underground cavern networks, moonlit plains
    # ══════════════════════════════════════════════════════
    "shadowmere_hollows": {
        "display_name":   "Shadowmere Hollows",
        "real_world_ref": "Eastern Europe / Carpathian Mountains",
        "dominant_element": "dark",
        "creatures": [
            # COMMON
            {"id": "marsh_lurker",        "name": "Marsh Lurker",        "element": "dark",    "rarity": "common",    "description": "A frog-like creature that sits perfectly still in dark marsh water for days at a time."},
            {"id": "mirecat",             "name": "Mirecat",             "element": "dark",    "rarity": "common",    "description": "A thin feral cat covered in marsh mud. Moves silently through reed beds."},
            {"id": "hollowbat",           "name": "Hollowbat",           "element": "dark",    "rarity": "common",    "description": "An unusually large bat with hollow bones that make it nearly silent in flight."},
            {"id": "moonveil_moth",       "name": "Moonveil Moth",       "element": "spirit",  "rarity": "common",    "description": "A pale moth that only flies in full moonlight. Its wings dissolve shadows around it."},
            # UNCOMMON
            {"id": "bog_golem",           "name": "Bog Golem",           "element": "nature",  "rarity": "uncommon",  "description": "A slow-moving golem made of peat and ancient marsh vegetation. Preserves everything it touches."},
            {"id": "stormcrow",           "name": "Stormcrow",           "element": "storm",   "rarity": "uncommon",  "description": "A crow that can predict storms three days in advance. Flocks of stormcrows are an omen."},
            {"id": "frostshade_wolf",     "name": "Frostshade Wolf",     "element": "ice",     "rarity": "uncommon",  "description": "A wolf with fur so pale it vanishes in winter fog. Its howl lowers the temperature around it."},
            # RARE
            {"id": "castle_wraith",       "name": "Castle Wraith",       "element": "dark",    "rarity": "rare",      "description": "A semi-corporeal creature that inhabits abandoned castle walls. Can pass through stone."},
            {"id": "bloodcrystal_bat",    "name": "Bloodcrystal Bat",    "element": "crystal", "rarity": "rare",      "description": "A massive bat with crystal growths on its wings that catch moonlight. Creates blinding flashes."},
            # LEGENDARY
            {"id": "void_sovereign",      "name": "Void Sovereign",      "element": "dark",    "rarity": "legendary", "description": "An entity of pure concentrated shadow. Exists in the space between things. Players who encounter it report that nearby light sources permanently dim. Cannot be photographed."},
        ]
    },

    # ══════════════════════════════════════════════════════
    #  REGION 10 — CRYSTALPEAK RANGE (Himalayas / Tibet)
    #  Flavor: world's highest peaks, ancient monasteries,
    #          crystal cave networks, thin air, star fields,
    #          hidden valleys
    # ══════════════════════════════════════════════════════
    "crystalpeak_range": {
        "display_name":   "Crystalpeak Range",
        "real_world_ref": "Himalayas / Tibet",
        "dominant_element": "crystal",
        "creatures": [
            # COMMON
            {"id": "peakpuff",            "name": "Peakpuff",            "element": "ice",     "rarity": "common",    "description": "A fluffy round creature that lives at extreme altitude. Its thick fur is insulated enough to sit on glaciers comfortably."},
            {"id": "crystalwing_dove",    "name": "Crystalwing Dove",    "element": "crystal", "rarity": "common",    "description": "A dove with small crystal growths on its wingtips. Releases musical tones when it flies."},
            {"id": "cliff_ibex",          "name": "Cliff Ibex",          "element": "crystal", "rarity": "common",    "description": "A mountain goat with crystalline horns. Navigates impossible cliff faces with perfect calm."},
            {"id": "starbreath_yak",      "name": "Starbreath Yak",      "element": "spirit",  "rarity": "common",    "description": "A large calm yak whose breath freezes into tiny star-shaped crystals in the cold mountain air."},
            # UNCOMMON
            {"id": "voidpeak_eagle",      "name": "Voidpeak Eagle",      "element": "dark",    "rarity": "uncommon",  "description": "An eagle that hunts above the cloud line. Its shadow is darker than any natural shadow. Monks consider it a guide to the underworld."},
            {"id": "thundermonk_ape",     "name": "Thundermonk Ape",     "element": "storm",   "rarity": "uncommon",  "description": "A meditative ape that generates static charge through focused stillness. Can release it in a single devastating blast."},
            {"id": "emberpillar",         "name": "Emberpillar",         "element": "fire",    "rarity": "uncommon",  "description": "A caterpillar that generates internal heat to survive the mountain cold. Wrapped in a cocoon of frozen flame."},
            # RARE
            {"id": "monastery_guardian",  "name": "Monastery Guardian",  "element": "crystal", "rarity": "rare",      "description": "A lion-like creature made entirely of translucent crystal. Has stood at the gates of a hidden mountain monastery for 800 years."},
            {"id": "water_ascendant",     "name": "Water Ascendant",     "element": "water",   "rarity": "rare",      "description": "A creature that exists partially in our world and partially in a higher plane. Its body is liquid water held in a vaguely creature-shaped form."},
            # LEGENDARY
            {"id": "peak_sovereign",      "name": "Peak Sovereign",      "element": "crystal", "rarity": "legendary", "description": "The highest creature in the world. Lives above 8000 meters where no other living thing survives. Its body is a living mountain of crystal. Looking directly at it causes temporary blindness from the refracted light."},
        ]
    },
}


# ══════════════════════════════════════════════════════════
#  ROSTER SUMMARY HELPER
# ══════════════════════════════════════════════════════════

def print_roster_summary():
    total = 0
    print("\n" + "="*60)
    print("  WORLDHATCH CREATURE ROSTER — FULL SUMMARY")
    print("="*60)
    for region_id, region in FULL_ROSTER.items():
        creatures = region["creatures"]
        total += len(creatures)
        by_rarity = {}
        by_element = {}
        for c in creatures:
            by_rarity[c["rarity"]] = by_rarity.get(c["rarity"], 0) + 1
            by_element[c["element"]] = by_element.get(c["element"], 0) + 1
        print(f"\n  {region['display_name']} ({region['real_world_ref']})")
        print(f"  Dominant: {region['dominant_element'].upper()} | Total: {len(creatures)}")
        print(f"  Rarities: {by_rarity}")
        print(f"  Elements: {by_element}")
    print(f"\n  TOTAL CREATURES: {total}")
    print("="*60)


def get_all_creature_ids():
    ids = []
    for region in FULL_ROSTER.values():
        for c in region["creatures"]:
            ids.append(c["id"])
    return ids


def get_creatures_by_element(element: str):
    result = []
    for region_id, region in FULL_ROSTER.items():
        for c in region["creatures"]:
            if c["element"] == element:
                result.append({**c, "region": region_id})
    return result


def get_creatures_by_rarity(rarity: str):
    result = []
    for region_id, region in FULL_ROSTER.items():
        for c in region["creatures"]:
            if c["rarity"] == rarity:
                result.append({**c, "region": region_id})
    return result


if __name__ == "__main__":
    print_roster_summary()
    print(f"\n  All IDs sample: {get_all_creature_ids()[:5]}...")
    print(f"\n  All DARK creatures:")
    for c in get_creatures_by_element("dark"):
        print(f"    [{c['region']}] {c['name']} ({c['rarity']})")
    print(f"\n  All LEGENDARY creatures:")
    for c in get_creatures_by_rarity("legendary"):
        print(f"    [{c['region']}] {c['name']} — {c['element'].upper()}")
