import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from backend.controller import load_data, clear_data

def clear_output_data(data):
    cleared_text = ""
    for element in data:
        cleared_text += f"Имя: {element['name']}\n  Возраст: {element['age']}\n  Ссылка: {element['url']}\n\n"
    return cleared_text


class OutputWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.output_text_window = ScrolledText(self, wrap = 'word')
        self.output_text_window.pack(expand=True, fill='both')
        self.update_text_window_btn = ttk.Button(self, 
                                                 text="Обновить", command=self.__update_text_window).pack( fill='x', anchor='s', padx=20, pady=5)
        self.clear_text_window_btn = ttk.Button(self, 
                                                 text="Очистить", command=self._clear_text_window).pack( fill='x', anchor='s', padx=20)
        self.__update_text_window()
        self.pack(expand=True, fill='both')

    def _clear_text_window(self):
        clear_data()
        self.output_text_window.delete("0.0", 'end')

    def __update_text_window(self):
        text = clear_output_data(load_data())
        if len(self.output_text_window.get("0.0", 'end')) != 0:
            self.output_text_window.delete("0.0", 'end')
        self.output_text_window.insert('end', text)