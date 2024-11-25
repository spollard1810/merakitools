import tkinter as tk
from tkinter import simpledialog

class ApiKeyDialog:
    def __init__(self, parent):
        self.parent = parent

    def get_api_key(self):
        api_key = simpledialog.askstring(
            "Meraki API Key",
            "Please enter your Meraki API key:",
            parent=self.parent,
            show='*'
        )
        return api_key 