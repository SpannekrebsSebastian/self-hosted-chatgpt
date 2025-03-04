import os
import discord
import faiss
import numpy as np
import openai  # Falls du Ollama später ersetzen willst
import requests
import json
import threading
import subprocess
import time
import tkinter as tk
from github import Github
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

# Automatische Installation der benötigten Module
def install_dependencies():
    required_packages = [
        "discord.py", "faiss-cpu", "numpy", "openai", "requests", "tk", "PyGithub", "langchain"
    ]
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"📦 Installiere {package}...")
            try:
                subprocess.run(["pip", "install", package], check=True)
            except subprocess.CalledProcessError:
                print(f"⚠ Fehler bei der Installation von {package}. Bitte manuell installieren.")

install_dependencies()

# Discord Bot Setup
TOKEN = "DEIN_DISCORD_BOT_TOKEN"
GUILD_ID = 123456789012345678  # Deine Server-ID
CHANNEL_IDS = [123456789012345678]  # Liste der relevanten Channel-IDs

# GitHub API Setup
GITHUB_TOKEN = "DEIN_GITHUB_TOKEN"
GITHUB_REPOS = ["angular/angular", "jenkinsci/jenkins", "pallets/flask"]

STACK_EXCHANGE_API = "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow&tagged=angular;docker;jenkins"

# Initialisiere FAISS-Datenbank
embedding_model = OpenAIEmbeddings()
vector_store = FAISS(embedding_model)

def fetch_github_issues():
    g = Github(GITHUB_TOKEN)
    all_issues = []
    for repo_name in GITHUB_REPOS:
        repo = g.get_repo(repo_name)
        issues = repo.get_issues(state="open")
        for issue in issues:
            all_issues.append(f"[{repo_name}] {issue.title}: {issue.body}")
    return all_issues

def fetch_stackoverflow_questions():
    response = requests.get(STACK_EXCHANGE_API)
    data = response.json()
    return [f"{q['title']} - {q['link']}" for q in data.get("items", [])]

def save_to_faiss(text):
    texts = [text]
    docs = embedding_model.embed_documents(texts)
    vector_store.add_texts(texts)

def auto_train_llm():
    new_github_issues = fetch_github_issues()
    new_stackoverflow_questions = fetch_stackoverflow_questions()
    new_data = new_github_issues + new_stackoverflow_questions
    if new_data:
        print("🚀 Training mit neuen GitHub-Issues und StackOverflow-Fragen startet...")
        save_to_faiss("\n".join(new_data))
    else:
        print("⚠ Keine neuen Daten zum Trainieren gefunden.")

def query_llm(query):
    retriever = vector_store.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=Ollama(model="mistral"), retriever=retriever)
    return qa_chain.run(query)

# GUI-Integration

def start_ollama():
    try:
        result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
        if "11434" in result.stdout:
            print("Ollama läuft bereits.")
            return
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
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
        ai_response = query_llm(user_input)
        chat_history.after(0, update_chat, ai_response)

    threading.Thread(target=fetch_response, daemon=True).start()

def update_chat(response):
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"KI: {response}\n\n", "ai")
    chat_history.yview(tk.END)
    chat_history.config(state=tk.DISABLED)

# Starte Ollama
start_ollama()

# GUI-Setup
root = tk.Tk()
root.title("Self-Hosted AI Assistant")
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