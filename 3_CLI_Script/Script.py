import pyautogui
import time
import pyperclip

# Funzione per arrotondare al quarto più vicino
def round_to_quarter(val):
    return round(val * 4) / 4

# Funzione per normalizzare input: virgola->punto, float, arrotonda al quarto
def normalizza_input_voto(riga):
    if not riga or riga.strip() == "":
        return None
    try:
        val = float(riga.replace(",", "."))
        val = round_to_quarter(val)
        return val
    except ValueError:
        return None

# --- Funzione per convertire numero in voto ClasseViva ---
def decimale_to_classeviva(val):
    if val == 0: return ""
    elif val < 1.25: return "1"
    elif val < 1.75: return "1½"
    elif val < 2.25: return "2"
    elif val < 2.75: return "2½"
    elif val < 3.25: return "3"
    elif val < 3.75: return "3½"
    elif val < 4.25: return "4"
    elif val == 4.25: return "4+"
    elif val == 4.5: return "4½"
    elif val == 4.75: return "5-"
    elif val == 5: return "5"
    elif val == 5.25: return "5+"
    elif val == 5.5: return "5½"
    elif val == 5.75: return "6-"
    elif val == 6: return "6"
    elif val == 6.25: return "6+"
    elif val == 6.5: return "6½"
    elif val == 6.75: return "7-"
    elif val == 7: return "7"
    elif val == 7.25: return "7+"
    elif val == 7.5: return "7½"
    elif val == 7.75: return "8-"
    elif val == 8: return "8"
    elif val == 8.25: return "8+"
    elif val == 8.5: return "8½"
    elif val == 8.75: return "9-"
    elif val == 9: return "9"
    elif val == 9.25: return "9+"
    elif val == 9.5: return "9½"
    elif val == 9.75: return "10-"
    elif val == 10: return "10"
    else: return ""

token = True
primo_incolla = True  # Variabile globale per gestire il primo incolla

while token:
    # --- Inserimento voti da input utente ---
    print("Inserisci i dati. "
    "Scrivi 'f' su una riga e premi Invio per terminare l'inserimento. Entro 5 secondi dovrai posizionare il cursore nella prima casella del registro. "
    "Scrivi 'esc' per uscire dal programma")
    voti = []
    while True:
        try:
            riga = input()
        except EOFError:
            break
        if riga.strip().lower() == "f":
            break
        elif riga.strip().lower() == "esc":
            token = False
            break
        # Split per tab: ogni cella è un elemento, anche se vuoto
        celle = riga.split('\t')
        for cella in celle:
            if cella == "":
                voti.append(None)
            else:
                voto_norm = normalizza_input_voto(cella)
                # Se la normalizzazione fallisce, incolla il testo così com'è (per competenze tipo A, B, C, D)
                if voto_norm is not None:
                    voti.append(voto_norm)
                else:
                    voti.append(cella.strip() if cella.strip() else None)

    if not token: 
        break
        
    # --- Delay per posizionare il cursore ---
    print()  # Riga vuota per separare input e messaggio
    print("Posiziona il cursore nella prima casella del registro entro 5 secondi...")

    time.sleep(5)

    # Svuota la clipboard per evitare residui
    pyperclip.copy("")

    for voto in voti:
        if voto is None or (isinstance(voto, str) and voto.strip() == ""):
            # Valore vuoto: solo tab
            pyautogui.press('tab')
            time.sleep(0.1)
            continue
        # Se è un numero, convertilo in voto ClasseViva, altrimenti incolla il testo così com'è
        if isinstance(voto, (int, float)):
            testo = decimale_to_classeviva(voto)
        else:
            testo = str(voto)
        pyperclip.copy(testo)
        if primo_incolla:
            # Primo giro: incolla a vuoto, seleziona tutto, incolla il valore
            pyautogui.hotkey('command', 'v')  # Incolla a vuoto
            time.sleep(0.1)
            pyautogui.hotkey('command', 'a')  # Seleziona tutto
            time.sleep(0.1)
            pyautogui.hotkey('command', 'v')  # Incolla il primo valore
            primo_incolla = False
        else:
            time.sleep(0.1)
            pyautogui.hotkey('command', 'v')  # Incolla il valore
        pyautogui.press('tab')       # passa alla casella successiva
        time.sleep(0.1)              # piccolo ritardo per sicurezza