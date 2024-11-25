class DeviceManager:
    def __init__(self, meraki_service):
        self.meraki_service = meraki_service
        self.devices = []
        self.selected_devices = set()
        
    def load_devices(self, network_id):
        self.devices = self.meraki_service.get_devices(network_id)
        self.selected_devices.clear()
        return self.devices
    
    def toggle_device(self, device_serial, selected):
        if selected:
            self.selected_devices.add(device_serial)
        else:
            self.selected_devices.discard(device_serial)
            
    def select_all(self):
        self.selected_devices = {device['serial'] for device in self.devices}
        
    def deselect_all(self):
        self.selected_devices.clear()
        
    def get_selected_devices(self):
        return [d for d in self.devices if d['serial'] in self.selected_devices] 