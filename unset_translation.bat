@echo off
setlocal enabledelayedexpansion

:: Set base directory paths.
set "SCRIPT_DIR=%~dp0"
set "BACKUP_BASE=%SCRIPT_DIR%Localization_backup"

:: If backup directory exists, restore the original files.
if exist "%BACKUP_BASE%" (
    for /d %%m in ("%BACKUP_BASE%\*") do (
        set "mod_id=%%~nxm"
        set "original_loc=%SCRIPT_DIR%..\!mod_id!\Localization"
        set "backup_loc=%BACKUP_BASE%\!mod_id!\Localization"
        
        if exist "!original_loc!" (
            xcopy "!backup_loc!\*.csv" "!original_loc!\" /Y >nul
            echo Restored original localization files for !mod_id!
        )
    )

    :: Remove the backup directory.
    rmdir /s /q "%BACKUP_BASE%"
    echo Original files restored and backup folder removed.
) else (
    echo No backup found - nothing to restore.
)

endlocal
pause