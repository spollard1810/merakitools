import tkinter as tk
from tkinter import ttk

class BssidTab(ttk.Frame):
    def __init__(self, parent, device_manager):
        super().__init__(parent)
        self.device_manager = device_manager
        self.init_ui()

    def init_ui(self):
        controls_frame = ttk.Frame(self)
        controls_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(controls_frame, text="BSSID:").pack(side='left', padx=5)
        self.bssid_entry = ttk.Entry(controls_frame, width=40)
        self.bssid_entry.pack(side='left', padx=5)

