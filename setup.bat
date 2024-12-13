@echo off
REM Change to the directory of the script
cd /d "%~dp0"

REM Define paths
set EXE_PATH=%~dp0App\dist\app.exe
set SHORTCUT_PATH=%USERPROFILE%\Desktop\Torch.lnk
set ICON_PATH=%~dp0App\Icon\icon.ico

REM Check if the executable exists
if not exist "%EXE_PATH%" (
    echo Error: The executable app.exe was not found in App\dist.
    pause
    exit /b
)

REM Create the shortcut using PowerShell
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%EXE_PATH%'; $Shortcut.IconLocation = '%ICON_PATH%'; $Shortcut.Save();"

if %ERRORLEVEL% neq 0 (
    echo Failed to create shortcut. Check your paths and permissions.
    pause
    exit /b
)

echo Shortcut created successfully on Desktop!
pause