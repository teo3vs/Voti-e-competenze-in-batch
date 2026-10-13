#!/bin/bash
cd "$(dirname "$0")"
# Mostra la versione di python3 usata
python3 --version
# Controlla che python3 sia installato
if ! command -v python3 &> /dev/null; then
  echo "Python3 non trovato. Installalo da https://www.python.org/downloads/"
  exit 1
fi
# Installa le dipendenze se mancano
# Usa sempre python3 -m pip per coerenza, con --break-system-packages per Homebrew/PEP668
python3 -m pip install --user --break-system-packages pyautogui pyperclip
# Avvia lo script
python3 "Script.py"
read -p "Premi INVIO per chiudere la finestra..."