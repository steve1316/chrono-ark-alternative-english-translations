import os
import shutil
from unset_translations import restore_originals


def sync_localization():
    # Set base directory paths.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    translated_base = os.path.join(script_dir, 'Localization') # Storage for translated files.
    backup_base = os.path.join(script_dir, 'Localization_backup') # Backup location for original files.

    # If backup directory does not exist, create it.
    if not os.path.exists(backup_base):
        os.makedirs(backup_base)
    else:
        # Otherwise, restore original files from backup.
        restore_originals()

    # Process each mod's localization files.
    for mod_id in os.listdir(translated_base):
        translated_localization = os.path.join(translated_base, mod_id, 'Localization') # Path to translated files.
        original_base = os.path.join(script_dir, '..', mod_id, 'Localization') # Path to original files.

        # Only process mods with existing localization directories.
        if os.path.isdir(translated_localization) and os.path.isdir(original_base):
            # Create backup directory for current mod.
            backup_path = os.path.join(backup_base, mod_id, 'Localization')
            os.makedirs(backup_path, exist_ok=True)

            # Backup original CSV files.
            for filename in os.listdir(original_base):
                if filename.endswith('.csv'):
                    src_file = os.path.join(original_base, filename)
                    dest_file = os.path.join(backup_path, filename)
                    shutil.copy2(src_file, dest_file) # copy2 preserves file metadata.
                    print(f'Backed up: {os.path.relpath(src_file, script_dir)} -> {os.path.relpath(dest_file, script_dir)}')

            # Deploy translated CSV files.
            for filename in os.listdir(translated_localization):
                if filename.endswith('.csv'):
                    src_file = os.path.join(translated_localization, filename)
                    dest_file = os.path.join(original_base, filename)
                    shutil.copy2(src_file, dest_file)
                    print(f'Deployed translation: {os.path.relpath(src_file, script_dir)} -> {os.path.relpath(dest_file, script_dir)}')

if __name__ == '__main__':
    sync_localization()