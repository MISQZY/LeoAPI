import tkinter as tk
from tkinter import ttk
from GUI.navbar import Navbar
import os
from GUI.components import eror_message

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("LeoApi Bot")
        self.iconbitmap(os.path.join(os.getcwd(), "attachments", "icon.ico"))
        self.attributes("-topmost",True)
        self.geometry("600x500")
        self.resizable(False, False)

        self.navbar = Navbar(self)