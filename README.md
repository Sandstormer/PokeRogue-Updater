<a href="https://sandstormer.github.io/PokeRogue-Dex/">
  <img src="https://github.com/Sandstormer/PokeRogue-Dex/raw/main/ui/bigbutton.png">
</a>

### ❌ This is <b>NOT</b> the repository for [Sandstorm's PokeRogue SearchDex](https://sandstormer.github.io/PokeRogue-Dex/).

### 🔧 This repository is for the update scripts that assemble the data for that site. 
These scripts read all the necessary data from the [game code](https://github.com/pagefaultgames/pokerogue/tree/main), process all the images, and put all the data into a compact format for my site. I run these scripts whenever there is a game update. There is no need for anyone else to run these, unless I am unable to continue the project.

# How to use

1. Install Python.
2. Download or clone this repository.
3. Run these scripts in order, from an IDE. There are more instructions in each file.

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
