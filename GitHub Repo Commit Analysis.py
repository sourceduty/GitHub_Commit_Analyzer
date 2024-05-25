import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox
import openai
import json

# Set your OpenAI API key
openai.api_key = "Your OpenAI API key here"

# Function to fetch commits from GitHub repository
def fetch_commits(repo_url):
    try:
        api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/")
        commits_url = f"{api_url}/commits"
        response = requests.get(commits_url)
        response.raise_for_status()
        commits = response.json()
        return commits
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch commits: {str(e)}")
        return []

# Function to analyze commits using OpenAI GPT-4 Turbo
def analyze_commits(commits):
    commit_messages = [commit['commit']['message'] for commit in commits]
    prompt = "Analyze the following commit messages and generate a Commit Analysis Report:\n" + "\n".join(commit_messages)
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an expert software analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        analysis = response.choices[0].message['content']
        return analysis
    except Exception as e:
        messagebox.showerror("Error", f"Failed to analyze commits: {str(e)}")
        return ""

# Function to handle the analysis process
def analyze_repo():
    repo_url = url_entry.get()
    if not repo_url.startswith("https://github.com/"):
        messagebox.showerror("Error", "Please enter a valid GitHub repository URL.")
        return
    
    commits = fetch_commits(repo_url)
    if not commits:
        return
    
    analysis = analyze_commits(commits)
    if analysis:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.INSERT, analysis)

# Create the GUI
root = tk.Tk()
root.title("GitHub Commit Analyzer")

tk.Label(root, text="GitHub Repository URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

analyze_button = tk.Button(root, text="Analyze Commits", command=analyze_repo)
analyze_button.pack(pady=10)

result_text = scrolledtext.ScrolledText(root, width=80, height=20)
result_text.pack(pady=10)

root.mainloop()
