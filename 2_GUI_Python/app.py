#!/usr/bin/env python3
"""
ClasseViva Batch Tool - Web Desktop App
Con conversione client-side istantanea (zero lag di rete) e automazione PyAutoGUI.
"""

import sys
import os
import time
import json
import threading
import platform
import subprocess
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import pyautogui
import pyperclip

PORT = 54321
IS_MAC = (platform.system() == "Darwin")
PASTE_MODIFIER = 'command' if IS_MAC else 'ctrl'

# Stato dell'automazione
state = {
    "is_running": False,
    "stop_requested": False,
    "status_message": "Pronto per inserire i dati.",
    "status_color": "normal",
    "current_index": 0,
    "total_count": 0
}

def run_automation_thread(items, countdown_sec, tab_delay):
    global state
    state["is_running"] = True
    state["stop_requested"] = False
    state["total_count"] = len(items)

    # 1. Countdown per posizionamento del cursore
    for remaining in range(countdown_sec, 0, -1):
        if state["stop_requested"]:
            state["is_running"] = False
            state["status_message"] = "Inserimento annullato."
            state["status_color"] = "warning"
            return
        state["status_message"] = f"👉 Clicca ORA sulla prima casella del registro! Avvio tra {remaining}s..."
        state["status_color"] = "warning"
        time.sleep(1)

    if state["stop_requested"]:
        state["is_running"] = False
        state["status_message"] = "Inserimento annullato."
        state["status_color"] = "warning"
        return

    state["status_message"] = "⚡ Inserimento in corso..."
    state["status_color"] = "success"

    primo_incolla = True
    pyperclip.copy("")
    total = len(items)

    try:
        for idx, item in enumerate(items, 1):
            if state["stop_requested"]:
                state["is_running"] = False
                state["status_message"] = f"Interrotto dall'utente ({idx-1}/{total} inseriti)."
                state["status_color"] = "warning"
                return

            state["current_index"] = idx
            val = item.get("converted", "")
            state["status_message"] = f"Inserimento {idx}/{total}: '{val}'..."

            if item.get("is_empty") or not val:
                pyautogui.press('tab')
                time.sleep(tab_delay)
                continue

            pyperclip.copy(str(val))

            if primo_incolla:
                pyautogui.hotkey(PASTE_MODIFIER, 'v')
                time.sleep(tab_delay)
                pyautogui.hotkey(PASTE_MODIFIER, 'a')
                time.sleep(tab_delay)
                pyautogui.hotkey(PASTE_MODIFIER, 'v')
                primo_incolla = False
            else:
                time.sleep(tab_delay)
                pyautogui.hotkey(PASTE_MODIFIER, 'v')

            pyautogui.press('tab')
            time.sleep(tab_delay)

        state["is_running"] = False
        state["status_message"] = "✅ Inserimento completato con successo!"
        state["status_color"] = "success"
    except Exception as e:
        state["is_running"] = False
        state["status_message"] = f"❌ Errore permessi macOS / simulazione: {e}"
        state["status_color"] = "error"


HTML_PAGE = """<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <title>Voti e Competenze in Batch - Matteo Trevisan</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    body { background: #121316; color: #e1e4ea; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
    header { background: #1a1c23; border-bottom: 1px solid #282c37; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; }
    header h1 { font-size: 17px; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 8px; }
    header p { font-size: 12px; color: #8e95a5; margin-top: 2px; }
    .author-badge { font-size: 11px; color: #60a5fa; background: #1e293b; padding: 3px 8px; border-radius: 12px; font-weight: 500; }
    .main { display: flex; flex: 1; overflow: hidden; padding: 14px; gap: 14px; }
    .col { flex: 1; display: flex; flex-direction: column; background: #1a1c23; border: 1px solid #282c37; border-radius: 10px; overflow: hidden; }
    .col-header { padding: 10px 14px; border-bottom: 1px solid #282c37; display: flex; justify-content: space-between; align-items: center; }
    .col-title { font-size: 13px; font-weight: 600; color: #cbd2e0; }
    .toolbar-btn { background: #282c37; color: #cbd2e0; border: none; border-radius: 6px; padding: 5px 12px; font-size: 12px; cursor: pointer; transition: 0.15s; }
    .toolbar-btn:hover { background: #353b49; color: #fff; }
    .btn-accent { background: #2563eb; color: #fff; }
    .btn-accent:hover { background: #1d4ed8; }
    textarea { flex: 1; background: #14161d; border: none; color: #f1f5f9; padding: 12px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; line-height: 1.5; resize: none; outline: none; }
    .table-container { flex: 1; overflow-y: auto; background: #14161d; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th { position: sticky; top: 0; background: #1e222d; color: #94a3b8; font-weight: 600; text-align: left; padding: 8px 12px; border-bottom: 1px solid #282c37; }
    td { padding: 6px 12px; border-bottom: 1px solid #1f232e; }
    tr:hover { background: #1e222e; }
    tr.active-row { background: #1e3a5f !important; font-weight: bold; }
    .tag-voto { background: #1e293b; color: #38bdf8; padding: 2px 8px; border-radius: 4px; font-weight: 600; display: inline-block; }
    .tag-empty { color: #64748b; font-style: italic; }
    footer { background: #1a1c23; border-top: 1px solid #282c37; padding: 12px 20px; display: flex; flex-direction: column; gap: 10px; }
    .controls-row { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }
    .opt-group { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #94a3b8; }
    select { background: #14161d; border: 1px solid #282c37; color: #f1f5f9; border-radius: 6px; padding: 6px 10px; font-size: 13px; outline: none; cursor: pointer; }
    .btn-action { padding: 9px 18px; border-radius: 6px; font-size: 13px; font-weight: 600; border: none; cursor: pointer; transition: 0.15s; }
    .btn-start { background: #16a34a; color: white; }
    .btn-start:hover { background: #15803d; }
    .btn-start:disabled { background: #1e293b; color: #64748b; cursor: not-allowed; }
    .btn-stop { background: #dc2626; color: white; }
    .btn-stop:hover { background: #b91c1c; }
    .btn-stop:disabled { background: #1e293b; color: #64748b; cursor: not-allowed; }
    .status-bar { font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
    .status-normal { color: #60a5fa; }
    .status-warning { color: #fbbf24; }
    .status-success { color: #4ade80; }
    .status-error { color: #f87171; }
    .footer-bottom { display: flex; justify-content: space-between; align-items: center; }
    .credits { font-size: 11px; color: #64748b; }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>🎓 Voti e Competenze in Batch</h1>
      <p>Copia e incolla i voti o le competenze da Excel, Google Fogli o Notion per compilarli nel registro ClasseViva.</p>
    </div>
  </header>

  <div class="main">
    <!-- Colonna Sinistra: Input -->
    <div class="col">
      <div class="col-header">
        <span class="col-title">1. Dati di Origine</span>
        <div style="display: flex; gap: 8px;">
          <button class="toolbar-btn btn-accent" onclick="pasteFromClipboard()">📋 Incolla Appunti</button>
          <button class="toolbar-btn" onclick="clearInput()">Cancella</button>
        </div>
      </div>
      <textarea id="rawInput" placeholder="Incolla qui i dati..." oninput="parseAndUpdate()"></textarea>
    </div>

    <!-- Colonna Destra: Anteprima -->
    <div class="col">
      <div class="col-header">
        <span class="col-title">2. Anteprima Conversione</span>
        <span id="statsLabel" style="font-size: 12px; color: #8e95a5;">0 celle caricate</span>
      </div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th style="width: 40px; text-align: center;">#</th>
              <th>Valore Originale</th>
              <th>Voto Spaggiari</th>
            </tr>
          </thead>
          <tbody id="previewBody">
            <tr>
              <td colspan="3" style="text-align: center; color: #64748b; padding: 40px;">Incolla i dati a sinistra per vedere l'anteprima</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <footer>
    <div class="controls-row">
      <div style="display: flex; gap: 16px;">
        <div class="opt-group">
          <label>Tempo posizionamento:</label>
          <select id="delaySelect">
            <option value="3" selected>3 secondi</option>
            <option value="5">5 secondi</option>
            <option value="7">7 secondi</option>
            <option value="10">10 secondi</option>
          </select>
        </div>
        <div class="opt-group">
          <label>Velocità:</label>
          <select id="speedSelect">
            <option value="0.05">Veloce (0.05s)</option>
            <option value="0.10" selected>Normale (0.10s)</option>
            <option value="0.20">Lenta (0.20s)</option>
          </select>
        </div>
      </div>

      <div style="display: flex; gap: 8px;">
        <button id="btnStop" class="btn-action btn-stop" onclick="stopAutomation()" disabled>⏹ Annulla</button>
        <button id="btnStart" class="btn-action btn-start" onclick="startAutomation()">🚀 Avvia Inserimento nel Registro</button>
      </div>
    </div>

    <div class="footer-bottom">
      <div class="status-bar">
        <span id="statusIndicator" class="status-normal">●</span>
        <span id="statusText" class="status-normal">Pronto per inserire i dati.</span>
      </div>
      <div class="credits">Sviluppato da Matteo Trevisan</div>
    </div>
  </footer>

  <script>
    let currentItems = [];

    // Conversione voti interamente client-side
    function roundToQuarter(val) {
      return Math.round(val * 4) / 4;
    }

    function decimalToClasseViva(val) {
      if (val === null || val === undefined || isNaN(val)) return "";
      if (val === 0) return "";
      if (val < 1.25) return "1";
      if (val < 1.75) return "1½";
      if (val < 2.25) return "2";
      if (val < 2.75) return "2½";
      if (val < 3.25) return "3";
      if (val < 3.75) return "3½";
      if (val < 4.25) return "4";
      if (val === 4.25) return "4+";
      if (val === 4.5) return "4½";
      if (val === 4.75) return "5-";
      if (val === 5) return "5";
      if (val === 5.25) return "5+";
      if (val === 5.5) return "5½";
      if (val === 5.75) return "6-";
      if (val === 6) return "6";
      if (val === 6.25) return "6+";
      if (val === 6.5) return "6½";
      if (val === 6.75) return "7-";
      if (val === 7) return "7";
      if (val === 7.25) return "7+"
      if (val === 7.5) return "7½";
      if (val === 7.75) return "8-";
      if (val === 8) return "8";
      if (val === 8.25) return "8+";
      if (val === 8.5) return "8½";
      if (val === 8.75) return "9-";
      if (val === 9) return "9";
      if (val === 9.25) return "9+";
      if (val === 9.5) return "9½";
      if (val === 9.75) return "10-";
      if (val === 10) return "10";
      return String(val);
    }

    function parseInputText(rawText) {
      if (!rawText || !rawText.trim()) return [];
      const lines = rawText.split(/\\r?\\n/);
      const items = [];
      let itemIdx = 1;

      for (const line of lines) {
        const cells = line.split('\\t');
        for (const cell of cells) {
          const rawCell = cell.trim();
          if (!rawCell) {
            items.append ? items.push({ id: itemIdx, original: "(vuoto)", converted: "", is_empty: true })
                         : items.push({ id: itemIdx, original: "(vuoto)", converted: "", is_empty: true });
          } else {
            // Verifica se è un numero con virgola o punto
            const numVal = parseFloat(rawCell.replace(',', '.'));
            if (!isNaN(numVal)) {
              const rounded = roundToQuarter(numVal);
              const conv = decimalToClasseViva(rounded);
              items.push({ id: itemIdx, original: rawCell, converted: conv, is_empty: false });
            } else {
              // Competenze o testo (A, B, C, D)
              items.push({ id: itemIdx, original: rawCell, converted: rawCell, is_empty: false });
            }
          }
          itemIdx++;
        }
      }
      return items;
    }

    function parseAndUpdate() {
      const text = document.getElementById('rawInput').value;
      currentItems = parseInputText(text);
      renderTable(currentItems);
    }

    function renderTable(items) {
      const tbody = document.getElementById('previewBody');
      const stats = document.getElementById('statsLabel');

      if (!items || items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" style="text-align: center; color: #64748b; padding: 40px;">Incolla i dati a sinistra per vedere l\\'anteprima</td></tr>';
        stats.innerText = '0 celle caricate';
        return;
      }

      let non_empty = 0;
      let html = '';
      items.forEach((it) => {
        if (!it.is_empty) non_empty++;
        const valConv = it.converted ? `<span class="tag-voto">${it.converted}</span>` : `<span class="tag-empty">(salta con Tab)</span>`;
        html += `<tr id="row-${it.id}"><td style="text-align:center; color:#64748b;">${it.id}</td><td>${escapeHtml(it.original)}</td><td>${valConv}</td></tr>`;
      });
      tbody.innerHTML = html;
      stats.innerText = `${items.length} celle totali (${non_empty} con voto/testo)`;
    }

    function escapeHtml(s) {
      return (s || '').replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    async function pasteFromClipboard() {
      try {
        const text = await navigator.clipboard.readText();
        if (text) {
          document.getElementById('rawInput').value = text;
          parseAndUpdate();
          return;
        }
      } catch (err) {}
      
      // Fallback tramite backend python
      try {
        const res = await fetch('/api/get-clipboard');
        const data = await res.json();
        if (data.text) {
          document.getElementById('rawInput').value = data.text;
          parseAndUpdate();
        }
      } catch (e) {}
    }

    function clearInput() {
      document.getElementById('rawInput').value = '';
      parseAndUpdate();
    }

    async function startAutomation() {
      if (!currentItems || currentItems.length === 0) {
        alert("Incolla prima i dati da inserire!");
        return;
      }

      const delay = parseInt(document.getElementById('delaySelect').value);
      const speed = parseFloat(document.getElementById('speedSelect').value);

      document.getElementById('btnStart').disabled = true;
      document.getElementById('btnStop').disabled = false;

      try {
        await fetch('/api/start', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            items: currentItems,
            countdown: delay,
            speed: speed
          })
        });
      } catch (err) {
        alert("Errore di connessione all'agente di automazione: " + err);
        document.getElementById('btnStart').disabled = false;
        document.getElementById('btnStop').disabled = true;
      }
    }

    async function stopAutomation() {
      try {
        await fetch('/api/stop', { method: 'POST' });
      } catch (e) {}
    }

    // Polling periodico dello stato
    setInterval(async () => {
      try {
        const res = await fetch('/api/status');
        const data = await res.json();
        
        const txt = document.getElementById('statusText');
        const ind = document.getElementById('statusIndicator');
        txt.innerText = data.status_message;
        txt.className = 'status-' + data.status_color;
        ind.className = 'status-' + data.status_color;

        document.getElementById('btnStart').disabled = data.is_running;
        document.getElementById('btnStop').disabled = !data.is_running;

        if (data.is_running && data.current_index > 0) {
          document.querySelectorAll('tr.active-row').forEach(r => r.classList.remove('active-row'));
          const activeRow = document.getElementById('row-' + data.current_index);
          if (activeRow) {
            activeRow.classList.add('active-row');
            activeRow.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
          }
        }
      } catch (e) {}
    }, 400);

    // Esegui subito l'aggiornamento se il textarea ha già testo
    window.addEventListener('DOMContentLoaded', () => {
      parseAndUpdate();
    });
  </script>
</body>
</html>
"""


class RequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(state).encode("utf-8"))
        elif self.path == "/api/get-clipboard":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            clip_text = ""
            try:
                clip_text = pyperclip.paste()
            except Exception:
                pass
            self.wfile.write(json.dumps({"text": clip_text}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len).decode("utf-8")
        data = json.loads(post_body) if post_body else {}

        if self.path == "/api/start":
            items = data.get("items", [])
            countdown = data.get("countdown", 5)
            speed = data.get("speed", 0.10)
            threading.Thread(target=run_automation_thread, args=(items, countdown, speed), daemon=True).start()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "started"}).encode("utf-8"))

        elif self.path == "/api/stop":
            global state
            state["stop_requested"] = True
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "stopping"}).encode("utf-8"))


def open_app_window(url):
    opened = False
    if IS_MAC:
        # Su macOS, 'open -a "Google Chrome" ...' o 'open ...' non scatena il blocco di privacy/automazione di sistema
        chrome_bundle = "/Applications/Google Chrome.app"
        brave_bundle = "/Applications/Brave Browser.app"

        if os.path.exists(chrome_bundle):
            try:
                subprocess.Popen(["open", "-a", "Google Chrome", "--args", f"--app={url}", "--window-size=920,700"])
                opened = True
            except Exception:
                pass

        if not opened and os.path.exists(brave_bundle):
            try:
                subprocess.Popen(["open", "-a", "Brave Browser", "--args", f"--app={url}", "--window-size=920,700"])
                opened = True
            except Exception:
                pass

        if not opened:
            try:
                subprocess.Popen(["open", url])
                opened = True
            except Exception:
                pass
    else:
        # Su Windows / Linux
        try:
            webbrowser.open(url)
            opened = True
        except Exception:
            pass

    if not opened:
        try:
            webbrowser.open(url)
        except Exception:
            pass


def main():
    # Gestione binding con reuse_address per evitare Address already in use
    server = None
    target_port = PORT
    for attempt in range(10):
        try:
            server = HTTPServer(("127.0.0.1", target_port), RequestHandler)
            break
        except OSError:
            target_port += 1

    if not server:
        print("Impossibile trovare una porta disponibile.")
        sys.exit(1)

    url = f"http://127.0.0.1:{target_port}"
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    print(f"Server pronto su {url}")

    # Prova ad aprire una VERA finestra desktop nativa tramite pywebview
    use_native_window = False
    try:
        import webview
        use_native_window = True
        print("[DEBUG] webview import OK")
    except Exception as e:
        print(f"[DEBUG] webview import FAILED: {e}")

    if use_native_window:
        try:
            print("[DEBUG] creating webview window...")
            window = webview.create_window(
                "Voti e Competenze in Batch",
                url=url,
                width=960,
                height=720,
                min_size=(800, 600)
            )
            print("[DEBUG] starting webview...")
            webview.start()
            print("[DEBUG] webview closed, exiting.")
            sys.exit(0)
        except Exception as e:
            import traceback
            print(f"[DEBUG] Errore apertura finestra nativa: {e}")
            traceback.print_exc()

    # Fallback su browser solo se pywebview non è disponibile o fallisce
    open_app_window(url)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
