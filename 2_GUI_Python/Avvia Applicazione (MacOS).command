#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

# Controlla se l'ambiente virtuale esiste, altrimenti lo crea e installa le dipendenze
if [ ! -d ".venv" ]; then
    echo "Configurazione dell'ambiente per la prima volta..."
    /usr/bin/python3 -m venv .venv
    CFLAGS="-Wno-error=default-const-init-var-unsafe" .venv/bin/pip install pyautogui pyperclip customtkinter
fi

# Avvia l'applicazione desktop
exec .venv/bin/python3 "$DIR/app.py"
