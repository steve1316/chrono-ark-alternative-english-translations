import os
import sys
import csv
import logging


BASE_PATH = r"D:\Steam\steamapps\workshop\content\1188930"

def detect_language(text: str):
    """
    Detects the language of the given text.

    Args:
        text (str): The text to detect the language of.

    Returns:
        str: The language of the text.
    """
    # Japanese Hiragana and Katakana.
    if any("\u3040" <= char <= "\u30ff" for char in text):  
        return "japanese"
    # Chinese characters.
    elif any("\u4e00" <= char <= "\u9fff" for char in text):  
        return "chinese"
    # Korean Hangul.
    elif any("\uac00" <= char <= "\ud7af" for char in text):  
        return "korean"
    # English.
    elif any(char.isalpha() for char in text):
        return "english"
    return "other"

def check_for_update(mod_id: str, language_to_compare: str):
    """
    Checks for updates in the mod's CSV files.

    Args:
        mod_id (str): The Steam Workshop ID of the mod to check. Can be left blank to check all mods.
        language_to_compare (str): The language to compare the mod's CSV to.
    """
    if mod_id:
        mod_ids_to_check = [mod_id]
    else:
        localization_path = os.path.join(BASE_PATH, "3427597117", "Localization")
        mod_ids_to_check = [f for f in os.listdir(localization_path) if f.isdigit()]
    
    differences = []
    for mod_id in mod_ids_to_check:
        mod_path = os.path.join(BASE_PATH, mod_id, "Localization")
        # alt_translations_path = os.path.join(BASE_PATH, "3427597117", "Localization", mod_id, "Localization")
        alt_translations_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Localization", mod_id, "Localization") # This is for testing purposes.
        
        # If the backup folder exists, raise an error saying that you need to restore the original files first.
        if os.path.exists(os.path.join(BASE_PATH, "3427597117", "Localization_backup")):
            raise FileExistsError(f"There is an existing backup folder. Please restore the original files first.")
        if not os.path.exists(mod_path):
            logging.warning(f"Mod ID {mod_id} for the original files does not exist at {mod_path}")
            continue
        if not os.path.exists(alt_translations_path):
            logging.warning(f"Mod ID {mod_id} for the alternative translations does not exist at {alt_translations_path}")
            continue

        # Load the alt translation CSV file(s) paths.
        alt_translation_csv_files = [os.path.join(alt_translations_path, f) for f in os.listdir(alt_translations_path) if f.endswith(".csv")]

        # Do the same with the mod's original CSV file(s) paths.
        mod_csv_files = [os.path.join(mod_path, f) for f in os.listdir(mod_path) if f.endswith(".csv")]
        
        # Create dictionary of filename:path for mod files.
        mod_files = {os.path.basename(f): f for f in mod_csv_files}
        
        # We need to open each file pair and compare each row to see if the mod's CSV is different than the alt translation's CSV in terms of their
        # column values at "Korean", "Japanese", and "Chinese" depending on the language_to_compare argument.

        for alt_file in alt_translation_csv_files:
            filename = os.path.basename(alt_file)
            mod_file = mod_files.get(filename)
            if not mod_file:
                raise FileNotFoundError(f"Corresponding mod file {filename} not found in {mod_path}")
            
            with open(alt_file, "r", encoding="utf-8") as alt_f, open(mod_file, "r", encoding="utf-8") as mod_f:
                alt_reader = csv.DictReader(alt_f)
                mod_reader = csv.DictReader(mod_f)
                lang_columns = ["Korean", "Japanese", "Chinese"]
                language_to_compare_index = lang_columns.index(language_to_compare.capitalize())
                
                # Create a dictionary of the rows of both files by their Key column value.
                alt_key_field = "\ufeffKey" if "\ufeffKey" in alt_reader.fieldnames else "Key"
                mod_key_field = "\ufeffKey" if "\ufeffKey" in mod_reader.fieldnames else "Key"
                alt_rows_by_key = {row[alt_key_field]: row for row in alt_reader}
                mod_rows_by_key = {row[mod_key_field]: row for row in mod_reader}
                
                for mod_key, mod_row in mod_rows_by_key.items():
                    # Ignore keys that are malformed.
                    # Check if the following are at the beginning of the key and if not, skip.
                    if not mod_key.startswith((
                        "Buff/", 
                        "Character/", 
                        "Item_Consume/", 
                        "Item_Equip/", 
                        "Item_Passive/",
                        "Skill/", 
                        "SkillExtended/", 
                        "SkillKeyword/", 
                        "SimpleCampDialogue/", 
                        "System/", 
                        "Dialogue/")) or "_" not in mod_key:
                        continue
                    
                    alt_row = alt_rows_by_key.get(mod_key)
                    if alt_row and alt_row[lang_columns[language_to_compare_index]] != mod_row[lang_columns[language_to_compare_index]]:
                        if mod_row[lang_columns[language_to_compare_index]] == None and alt_row[lang_columns[language_to_compare_index]] == "":
                            continue
                        
                        # Skip if the row value's language is different from the compared alt row value's language.
                        mod_value_lang = detect_language(mod_row[lang_columns[language_to_compare_index]])
                        alt_value_lang = detect_language(alt_row[lang_columns[language_to_compare_index]])
                        if mod_value_lang != alt_value_lang:
                            continue
                        
                        logging.info(f"String difference found in {filename} for {mod_key}.")
                        differences.append({
                            "mod_id": mod_id,
                            "file": filename,
                            "row": mod_row[lang_columns[language_to_compare_index]],
                            "key": mod_row.get(mod_key_field),
                            "mod_value": mod_row[lang_columns[language_to_compare_index]],
                            "alt_value": alt_row[lang_columns[language_to_compare_index]]
                        })
                    elif not alt_row:
                        logging.info(f"New string found in {filename} for {mod_key}.")
                        differences.append({
                            "mod_id": mod_id,
                            "file": filename,
                            "row": mod_row[lang_columns[language_to_compare_index]],
                            "key": mod_row.get(mod_key_field),
                            "mod_value": mod_row[lang_columns[language_to_compare_index]],
                            "alt_value": "THIS IS NEW"
                        })

    if differences:
        output_to_text_file(differences, mod_ids_to_check)
        logging.info(f"String differences found and written to differences.txt.")
    else:
        logging.info("No string differences found between the mod's CSV and the alt translation's CSV.")

def output_to_text_file(differences: list, mod_ids_to_check: list):
    """
    Outputs the string differences to a text file.

    Args:
        differences (list): A list of dictionaries containing the differences between CSV files.
        mod_ids_to_check (list): A list of mod IDs that were checked.
    """
    with open("differences.txt", "w", encoding="utf-8") as f:
        for mod_id in mod_ids_to_check:
            diff_check = False
            for diff in differences:
                if diff["mod_id"] == mod_id:
                    if not diff_check:
                        f.write("=" * 100 + "\n")
                        f.write("=" * 100 + "\n")
                        f.write(f"\nMod ID: {mod_id}\n")
                        diff_check = True
                    
                    f.write(f"{diff['file']} \"{diff['key']}\" vs alt: \"{diff['mod_value']}\" vs \"{diff['alt_value']}\"\n\n")

if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
    
    mod_id = None
    if len(sys.argv) != 1:
        if len(sys.argv) != 2 and len(sys.argv) != 3:
            logging.error("Usage: python check_update.py <MOD_ID (optional)> <LANGUAGE (optional)>")
            logging.error("If no arguments are provided, the script will check all mods in the base path.")
            logging.error("MOD_ID is the Steam Workshop ID of the mod you want to check.")
            logging.error("LANGUAGE can be 'korean', 'japanese', or 'chinese'.")
            sys.exit(1)

        mod_id = sys.argv[1]
        if not mod_id.isdigit():
            logging.error("MOD_ID must be a Steam Workshop ID.")
            sys.exit(1)
    
    language_to_compare = sys.argv[2].lower() if len(sys.argv) == 0 or len(sys.argv) > 2 else "chinese"
    if language_to_compare not in ["korean", "japanese", "chinese"]:
        logging.error("Invalid language. Please use 'korean', 'japanese', or 'chinese'.")
        sys.exit(1)
    
    try:
        check_for_update(mod_id, language_to_compare)
    except Exception as e:
        logging.exception(e)
