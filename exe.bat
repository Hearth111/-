@echo off
rem Build executable from display_server/main.py using PyInstaller
pyinstaller run_display.spec --distpath . --noconfirm

rem Verify the executable runs
if exist run_display.exe (
    echo Running run_display.exe for verification...
    run_display.exe
) else (
    echo Build failed: run_display.exe not found.
)
