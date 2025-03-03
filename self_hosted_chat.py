import tkinter as tk
import requests
import json
import threading
import subprocess
import time


def start_ollama():
    try:
        # Überprüfen, ob Ollama bereits läuft
        result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
        if "11434" in result.stdout:
            print("Ollama läuft bereits.")
            return

        # Ollama starten
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)  # Längere Verzögerung, um sicherzustellen, dass Ollama gestartet wurde
    except Exception as e:
        print(f"Fehler beim Starten von Ollama: {e}")


def send_prompt():
    user_input = input_box.get("1.0", tk.END).strip()
    if not user_input:
        return

    input_box.delete("1.0", tk.END)
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"Du: {user_input}\n", "user")
    chat_history.config(state=tk.DISABLED)

    def fetch_response():
        api_url = "http://localhost:11434/api/generate"
        data = {
            "model": "mistral",  # Alternativ "mixtral" oder "deepseek-coder"
            "prompt": user_input,
            "stream": False  # Verhindert die Ausgabe von gestreamten JSON-Objekten
        }

        try:
            response = requests.post(api_url, json=data, timeout=30)
            response.raise_for_status()

            # JSON-Antwort prüfen
            response_text = response.text.strip()
            print(f"DEBUG: API Antwort: {response_text}")
            response_json = json.loads(response_text)
            ai_response = response_json.get("response", "Fehler: Keine Antwort erhalten.")
        except requests.Timeout:
            ai_response = "Fehler: Anfrage hat zu lange gedauert."
        except requests.RequestException as e:
            ai_response = f"HTTP-Fehler: {str(e)}"
        except json.JSONDecodeError:
            ai_response = "Fehler: Ungültige JSON-Antwort vom Server. Überprüfe, ob `stream=False` gesetzt wurde."
        except Exception as e:
            ai_response = f"Fehler: {str(e)}"

        chat_history.after(0, update_chat, ai_response)

    threading.Thread(target=fetch_response, daemon=True).start()


def update_chat(response):
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"KI: {response}\n\n", "ai")
    chat_history.yview(tk.END)
    chat_history.config(state=tk.DISABLED)


# Ollama beim Start des Programms starten
start_ollama()

# GUI-Setup
root = tk.Tk()
root.title("Self-Hosted ChatGPT")
root.geometry("800x600")

chat_frame = tk.Frame(root)
chat_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

chat_history = tk.Text(chat_frame, wrap=tk.WORD, state=tk.DISABLED, bg="white", fg="black", font=("Arial", 10))
chat_history.tag_config("user", foreground="blue")
chat_history.tag_config("ai", foreground="green")
scrollbar = tk.Scrollbar(chat_frame, command=chat_history.yview)
chat_history.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_history.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

input_frame = tk.Frame(root)
input_frame.pack(pady=5, padx=10, fill=tk.X)

input_box = tk.Text(input_frame, height=3, wrap=tk.WORD, bg="white", fg="black", font=("Arial", 10))
input_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

send_button = tk.Button(input_frame, text="Senden", command=send_prompt, bg="blue", fg="white", font=("Arial", 10))
send_button.pack(side=tk.RIGHT, padx=5)

root.mainloop()
