# Spaggiari Tool - Istruzioni rapide

### A cosa serve
Come molti colleghi scrivo le valutazioni su un folgio excel, google sheets o un database notion oppure le faccio calcolare automaticamente a partire da dei descrittori.
Questo tool serve a trascrivere con un copia e incolla voti e competenze dal folgio di calcolo o database al registro elettronico.

### Cosa fa
Il tool riconosce tab e a capo nel testo incollato, converte i valori numerici nel formato dei voti di spaggiari con mezzi voti, "+" e "-", a partire dalla prima casella incolla il primo valore, preme tab, incolla il secondo e così via fino a terminare la lista.

## Requisiti
- Python 3 deve essere installato sul computer.
  - Scarica da: https://www.python.org/downloads/

## Come si usa


### Su Mac
1. Fai doppio click su `Voti e competenze in batch (MacOS).command`.
2. Se richiesto, consenti l'esecuzione del file (tasto destro > Apri la prima volta).
3. Segui le istruzioni a schermo.

### Su Windows
1. Fai doppio click su `Voti e competenze in batch (Windows).bat`.
2. Segui le istruzioni a schermo.

## Note
- Le dipendenze (pyautogui, pyperclip) vengono installate automaticamente se mancano.
- Per terminare l'inserimento voti premi Ctrl+D (Mac) o Ctrl+Z seguito da INVIO (Windows).
- Se hai problemi con i permessi su Mac, apri il Terminale nella cartella del tool e digita:
  chmod +x "Voti e competenze in batch (MacOS).command"
Poi riprova il doppio click.
# Il file principale dello script è `Script.py`.
## Problemi?
- Assicurati che Python sia installato e funzionante.
- Se qualcosa non va, riavvia il computer e riprova.
