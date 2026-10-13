@echo off
cd /d %~dp0
where python >nul 2>nul || (
  echo Python non trovato. Scaricalo da https://www.python.org/downloads/
  pause
  exit /b
)
REM Installa le dipendenze se mancano
python -m pip install --user pyautogui pyperclip
REM Avvia lo script
python "Script.py"
pause