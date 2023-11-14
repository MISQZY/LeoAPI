import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import json, os, re
from GUI.components import EntyTab, eror_message, warning_message, info_message
from backend.controller import save_sattings, clear_settings
from GUI.authorization_window import AuthWindow


def validate_api_key(newwal):
    if len(newwal) == 0:
        eror_message("Ошибка Апи Ключа", "В Апи ключе возникла ошибка", "Поле не может быть пустым!")
        return False
    if len(newwal) != 220:
        eror_message("Ошибка Апи Ключа", "В Апи ключе возникла ошибка", "Длина ключа должна быть 220 символов!")
        return False
    return True

# def validate_vk_id(newwal):
#     if len(newwal) == 0:
#         eror_message("Ошибка ", "В Вк id возникла ошибка", "Поле не может быть пустым!")
#         return False
#     try:
#         key = int(newwal)
#     except:
#         eror_message("Ошибка Вк id", "В Вк id возникла ошибка", "id должен состоять только из цифр!")
#         return False
#     if len(str(key)) != 9:
#         eror_message("Ошибка Вк id", "В Вк id возникла ошибка", "id должен быть длиной в 9 символов!")
#         return False
#     return True

def validate_filters(newwal):
    return True

def validate_cooldown(newwal):
    if len(newwal) == 0:
        eror_message("Ошибка ", "В задержке сообщения возникла ошибка", "Поле не может быть пустым!")
        return False
    try:
        int(newwal)
    except:
        eror_message("Ошибка в выставлении задержки", "В задержке сообщения возникла ошибка", "задержка должна быть целым числом!")
        return False
    return True


class SettingsWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # self.pack(fill='both', expand=True)
        self.__create_widgets()

    def __create_widgets(self):
        title_label = ttk.Label(self, text="Настройки",
                                background='burlywood2',
                                font=("Arial", 20),
                                justify="center", padding=10)
        
        title_label.pack(fill='x',padx=20, pady=15, anchor='n')

        self.left_side_frame = LeftSide(self)
        self.right_side_frame = RightSide(self)


    def generate_settings(self):
        info_message("Сохранено", "Настройки были успешно сохранены")

        checklist = str(self.master.left_side_frame.filters_input.entry.get())
        if len(checklist) != 0:
            checklist.split(', ')
        else:
            checklist = []

        token = self.master.left_side_frame.api_input.entry.get()
        ignore_mode = self.master.right_side_frame.spam_mode.get()
        pasive_mode = self.master.right_side_frame.passive_mode.get()
        cooldown_time = int(self.master.left_side_frame.cooldown_input.entry.get())

        settings_dict = {
                "token": token,
                "ignore_mode": ignore_mode,
                "passive_mode": pasive_mode,
                "checklist": checklist,
                "cooldown_time": cooldown_time
            }
        
        save_sattings(settings_dict)


    #         with open("settings.json", "w") as settings:
    #             json.dump(settings_dict, settings, indent=4)
    #     else:
    #         with open("settings.json", "w") as settings:
    #             json.dump(settings_dict, settings, indent=4)
    #         #accept_info("Успешно", "Настройки успешно сохранены")

class LeftSide(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', side='left', expand=True)
        
        self.check_api_key = (self.register(validate_api_key), '%P')
        # self.check_vk_id = (self.register(validate_vk_id), '%P')
        self.check_filters = (self.register(validate_filters), '%P')
        self.check_cooldown = (self.register(validate_cooldown), '%P')
        self.__create_widgets()

    def __create_widgets(self):
        self.api_input = EntyTab(self, "Апи ключ: ", "Подсказка:\nКак получить ключ указано в Help.txt",
                                 validate="focusout", validatecommand=self.check_api_key)
        # self.vk_id_input = EntyTab(self, "Vk ID: ", "Подсказка:\nЦифровой id вашей страницы, пример: 2124115",
        #                            validate="focusout", validatecommand=self.check_vk_id)
        self.filters_input = EntyTab(self, "Фильтры: ", "Подсказка:\nдля нескольких значений сепаратор ', '",
                                     validate="focusout", validatecommand=self.check_filters)
        self.cooldown_input = EntyTab(self, "Задержка\nсообщения: ", "Подсказка:\nВ мс",
                                     validate="focusout", validatecommand=self.check_cooldown)
        self.save_button = ttk.Button(self, text='Сохранить настройки', command=lambda: SettingsWindow.generate_settings(self)).pack( fill='both', padx=15, pady=5)
        self.clear_save_button = ttk.Button(self, text='Очистить все настройки', command=clear_settings).pack( fill='both', padx=15)

        # self.auth_button = tk.Button(self, text="Авторизация", command=self.open_auth_window)
        # self.auth_button.pack()

        # self.auth_window = None  # Переменная для хранения ссылки на окно авторизации

    def open_auth_window(self):
        if self.auth_window is None:  # Проверяем, что окно авторизации еще не открыто
            self.auth_window = AuthWindow()
            self.auth_window.protocol("WM_DELETE_WINDOW", self.close_auth_window)  # Обработчик закрытия окна авторизации

    def close_auth_window(self):
        self.auth_window.destroy()
        self.auth_window = None



class RightSide(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', side='right')
 
        self.spam_mode = tk.BooleanVar()
        self.spam_mode.set(False)

        self.passive_mode = tk.BooleanVar()
        self.passive_mode.set(False)

        self.console_toggle = tk.BooleanVar()
        self.console_toggle.set(False)


        self.__create_widgets()

    def __create_widgets(self):
        ttk.Label(self, text="Дополнительные параметры:", font=("Arial", 12)).pack(fill='x')
        self.settings_spam_mode_check = ttk.Checkbutton(self, 
                                                        text="Игнор мод", 
                                                        variable=self.spam_mode, 
                                                        onvalue=1, 
                                                        offvalue=0).pack(fill='x')
        self.settings_passive_mode_check = ttk.Checkbutton(self, 
                                                        text="Пасивный режим", 
                                                        variable=self.passive_mode, 
                                                        onvalue=1, 
                                                        offvalue=0).pack(fill='x')
        
        self.settings_console_toggle = ttk.Checkbutton(self, 
                                                        text="Консоль", 
                                                        variable=self.console_toggle, 
                                                        onvalue=1, 
                                                        offvalue=0, command=self.__update_root).pack(fill='x')
        # ttk.Label(self, text="Капча:", background='white', font=("Arial", 12)).pack(fill='x')

        # #add captcha img
        # self.image = Image.open(os.path.join(os.getcwd(), "temp", "captcha.jpeg")).resize([220,70])
        # self.photo = ImageTk.PhotoImage(self.image)

        # self.canvas = tk.Canvas(self, height=70, width=220)
        # self.c_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        # self.canvas.pack(expand=True, fill='both')

        # enter_captcha_entry = ttk.Entry(self, width=30).pack(fill='x')
        # enter_captcha_btn = ttk.Button(self, text='Ввести капчу'
        #                            ).pack(expand=True, fill='both', padx=15, pady=15)
    
    def __update_root(self):
        self.master.master.change_console_status(self.console_toggle.get())

    # def submit_spam_mode(): 
    #     result = askyesno(title="Режим спама", message="Вы уверены, что хотите включить режим спама?\nВ данном режиме все анкеты просто пропускаются.")
    #     if result: showinfo("Успешное сохранение", "Настройки успешно сохранены")
    #     else: showinfo("Сохранения отменены", "Операция отменена")

