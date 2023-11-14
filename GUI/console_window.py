from tkinter import ttk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import sys

class ConsoleWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.output_text_window = ScrolledText(self, wrap='word')
        self.output_text_window.pack(expand=True, fill='both')
        self.update_text_window_btn = ttk.Button(self, text="Обновить", command=self.__redirect_output)
        self.update_text_window_btn.pack(expand=True, fill='x', anchor='s', padx=20)
        self.pack(expand=True, fill='both')

    def __redirect_output(self):
        self.__update_text_window("Все работает типо без ошибок!")

    def __update_text_window(self, text):
        self.output_text_window.delete("1.0", 'end')
        self.output_text_window.insert('end', text)