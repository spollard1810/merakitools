import tkinter as tk
from tkinter import ttk, filedialog
import csv
from datetime import datetime

class ClientsTab(ttk.Frame):
    def __init__(self, parent, meraki_service):
        super().__init__(parent)
        self.meraki_service = meraki_service
        self.clients = []
        self.init_ui()

    def init_ui(self):
        # Create controls frame
        controls_frame = ttk.Frame(self)
        controls_frame.pack(fill='x', padx=5, pady=5)
        
        # Add Export button
        ttk.Button(controls_frame, text="Export to CSV", 
                  command=self.export_to_csv).pack(side='left', padx=5)
        
        # Add timespan selection
        ttk.Label(controls_frame, text="Time Period:").pack(side='left', padx=5)
        self.timespan_var = tk.StringVar(value="30 days")
        timespan_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.timespan_var,
            values=["24 hours", "7 days", "30 days"],
            state='readonly'
        )
        timespan_combo.pack(side='left', padx=5)
        timespan_combo.bind('<<ComboboxSelected>>', self.refresh_clients)

        # Create Treeview for clients
        self.tree = ttk.Treeview(
            self,
            columns=('description', 'mac', 'ip', 'first_seen', 'last_seen', 'usage'),
            show='headings'
        )
        
        # Define columns
        self.tree.heading('description', text='Description')
        self.tree.heading('mac', text='MAC Address')
        self.tree.heading('ip', text='IP Address')
        self.tree.heading('first_seen', text='First Seen')
        self.tree.heading('last_seen', text='Last Seen')
        self.tree.heading('usage', text='Usage (MB)')
        
        # Set column widths
        for col in self.tree['columns']:
            self.tree.column(col, width=130)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def load_clients(self, network_id):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get timespan in seconds
        timespan_map = {
            "24 hours": 86400,
            "7 days": 604800,
            "30 days": 2592000
        }
        timespan = timespan_map.get(self.timespan_var.get(), 2592000)
        
        # Load clients
        self.clients = self.meraki_service.get_clients(network_id, timespan)
        
        # Display clients
        for client in self.clients:
            usage_mb = round((client.get('usage', {}).get('sent', 0) + 
                            client.get('usage', {}).get('recv', 0)) / 1024 / 1024, 2)
            
            self.tree.insert('', 'end', values=(
                client.get('description', 'Unknown'),
                client.get('mac', 'Unknown'),
                client.get('ip', 'Unknown'),
                self.format_timestamp(client.get('firstSeen')),
                self.format_timestamp(client.get('lastSeen')),
                usage_mb
            ))

    def refresh_clients(self, event=None):
        if hasattr(self, 'current_network_id'):
            self.load_clients(self.current_network_id)

    def format_timestamp(self, timestamp):
        if not timestamp:
            return 'Unknown'
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M')
        except:
            return timestamp

    def export_to_csv(self):
        if not self.clients:
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[("CSV files", "*.csv")],
            initialfile=f'meraki_clients_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
        if not filename:
            return
            
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(['Description', 'MAC Address', 'IP Address', 
                           'First Seen', 'Last Seen', 'Usage (MB)'])
            
            # Write data
            for client in self.clients:
                usage_mb = round((client.get('usage', {}).get('sent', 0) + 
                                client.get('usage', {}).get('recv', 0)) / 1024 / 1024, 2)
                writer.writerow([
                    client.get('description', 'Unknown'),
                    client.get('mac', 'Unknown'),
                    client.get('ip', 'Unknown'),
                    self.format_timestamp(client.get('firstSeen')),
                    self.format_timestamp(client.get('lastSeen')),
                    usage_mb
                ]) 