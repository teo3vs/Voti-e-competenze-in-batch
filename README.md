# Voti e Competenze in Batch
**Autore:** Matteo Trevisan  
**Licenza:** Open Source per docenti e scuole

Strumento di automazione desktop per trascrivere con un semplice copia e incolla voti e valutazioni per competenze da fogli di calcolo (**Excel**, **Google Fogli**, **Notion**) direttamente al registro elettronico **ClasseViva (Spaggiari)**.

---

## 📥 Download Eseguibili (Senza installare Python)

Scarica la versione per il tuo sistema operativo direttamente dalla sezione [Releases di GitHub](https://github.com/teo3vs/Voti-e-competenze-in-batch/releases) o dalla cartella `1_App_Standalone/`:

| Piattaforma | Download / File | Istruzioni di avvio |
| :--- | :--- | :--- |
| 🍏 **macOS** | **[Voti-e-Competenze-in-Batch-macOS.zip](https://github.com/teo3vs/Voti-e-competenze-in-batch/releases/latest)** | Estrai lo zip, trascina `Voti e Competenze in Batch.app` in **Applicazioni** e fai doppio clic. |
| 🪟 **Windows** | **[Voti-e-Competenze-in-Batch-Windows.zip](https://github.com/teo3vs/Voti-e-competenze-in-batch/releases/latest)** | Estrai lo zip e avvia `Voti e Competenze in Batch.exe` con doppio clic. |

---

## 🛡️ Note su Antivirus e Permessi di Sistema

Poiché l'applicazione automatizza la digitazione su schermo tramite librerie di sistema ed è un eseguibile open source indipendente non firmato con certificati a pagamento Microsoft/Apple:

### Su Windows (SmartScreen / Windows Defender / Antivirus):
* Al primo avvio, Windows Defender SmartScreen potrebbe mostrare la schermata blu *"PC protetto da Windows"*.
* **Cosa fare:** Clicca su **"Ulteriori informazioni"** e poi su **"Esegui comunque"**.
* Se un antivirus di terze parti segnala un falso positivo (dovuto a PyInstaller che impacchetta script Python in un unico file `.exe`), aggiungi l'eseguibile alle eccezioni dell'antivirus. Il codice sorgente completo è al 100% visibile e verificabile nella cartella `2_GUI_Python/app.py`.

### Su macOS (Accessibilità):
* Al primo inserimento, macOS chiederà di abilitare l'app per simulare la pressione dei tasti TAB e Incolla.
* **Cosa fare:** Apri *Impostazioni di Sistema > Privacy e Sicurezza > Accessibilità* e attiva la spunta accanto a **Voti e Competenze in Batch**.

---

## 📁 Struttura della Repository

```text
├── 1_App_Standalone/                     -> App pronte all'uso per macOS e Windows
│   ├── Voti e Competenze in Batch.app   -> App per macOS
│   ├── Voti e Competenze in Batch.exe   -> Eseguibile per Windows
│   ├── Voti-e-Competenze-in-Batch-macOS.zip
│   └── Voti-e-Competenze-in-Batch-Windows.zip
│
├── 2_GUI_Python/                         -> Versione grafica con codice sorgente Python
│   ├── app.py                           -> Applicazione con interfaccia WebKit nativa
│   ├── Avvia Applicazione (MacOS).command
│   ├── Avvia Applicazione (Windows).bat
│   └── Compila Eseguibile (Windows).bat -> Script per ricompilare l'.exe su Windows
│
├── 3_CLI_Script/                         -> Versione classica da terminale/riga di comando
│   ├── Script.py                        -> Script Python originale CLI
│   ├── Voti e competenze in batch (MacOS).command
│   └── Voti e competenze in batch (Windows).bat
│
├── assets/                              -> Icone del progetto (PNG, ICNS Apple, ICO Windows)
├── Voti e Competenze in Batch.app       -> Applicazione macOS pronta all'uso
└── Voti e Competenze in Batch.exe       -> Eseguibile Windows pronto all'uso
```

---

## 💻 Esecuzione da Codice Sorgente (2_GUI_Python)

Se preferisci eseguire direttamente lo script Python senza gli eseguibili standalone:

* **Requisiti:** Python 3.10 o superiore.
* **Mac:** doppio clic su `Avvia Applicazione (MacOS).command` (oppure `python3 app.py`).
* **Windows:** doppio clic su `Avvia Applicazione (Windows).bat` (oppure `python app.py`).

---

## ⌨️ Versione classica da Terminale (3_CLI_Script)

Per chi preferisce la riga di comando minimale senza interfaccia grafica:
* **Mac:** doppio clic su `Voti e competenze in batch (MacOS).command`.
* **Windows:** doppio clic su `Voti e competenze in batch (Windows).bat`.

---

## ⚠️ Disclaimer
Ricontrollare sempre che i dati inseriti dal tool siano conformi e corretti prima del salvataggio definitivo sul registro elettronico Spaggiari.
