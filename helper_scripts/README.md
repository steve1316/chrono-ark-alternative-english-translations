# Chrono Ark Mod Translation Helper Scripts

This repository contains a collection of Python scripts designed to help automate my workflow for translating mods for the game Chrono Ark.Below is a brief overview of each script:

## Scripts

### `move.py`

This script is responsible for copying mod files to Chrono Ark's `/Mod` folder and placing a copy in the `/Alternative_English_Translations/Localization` folder by its Steam Workshop ID.

### `merge.py`

This script merges the mod's initial translation file with the primary translation file exported from within Chrono Ark, to be placed in the mod's Localization folder manually.

### `strip.py`

This script strips the text from the program that I use to send requests to the DeepSeek R1 API which adds extra whitespaces for some reason to its responses.
