import tkinter as tk
from tkinter import ttk

class DevicesTab(ttk.Frame):
    def __init__(self, parent, device_manager):
        super().__init__(parent)
        self.device_manager = device_manager
        self.init_ui()

    def init_ui(self):
        # Create controls frame
        controls_frame = ttk.Frame(self)
        controls_frame.pack(fill='x', padx=5, pady=5)
        
        # Add Select All/Deselect All buttons
        ttk.Button(controls_frame, text="Select All", 
                  command=self.select_all).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Deselect All", 
                  command=self.deselect_all).pack(side='left', padx=5)

        # Create Treeview for devices
        self.tree = ttk.Treeview(self, columns=('name', 'model', 'serial'), 
                                show='headings')
        
        # Define columns
        self.tree.heading('name', text='Name')
        self.tree.heading('model', text='Model')
        self.tree.heading('serial', text='Serial')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def load_devices(self, network_id):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load and display devices
        devices = self.device_manager.load_devices(network_id)
        for device in devices:
            self.tree.insert('', 'end', values=(
                device.get('name', 'Unnamed'),
                device.get('model', 'Unknown'),
                device.get('serial', 'Unknown')
            ))

    def select_all(self):
        self.tree.selection_set(self.tree.get_children())
        self.device_manager.select_all()

    def deselect_all(self):
        self.tree.selection_remove(self.tree.get_children())
        self.device_manager.deselect_all()

    def on_select(self, event):
        # Update device manager with selected items
        for item in self.tree.get_children():
            serial = self.tree.item(item)['values'][2]
            is_selected = item in self.tree.selection()
            self.device_manager.toggle_device(serial, is_selected) 