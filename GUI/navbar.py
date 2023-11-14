from tkinter import ttk
from GUI.settings_window import SettingsWindow
from GUI.main_window import MainWindow
from GUI.output_window import OutputWindow
from GUI.console_window import ConsoleWindow

class Navbar(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill='both')
        
        self.__crete_widgets()

    def __crete_widgets(self):
        self.main_window = MainWindow(self)
        self.settings_window = SettingsWindow(self)
        self.output_window = OutputWindow(self)
        self.console_window = ConsoleWindow(self)

        # print(self.settings_window.children['!rightside'].console_toggle.get())

        
        self.add(self.main_window, text="Главная")
        self.add(self.settings_window, text="Настройки")
        self.add(self.output_window, text="Вывод")
        self.change_console_status(False)

    def change_console_status(self, status):
        if status is True:
            self.add(self.console_window, text="Консоль", state='normal')
        else:
            self.add(self.console_window, text="Консоль", state='hidden')
    