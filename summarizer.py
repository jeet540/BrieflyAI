import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import google.generativeai as genai

# ==========================================
# 1. GEMINI AI CONFIGURATION
# ==========================================
# YAHA APNI REAL GEMINI API KEY DAALEIN
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=API_KEY)

# ==========================================
# 2. CORE FUNCTIONS (BACKEND)
# ==========================================
def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    elif ext == '.pdf':
        try:
            import pypdf
            reader = pypdf.PdfReader(file_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
        except ImportError:
            raise ImportError("PDF files read karne ke liye 'pypdf' package zaroori hai.")
    else:
        raise ValueError("Sirf .txt aur .pdf files hi support hoti hain.")

def generate_summary():
    file_path = file_path_var.get()
    if not file_path:
        messagebox.showwarning("Warning", "Kripya pehle ek PDF ya Text file select karein!")
        return
    status_label.config(text="AI Summary generate kar raha hai... Kripya intezar karein.", fg="#d35400")
    root.update_idletasks()
    try:
        text_content = extract_text_from_file(file_path)
        if not text_content.strip():
            raise ValueError("File khali hai ya usme se text nahi nikala ja saka.")
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Please provide a clear, concise bullet-point summary of the following text in Hindi or English (depending on user convenience, output should be easy to understand):\n\n{text_content}"
        response = model.generate_content(prompt)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, response.text)
        status_label.config(text="Summary safaltapoorvak taiyar ho gayi!", fg="#27ae60")
    except Exception as e:
        status_label.config(text="Error occurred!", fg="#c0392b")
        messagebox.showerror("Error", f"Kuch galat hua:\n{str(e)}")

def browse_file():
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Text & PDF Files", ".txt *.pdf"), ("Text Files", ".txt"), ("PDF Files", "*.pdf")]
    )
    if file_path:
        file_path_var.set(file_path)
        file_label.config(text=os.path.basename(file_path))
        status_label.config(text="File select ho gayi. Ab 'Summarize' button par click karein.", fg="#2980b9")
        output_text.delete("1.0", tk.END)

# ==========================================
# 3. MODERN GUI DESIGN (TKINTER)
# ==========================================
root = tk.Tk()
root.title("AI Desktop Text & PDF Summarizer")
root.geometry("650x550")
root.configure(bg="#f5f6fa")

file_path_var = tk.StringVar()
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)

header_label = tk.Label(root, text="AI Document Summarizer", font=("Segoe UI", 16, "bold"), bg="#f5f6fa", fg="#2c3e50")
header_label.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=25)

top_frame = tk.Frame(root, bg="#ffffff", bd=1, relief="solid")
top_frame.grid(row=1, column=0, padx=25, pady=10, sticky="ew")
top_frame.grid_columnconfigure(1, weight=1)

browse_btn = tk.Button(top_frame, text="Choose File (.txt/.pdf)", command=browse_file, font=("Segoe UI", 10, "bold"), bg="#3498db", fg="white", bd=0, padx=15, pady=8, cursor="hand2")
browse_btn.grid(row=0, column=0, padx=10, pady=10, sticky="w")

file_label = tk.Label(top_frame, text="Koi file select nahi ki gayi", font=("Segoe UI", 10, "italic"), bg="#ffffff", fg="#7f8c8d", anchor="w")
file_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

summarize_btn = tk.Button(root, text="⚡ Generate AI Summary", command=generate_summary, font=("Segoe UI", 12, "bold"), bg="#2ecc71", fg="white", bd=0, padx=20, pady=10, cursor="hand2")
summarize_btn.grid(row=2, column=0, padx=25, pady=10, sticky="ew")

status_label = tk.Label(root, text="Shuru karne ke liye ek file upload karein.", font=("Segoe UI", 9), bg="#f5f6fa", fg="#7f8c8d")
status_label.grid(row=3, column=0, padx=25, pady=(5, 0), sticky="w")

output_frame = tk.Frame(root, bg="#ffffff", bd=1, relief="solid")
output_frame.grid(row=4, column=0, padx=25, pady=(5, 20), sticky="nsew")
output_frame.grid_rowconfigure(0, weight=1)
output_frame.grid_columnconfigure(0, weight=1)

scrollbar = ttk.Scrollbar(output_frame)
scrollbar.grid(row=0, column=1, sticky="ns")

output_text = tk.Text(output_frame, font=("Segoe UI", 11), wrap="word", bd=0, yscrollcommand=scrollbar.set, bg="#ffffff", fg="#2c3e50", padx=10, pady=10)
output_text.grid(row=0, column=0, sticky="nsew")
scrollbar.config(command=output_text.yview)

root.mainloop()