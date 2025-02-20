@echo off
setlocal enabledelayedexpansion

:: Set base directory paths.
set "SCRIPT_DIR=%~dp0"
:: Where translated files are stored.
set "TRANSLATED_BASE=%SCRIPT_DIR%Localization" 
:: Where backup files are stored.
set "BACKUP_BASE=%SCRIPT_DIR%Localization_backup"

:: If backup directory exists, run unset_translation.bat to restore the original files first.
if exist "%BACKUP_BASE%" (
    call unset_translation.bat
)

:: Iterate over each mod ID directory in the translated base.
for /d %%m in ("%TRANSLATED_BASE%\*") do (
    set "mod_id=%%~nxm"
    :: Set the path to the original localization files.
    set "original_loc=%SCRIPT_DIR%..\!mod_id!\Localization"
    :: Set the path to the translated localization files.
    set "translated_loc=%TRANSLATED_BASE%\!mod_id!\Localization"
    set "backup_loc=%BACKUP_BASE%\!mod_id!\Localization"
    
    :: If the original localization files exist, create a backup directory and copy the original files to it.
    if exist "!original_loc!" (
        mkdir "!backup_loc!"
        xcopy "!original_loc!\*.csv" "!backup_loc!\" /Y >nul
        xcopy "!translated_loc!\*.csv" "!original_loc!\" /Y >nul
        echo Translations deployed for !mod_id!
    )
)

endlocal
pause