from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo, showerror, showwarning

class EntyTab(ttk.Frame):
    def __init__(self, parent, label_text, tooltip_text, **kwargs):
        super().__init__(parent)

        validate = kwargs.get('validate', 'none')
        validatecommand = kwargs.get('validatecommand', 'none')

        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0,1,2), weight=1)

        ttk.Label(self, text=label_text, width=10).grid(row=0,column=0, sticky='nswe')
        self.entry = ttk.Entry(self, width=30, validate=validate, validatecommand=validatecommand, state='normal')
        self.entry.grid(column=1, row=0, columnspan=2, sticky='nswe')
        ttk.Label(self, text=tooltip_text).grid(row=1,column=0, columnspan=3, sticky='nswe')

        self.pack(expand=True, fill='both', padx=5)


class UsersListFrame(ttk.Frame):
    def __init__(self, parent, label_text, command=None, button_text = "X"):
        super().__init__(parent)
        self.rowconfigure(0, weight=1)
        self.columnconfigure((0,1,2), weight=1)
        ttk.Label(self, text=label_text, width=10).grid(row=0,column=0, columnspan=2, sticky='nswe', pady=10, padx=20)
        ttk.Button(self, text=button_text, width=2, command=command).grid(row=0,column=2)

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def eror_message(box_title, msg, eror):
    showerror(title=box_title, message=f"{msg}: {eror}")

def info_message(box_title, msg):
    showinfo(title=box_title, message=msg)

def warning_message(box_title, msg):
    showwarning(title=box_title, message=msg)
