import tkinter as tk
import requests
import json


def send_prompt():
    user_input = input_box.get("1.0", tk.END).strip()
    if not user_input:
        return

    input_box.delete("1.0", tk.END)
    chat_history.insert(tk.END, f"Du: {user_input}\n", "user")

    api_url = "http://localhost:11434/api/generate"
    data = {
        "model": "mixtral",  # Oder "deepseek-coder" für Coding-Aufgaben
        "prompt": user_input
    }

    try:
        response = requests.post(api_url, json=data)
        response_json = response.json()
        ai_response = response_json.get("response", "Fehler: Keine Antwort erhalten.")
    except Exception as e:
        ai_response = f"Fehler: {str(e)}"

    chat_history.insert(tk.END, f"KI: {ai_response}\n\n", "ai")
    chat_history.yview(tk.END)


# GUI-Setup
root = tk.Tk()
root.title("Self-Hosted ChatGPT")
root.geometry("600x400")

chat_history = tk.Text(root, wrap=tk.WORD, state=tk.NORMAL, bg="white", fg="black", font=("Arial", 10))
chat_history.tag_config("user", foreground="blue")
chat_history.tag_config("ai", foreground="green")
chat_history.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

input_box = tk.Text(root, height=3, wrap=tk.WORD, bg="white", fg="black", font=("Arial", 10))
input_box.pack(pady=5, padx=10, fill=tk.X)

send_button = tk.Button(root, text="Senden", command=send_prompt, bg="blue", fg="white", font=("Arial", 10))
send_button.pack(pady=5)

root.mainloop()
