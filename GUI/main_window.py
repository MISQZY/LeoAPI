import tkinter as tk
from tkinter import ttk
from backend.leo_logic import start_processes, kill_processes
from GUI.components import UsersListFrame, eror_message
from backend.leo_logic import kill_process, start_process, get_process_list

class MainWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.__create_widgets()

    def __create_widgets(self):
        self.title_label = ttk.Label(self, text="LeoAPI Bot",
                                font=("Arial", 24),
                                background='burlywood2',
                                justify="center", padding=10)

        self.user_frame = ttk.Frame(self)

        # self.__update_process_list()

        self.start_button = ttk.Button(self, text='Запустить',command=self.__start_bot)
        self.stop_button = ttk.Button(self, text='Выключить', command=self.__stop_bot)


        self.title_label.pack(fill='x', padx=20, pady=15, anchor='n')
        self.user_frame.pack(expand=True, fill='both', anchor='center')
        self.stop_button.pack(fill='x', padx=50, pady=5, ipady=10, ipadx=10, side='bottom')
        self.start_button.pack(fill='x', padx=50, pady=5, ipady=10, ipadx=10, side='bottom')

    def __start_bot(self):
        try:
            start_processes()
        except Exception as e:
            eror_message(box_title="Ошибка", 
                         msg = "Во время выполнения произошла ошибка",
                         eror=e)
        # self.__update_process_list()
        self.start_button['state'] = 'disabled'
        self.start_button['text'] = 'Запущен'

        self.stop_button['state'] = 'normal'
        self.stop_button['text'] = 'Выключить'

    def __stop_bot(self):
        kill_processes()
        self.start_button['state'] = 'normal'
        self.start_button['text'] = 'Запустить'

        self.stop_button['state'] = 'disabled'
        self.stop_button['text'] = 'Выключен'
    
    # def __update_process_list(self):
    #     processes = get_process_list()
    #     for process in processes:
    #         UsersListFrame(self.user_frame, label_text=process.name, button_text="V").pack(fill='x')

