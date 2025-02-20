import os
import shutil


def restore_originals():
    # Set base directory paths.
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Path to the script directory.
    backup_base = os.path.join(script_dir, 'Localization_backup') # Path to the backup directory.

    # Process each mod's localization files in the backup directory.
    for mod_id in os.listdir(backup_base):
        backup_localization = os.path.join(backup_base, mod_id, 'Localization') # Path to the backup localization directory.
        original_base = os.path.join(script_dir, '..', mod_id, 'Localization') # Path to the original localization directory.

        # Only process mods with existing backup and original localization directories.
        if os.path.isdir(backup_localization) and os.path.isdir(original_base):
            # Restore original CSV files from backup.
            for filename in os.listdir(backup_localization):
                if filename.endswith('.csv'):
                    src_file = os.path.join(backup_localization, filename)
                    dest_file = os.path.join(original_base, filename)
                    shutil.copy2(src_file, dest_file)
                    print(f'Restored original: {os.path.relpath(src_file, script_dir)} -> {os.path.relpath(dest_file, script_dir)}')

    # Remove the backup directory.
    if os.path.exists(backup_base):
        shutil.rmtree(backup_base)
        print(f'Backup directory {backup_base} removed')

if __name__ == '__main__':
    restore_originals()