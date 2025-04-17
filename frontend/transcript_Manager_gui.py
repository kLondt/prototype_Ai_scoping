import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import os

class TranscriptManagerGUI:                                 #using a gui created by VO
    def __init__(self, root):
        self.root = root
        self.root.title("Transcript Manager")
        self.root.geometry("800x600")
        
        self.transcript = ""
        self.file_path = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Upload tab
        self.upload_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.upload_frame, text="Upload Document")
        
        # Paste tab
        self.paste_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.paste_frame, text="Paste Transcript")
        
        # Upload tab content
        ttk.Label(self.upload_frame, text="Select a text file to upload:").pack(pady=10)
        ttk.Button(self.upload_frame, text="Browse...", command=self.browse_file).pack(pady=5)
        self.file_label = ttk.Label(self.upload_frame, text="No file selected")
        self.file_label.pack(pady=5)
        
        # Paste tab content
        ttk.Label(self.paste_frame, text="Paste your transcript here:").pack(pady=10)
        self.paste_text = scrolledtext.ScrolledText(self.paste_frame, height=10)
        self.paste_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        ttk.Button(self.paste_frame, text="Use This Text", command=self.use_pasted_text).pack(pady=5)
        
        # Preview and edit section
        self.preview_frame = ttk.LabelFrame(self.root, text="Transcript Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.edit_button = ttk.Button(self.preview_frame, text="Edit", command=self.toggle_edit)
        self.edit_button.pack(anchor=tk.NE, padx=10, pady=5)
        
        self.transcript_text = scrolledtext.ScrolledText(self.preview_frame, height=10)
        self.transcript_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.transcript_text.config(state=tk.DISABLED)
        
        # Bottom buttons
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(self.button_frame, text="Save Transcript", command=self.save_transcript).pack(side=tk.RIGHT, padx=5)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.transcript = file.read()
                    self.update_preview()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not read file: {e}")
    
    def use_pasted_text(self):
        self.transcript = self.paste_text.get("1.0", tk.END).strip()
        self.update_preview()
    
    def update_preview(self):
        self.transcript_text.config(state=tk.NORMAL)
        self.transcript_text.delete("1.0", tk.END)
        self.transcript_text.insert(tk.END, self.transcript)
        self.transcript_text.config(state=tk.DISABLED)
    
    def toggle_edit(self):
        if self.transcript_text.cget("state") == tk.DISABLED:
            self.transcript_text.config(state=tk.NORMAL)
            self.edit_button.config(text="Save Changes")
        else:
            self.transcript = self.transcript_text.get("1.0", tk.END).strip()
            self.transcript_text.config(state=tk.DISABLED)
            self.edit_button.config(text="Edit")
    
    def save_transcript(self):
        if not self.transcript:
            tk.messagebox.showinfo("Info", "No transcript to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.transcript)
                tk.messagebox.showinfo("Success", f"Transcript saved to {file_path}")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not save file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptManagerGUI(root)
    root.mainloop()