@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

echo ========================================================
echo  Compilazione: Voti e Competenze in Batch (.exe)
echo  Autore: Matteo Trevisan
echo ========================================================
echo.

REM 1. Individuazione interprete Python valido
set "PY_CMD="

py -3 --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py -3"
    goto :FOUND_PY
)

py --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py"
    goto :FOUND_PY
)

python --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=python"
    goto :FOUND_PY
)

for %%D in (
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "C:\Program Files\Python313\python.exe"
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python310\python.exe"
    "C:\Python313\python.exe"
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
) do (
    if exist %%D (
        set "PY_CMD=%%~D"
        goto :FOUND_PY
    )
)

echo.
echo [ERRORE] Nessun interprete Python valido trovato nel sistema!
pause
exit /b 1

:FOUND_PY
echo [OK] Trovato Python: %PY_CMD%
echo.

REM 2. Installazione librerie con l'interprete di sistema (evita il bug di venv su cartelle di rete WebDAV/UTM)
echo [INFO] Installazione/aggiornamento librerie necessarie (pyautogui, pyperclip, pywebview, pyinstaller)...
%PY_CMD% -m pip install --upgrade pip
%PY_CMD% -m pip install pyautogui pyperclip pywebview pyinstaller
if errorlevel 1 (
    echo [ERRORE] Errore durante l'installazione delle librerie con pip.
    pause
    exit /b 1
)

echo.
echo [INFO] Compilazione in corso con PyInstaller...
%PY_CMD% -m PyInstaller --noconfirm --onefile --windowed --name "Voti e Competenze in Batch" --icon "assets/icon.ico" app.py

if errorlevel 1 (
    echo.
    echo ========================================================
    echo [ERRORE] La compilazione con PyInstaller e' fallita.
    echo ========================================================
    pause
    exit /b 1
)

echo.
echo ========================================================
echo  COMPILAZIONE COMPLETATA CON SUCCESSO!
echo ========================================================
echo Trovi il file "Voti e Competenze in Batch.exe" dentro:
echo %~dp0dist\Voti e Competenze in Batch.exe
echo ========================================================
echo.
pause
