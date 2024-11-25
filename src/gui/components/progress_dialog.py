import tkinter as tk
from tkinter import ttk

class ProgressDialog(tk.Toplevel):
    def __init__(self, parent, title="Progress"):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x150")
        self.transient(parent)
        self.grab_set()
        
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Starting...")
        
        self.init_ui()
        
    def init_ui(self):
        # Status label
        ttk.Label(self, textvariable=self.status_var).pack(pady=10)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self,
            variable=self.progress_var,
            maximum=100,
            length=200,
            mode='determinate'
        )
        self.progress_bar.pack(pady=10)
        
    def update_progress(self, percentage, status_text):
        self.progress_var.set(percentage)
        self.status_var.set(status_text)
        self.update() 