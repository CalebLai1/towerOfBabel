import tkinter as tk
from tkinter import ttk
from offline_mode import OfflineMode
from realtime_mode import RealtimeMode
from shared_functions import preload_models

class TranslationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Translation App")
        self.master.geometry("800x600")
        self.master.minsize(600, 400)  # Set minimum size

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.offline_mode = OfflineMode(self.notebook)
        self.realtime_mode = RealtimeMode(self.notebook)

        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        mode_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Mode", menu=mode_menu)
        mode_menu.add_command(label="Offline Mode", command=self.switch_to_offline)
        mode_menu.add_command(label="Realtime Mode", command=self.switch_to_realtime)

    def switch_to_offline(self):
        self.notebook.select(self.offline_mode.frame)

    def switch_to_realtime(self):
        self.notebook.select(self.realtime_mode.frame)

if __name__ == "__main__":
    preload_models()
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()