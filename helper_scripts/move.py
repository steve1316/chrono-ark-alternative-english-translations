import os
import shutil
import sys
import subprocess

def copy_mod_files(mod_id: str):
    """Copies the mod files to the alternative translations path and the Chrono Ark Mod path.
    
    Args:
        mod_id (str): The ID of the mod to copy.
    """
    base_path = r"D:\Steam\steamapps\workshop\content\1188930"
    mod_path = os.path.join(base_path, mod_id)
    alt_translations_path = os.path.join(base_path, "Alternative_English_Translations", "Localization", mod_id)
    chrono_ark_mod_path = r"D:\Steam\steamapps\common\Chrono Ark\Mod"

    # Check if the mod ID directory exists.
    if not os.path.exists(mod_path):
        raise FileNotFoundError(f"Mod ID {mod_id} does not exist at {mod_path}")

    # Check if the mod ID already exists in the alternative translations path.
    if os.path.exists(alt_translations_path):
        raise FileExistsError(f"Mod ID {mod_id} already exists in {alt_translations_path}")

    # Copy the Localization folder.
    localization_src = os.path.join(mod_path, "Localization")
    localization_dest = os.path.join(alt_translations_path, "Localization")
    shutil.copytree(localization_src, localization_dest)

    # Copy .png files.
    for item in os.listdir(mod_path):
        if item.endswith('.png'):
            shutil.copy(os.path.join(mod_path, item), alt_translations_path)

    # Copy the original mod files to Chrono Ark Mod path.
    chrono_ark_dest = os.path.join(chrono_ark_mod_path, mod_id)
    shutil.copytree(mod_path, chrono_ark_dest)

    # Open the destination folder in a new File Explorer window.
    subprocess.run(['explorer', alt_translations_path])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python merge.py <MOD_ID>")
        sys.exit(1)

    mod_id = sys.argv[1]
    try:
        copy_mod_files(mod_id)
        print(f"Mod files for {mod_id} copied successfully.")
    except Exception as e:
        print(f"Error: {e}")