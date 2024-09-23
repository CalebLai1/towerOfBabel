import tkinter as tk
from tkinter import ttk
from shared_functions import SharedFunctions
from conversation_mode import ConversationMode
from transcription_mode import TranscriptionMode

class TranscriptionApp:
    def __init__(self, master):
        self.master = master
        master.title("Multilingual Transcription App")
        master.geometry("800x600")

        self.shared = SharedFunctions()

        self.create_styles()

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.transcription_tab = TranscriptionMode(self.notebook, self.shared)
        self.conversation_tab = ConversationMode(self.notebook, self.shared)

        self.notebook.add(self.transcription_tab, text="Transcription")
        self.notebook.add(self.conversation_tab, text="Conversation")

        self.status_label = ttk.Label(master, text="")
        self.status_label.pack(pady=5)

    def create_styles(self):
        style = ttk.Style()
        style.configure("right.TFrame", background="#e1f5fe")
        style.configure("left.TFrame", background="#fff3e0")
        style.configure("right.TLabel", background="#e1f5fe", font=("Arial", 10))
        style.configure("left.TLabel", background="#fff3e0", font=("Arial", 10))

    def update_status(self, message):
        self.status_label.config(text=message)
        self.master.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()