@echo off
cd /d "%~dp0"
echo Avvio di ClasseViva Batch Tool...

if not exist ".venv\Scripts\pythonw.exe" (
    echo Configurazione dell'ambiente virtuale Windows...
    if exist ".venv" rmdir /s /q ".venv"
    python -m venv .venv
    .venv\Scripts\pip install pyautogui pyperclip pywebview
)

start "" .venv\Scripts\pythonw.exe app.py
