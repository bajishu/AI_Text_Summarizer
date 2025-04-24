import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from transformers import pipeline

# Load the summarizer model (abstractive by default)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Input Error", "Please enter or upload text to summarize.")
        return

    try:
        result = summarizer(text, max_length=130, min_length=30, do_sample=False)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result[0]['summary_text'])
    except Exception as e:
        messagebox.showerror("Error", str(e))

def upload_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        with open(filepath, 'r', encoding='utf-8') as file:
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, file.read())

def copy_summary():
    text = output_text.get("1.0", tk.END).strip()
    if text:
        root.clipboard_clear()
        root.clipboard_append(text)
        messagebox.showinfo("Copied", "Summary copied to clipboard.")

# GUI Setup
root = tk.Tk()
root.title("AI-Powered Text Summarizer")
root.geometry("800x600")
root.config(bg="#f2f2f2")

title = tk.Label(root, text="AI Text Summarizer", font=("Helvetica", 18, "bold"), bg="#f2f2f2")
title.pack(pady=10)

btn_frame = tk.Frame(root, bg="#f2f2f2")
btn_frame.pack()

upload_btn = tk.Button(btn_frame, text="📂 Upload File", command=upload_file)
upload_btn.grid(row=0, column=0, padx=10)

summarize_btn = tk.Button(btn_frame, text="🧠 Summarize", command=summarize_text)
summarize_btn.grid(row=0, column=1, padx=10)

copy_btn = tk.Button(btn_frame, text="📋 Copy Result", command=copy_summary)
copy_btn.grid(row=0, column=2, padx=10)

# Input text area
tk.Label(root, text="Input Text", bg="#f2f2f2").pack()
input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=15)
input_text.pack(padx=10, pady=5)

# Output summary
tk.Label(root, text="Summary", bg="#f2f2f2").pack()
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=10, bg="#e8f0fe")
output_text.pack(padx=10, pady=5)

root.mainloop()
