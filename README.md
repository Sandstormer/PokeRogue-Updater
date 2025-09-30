<a href="https://sandstormer.github.io/PokeRogue-Dex/">
  <img src="https://github.com/Sandstormer/PokeRogue-Dex/raw/main/ui/bigbutton.png">
</a>

### ❌ This is <b>NOT</b> the repository for [Sandstorm's PokeRogue SearchDex](https://sandstormer.github.io/PokeRogue-Dex/).

### 🔧 This repository is for the update scripts that assemble the data for that site. 
These scripts read all the necessary data from the [game code](https://github.com/pagefaultgames/pokerogue/tree/main), process all the images, and put all the data into a compact format for my site. I run these scripts whenever there is a game update. There is no need for anyone else to run these, unless I am unable to continue the project.

# How to use

## Folder structure

    root/
    ├── game_files/
    │   ├── live/
    │   ├── beta/
    │   └── locales/
    ├── local_files/
    │   ├── my_json/
    │   └── lang_overrides/
    └── website/

**game_files** is populated by updateGameFiles.py. It clones the official game data for 3 folders: live (the current version of the game), beta (the beta version of the game), locales (translations for the game)

**local_files** contains proc_data.json and trimmed_data.json, which are the current versions of move/ability and pokemon data, respectively. There are also previous versions ("prev"), which are used to identify changes to the data in updateMoves.py and updateDatabase.py. trimmed_data_prev_shvar.json is a further back version of the data to detect which shiny variants are "new".

**my_json** contains other json files that are created by my scripts, so that my other scripts can access the data.

**lang_overrides** contains all the UI elements for each language, which are manually translated. Other translations, such as pokemon/moves/ability names and descriptions, are automatically taken from the game with updateLangs.py.

**website** contains the website files for the [Searchdex itself](https://github.com/Sandstormer/PokeRogue-Dex). Those files are modified by the scripts in this repository.

## Structure of pokedex_data.js

The data contains the full data on every Pokemon, and the structure allows for fast lookups of information.
The pokemon must be in the same order as speciesNames in the lang file. This is also the default sort option.
The entries for each pokemon can be in any order.

    dex:    Pokedex number
    
    img:    File name of the image
            Gets the actual image as "ui/{img}_0.png" for tier 0 (non-shiny)
    
    t1, t2, a1, a2, ha, pa: Types, Abilities, Hidden Ability, Passive
            Contains the Filter ID (FID) that corresponds to the type/ability described
            An entry is omitted if it does not apply to the pokemon
    
    bst, hp, atk, def, spa, spd, spe: Stats
    
    e1, e2, e3, e4: Egg moves
            Contains the Filter ID (FID) of the corresponding move
    
    co: Base cost of the pokemon
    
    et: Egg tier
            0 = common, 1 = rare, 2 = epic, 3 = manaphy, 4 = legendary
    
    sh: Number of shiny variants the Pokemon has
            Either 1 (no variants), or 3 (all variants)
    
    ge: Which generation the pokemon is in

    All the remaining entries are omitted if not applicable to the pokemon
    
    fe: If the Pokemon has a female form
            Value is 1 if they have traditional sprite differences, like Venusaur
            Value is 2 if they have named female forms, like Meowstic
    
    fa: Which family the pokemon is in
            This is used for the "Related To" filters
            Contains the FID that corresponds to that family filter
    
    st: Value is 1 if the Pokemon is available from starter select (i.e. being the lowest evolution)
    
    fs: Value is 1 if the Pokemon is available in fresh start (i.e. being a first partner pokemon)
    
    nv: Value is 1 if the Pokemon had new variants recently added
    
    fx: If the Pokemon is form exclusive
            Value is 1 for Mega, G-Max, item form changes, or temporary form changes
    
    ex: If the Pokemon is egg exclusive
            Value is 1 for traditional egg exclusives, like Arceus
            Value is 2 for baby Pokemon, like Pichu
            Value is 3 for paradox egg exclusives, like Scream Tail
            Value is 4 only for Eternatus
            Value is 5 only for Starmobile Revavroom
    
    numerical entries: These are like FID:value
            FID is the Filter ID that can be a type, ability, move, biome
            value is how that pokemon relates to that FID (this is different depending on the FID)
            Do not include entries that don't apply to that pokemon
            For Moves: (i.e. 876:204, 328:1, 1125:209, or anything like that)
                    fidThreshold[1] <= FID < fidThreshold[2]
                    value shows how the pokemon learns the move
                            -1:mushroom, 0:evo, 1-200:level, 
                            201:egg&commonTM, 202:egg&greatTM, 203:egg&ultraTM, 204:egg,
                            205:rareEgg&commonTM, 206:rareEgg&greatTM, 205:rareEgg&ultraTM, 208:rareEgg,
                            209:commonTM, 210:greatTM, 211: ultraTM
            For Types: (i.e. 9:307)
                    fidThreshold[0] <= FID < fidThreshold[1]
                    value shows which slot the pokemon has that type (307 = type1, 308 = type2)
                    This data is technically redundant but allows for faster lookups
            For Abilities: (i.e. 18:309)
                    fidThreshold[1] <= FID < fidThreshold[2]
                    value shows which slot the pokemon has that ability (309 = ab1, 310 = ab2, 311 = ha, 312 = pa)
                    This data is technically redundant but allows for faster lookups
            For Biomes: (i.e. 1197:[80,100])
                    fidThreshold[8] <= FID < fidThreshold[9]
                    value is an array describing the encounter types in that biome
                            Each of those entries encodes the encounter rarity and time of day
                            Each rarity is a number:
                                    20 = COMMON,  40 = UNCOMMON,  60 = BOSS,  80 = RARE,  100 = BOSS_RARE,
                                    120 = SUPER_RARE,  140 = BOSS_SUPER_RARE,  160 = ULTRA_RARE,  180 = BOSS_ULTRA_RARE
                            If a pokemon is only available at a certain time of day, it has a modifier added to that number
                                    +1 for dawn, +2 for day, +4 for dusk, +8 for night
                                    Modifiers are added together if the Pokemon is available during more than one time of day
                            If there is more than one entry for encounter types that are always put in a predictable order
                                    The first entry is the most common nonboss encounter
                                    The second entry is the most common boss encounter
                                    Entries beyond the second can be in any order
                                    If a pokemon is only Boss encounters, the first entry is the lowest number
                    For example, Amoonguss has 1201:[32,72,83,103]
                            This means it is in the Jungle (FID = 1201)
                            The rarities are Common (Dusk, Night), Boss Common (Dusk, Night), Rare (Dawn, Day), Boss Rare (Dawn, Day)
