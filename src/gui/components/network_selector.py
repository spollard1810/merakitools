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
        
        # Load networks and add "All Networks" option
        self.networks = self.meraki_service.get_networks()
        network_names = ["All Networks"] + [n['name'] for n in self.networks]
        self.network_combo['values'] = network_names
        
        # Add callback for network selection
        self.network_combo.bind('<<ComboboxSelected>>', self.on_network_selected)
        
        # Layout
        ttk.Label(self, text="Select Network:").pack(pady=5)
        self.network_combo.pack(pady=5)

    def on_network_selected(self, event):
        selected_index = self.network_combo.current()
        if selected_index == 0:  # "All Networks" selected
            network_ids = [n['id'] for n in self.networks]
            self.event_generate('<<NetworkSelected>>', 
                              data={'network_id': 'all', 'network_ids': network_ids})
        elif selected_index > 0:
            network_id = self.networks[selected_index - 1]['id']
            self.event_generate('<<NetworkSelected>>', 
                              data={'network_id': network_id, 'network_ids': [network_id]})