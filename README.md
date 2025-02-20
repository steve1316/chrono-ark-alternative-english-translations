# Chrono Ark Alternative English Translations

In order to push updates to Steam, the mod version needs to be bumped up in `ChronoArkMod.json` and the upload needs to be initiated from within Chrono Ark itself.

Each folder under `Localization` is named after the mod's unique Steam Workshop ID and follows a `STEAM_WORKSHOP_ID/Localization/*.csv` file structure. Mod logo images are provided for a slightly better sense of which folder belongs to which mod.

Two sets of helper scripts are provided: `set_translation` and `unset_translation` both as Python scripts and Windows scripts.

### set_translation
- For each localization folder inside `Localization`, this script makes a backup of the original csv files and then overwrites them with the translated copies. If the backup folder already exists, then it restores the backups before starting the translation deployment process.

### unset_translation
- For each localization folder inside the `Localization_backup` that was created from `set_translation`, it restores the original files.