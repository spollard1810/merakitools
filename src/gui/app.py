import tkinter as tk
from .components.api_key_dialog import ApiKeyDialog
from .components.network_selector import NetworkSelector
from src.services.meraki_service import MerakiService

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
        
        # Create network selector
        self.network_selector = NetworkSelector(self.root, self.meraki_service)
        self.network_selector.pack(pady=20)

    def run(self):
        self.root.mainloop() 