import tkinter as tk
from tkinter import ttk
from .components.api_key_dialog import ApiKeyDialog
from .components.network_selector import NetworkSelector
from src.services.meraki_service import MerakiService
from src.services.device_manager import DeviceManager
from .components.devices_tab import DevicesTab
from .components.clients_tab import ClientsTab

class MerakiApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Meraki Network Tool")
        self.root.geometry("800x600")
        
        self.meraki_service = MerakiService()
        self.init_ui()

    def init_ui(self):
        # First prompt for API key
        api_key_dialog = ApiKeyDialog(self.root)
        api_key = api_key_dialog.get_api_key()
        
        if not api_key:
            self.root.quit()
            return
            
        self.meraki_service.set_api_key(api_key)
        
        # Create device manager
        self.device_manager = DeviceManager(self.meraki_service)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create devices tab
        self.devices_tab = DevicesTab(self.notebook, self.device_manager)
        self.notebook.add(self.devices_tab, text='Devices')
        
        # Create clients tab
        self.clients_tab = ClientsTab(self.notebook, self.meraki_service)
        self.notebook.add(self.clients_tab, text='Clients')
        
        # Create network selector
        self.network_selector = NetworkSelector(self.root, self.meraki_service)
        self.network_selector.pack(pady=20)
        
        # Bind network selection to device loading
        self.network_selector.bind('<<NetworkSelected>>', self.on_network_selected)

    def on_network_selected(self, event):
        network_id = event.data['network_id']
        self.devices_tab.load_devices(network_id)
        self.clients_tab.current_network_id = network_id
        self.clients_tab.load_clients(network_id)

    def run(self):
        self.root.mainloop() 