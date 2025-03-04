# Self-Hosted AI Assistant mit Discord Crawler & RAG

## 📌 Beschreibung
Dieses Projekt kombiniert einen **lokalen KI-Assistenten (Ollama)** mit einem **Discord-Crawler**, **GitHub- & Stack Overflow-Scraper** und einer **Retrieval-Augmented Generation (RAG)**, um aktuelle Entwicklerinfos für DevSecOps, Fullstack & KI bereitzustellen.

## 🚀 Features
- 🖥 **Self-Hosted KI** → Läuft mit Ollama & lokalen LLMs (`mistral`, `mixtral`, `deepseek-coder`)
- 🤖 **Discord-Integration** → Crawlt Nachrichten aus Entwickler-Channels
- 📝 **GitHub & Stack Overflow API** → Holt Issues & Fragen zu relevanten Themen
- 🔍 **Vektorbasierte Suche mit FAISS** → Speichert & sucht relevante Infos
- 🛠 **Automatisches Training mit LoRA/QLoRA** → Falls neue Daten gefunden werden
- 🖼 **GUI** → Benutzerfreundliche Oberfläche mit `tkinter`

## 📂 Installation & Einrichtung
### **1️⃣ Abhängigkeiten installieren**
Falls `pip` noch nicht alle Pakete installiert hat, führe folgendes aus:
```sh
pip install discord.py faiss-cpu numpy openai requests tk PyGithub langchain
```
Falls du eine **NVIDIA-GPU** hast, kannst du `faiss-gpu` anstelle von `faiss-cpu` verwenden:
```sh
pip install faiss-gpu
```

### **2️⃣ Umgebungsvariablen setzen**
Ersetze die API-Tokens in der `self_hosted_chat.py`:
```python
TOKEN = "DEIN_DISCORD_BOT_TOKEN"
GITHUB_TOKEN = "DEIN_GITHUB_TOKEN"
```
Falls du Channels begrenzen möchtest:
```python
CHANNEL_IDS = [123456789012345678]  # Discord Channel-IDs
```

### **3️⃣ Starte die Anwendung**
```sh
python self_hosted_chat.py
```
Falls Ollama nicht automatisch startet, kannst du es manuell starten:
```sh
ollama serve
```

## 📖 Nutzung
- **Gib Fragen in die GUI ein** → Das Modell sucht relevante Infos aus Discord/GitHub/Stack Overflow & antwortet
- **Neue Daten in FAISS speichern** → Automatische Speicherung & Abrufbarkeit
- **Discord-Crawler läuft automatisch** → Holt & speichert neue Nachrichten

## ⚠ Fehlerbehebung
### ❌ `ModuleNotFoundError: No module named 'faiss'`
Lösung:
```sh
pip install faiss-cpu  # oder faiss-gpu bei NVIDIA-GPU
```
Falls es weiterhin nicht funktioniert:
```sh
pip install faiss-cpu --no-cache-dir
```

### ❌ `Ollama Fehler: Port 11434 belegt`
Falls Ollama nicht startet:
```sh
netstat -ano | findstr :11434  # Prüfe, ob der Port belegt ist
```
Falls Ollama bereits läuft:
```sh
ollama serve
```
Falls ein anderer Prozess den Port blockiert:
```sh
taskkill /PID <PID> /F
```

## 📌 Weiterentwicklung
- 🛠 **Integration von weiteren APIs** → Mehr Datenquellen wie Hacker News oder Reddit
- 🧠 **Bessere LLM-Optimierung** → Feintuning der Modelle für spezifische Aufgaben
- 🌐 **Web-Frontend** → Moderne Web-Oberfläche statt `tkinter`

---
Made with ❤️ by Sebastian Spannekrebs

