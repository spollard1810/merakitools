import tkinter as tk
from tkinter import ttk

class NetworkSelector(ttk.Frame):
    def __init__(self, parent, meraki_service):
        super().__init__(parent)
        self.meraki_service = meraki_service
        self.init_ui()

    def init_ui(self):
        # Create combobox for network selection
        self.network_var = tk.StringVar()
        self.network_combo = ttk.Combobox(
            self,
            textvariable=self.network_var,
            state='readonly'
        )
        
        # Load networks
        networks = self.meraki_service.get_networks()
        self.network_combo['values'] = [n['name'] for n in networks]
        
        # Layout
        ttk.Label(self, text="Select Network:").pack(pady=5)
        self.network_combo.pack(pady=5) 