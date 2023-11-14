import tkinter as tk
import vk_api
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os

class AuthWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Окно авторизации")

        self.login_label = tk.Label(self, text="Логин:")
        self.login_label.pack()
        self.login_entry = tk.Entry(self)
        self.login_entry.pack()

        self.password_label = tk.Label(self, text="Пароль:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.auth_button = tk.Button(self, text="Авторизоваться", command=self.authorize)
        self.auth_button.pack()

    def authorize(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        try:
            vk_session = vk_api.VkApi(login, password, captcha_handler=self.captcha_handler)
            vk_session.auth()
            token = vk_session.token['access_token']
            self.destroy()
            return token
        except vk_api.AuthError as e:
            # Обработка ошибки авторизации
            print("Ошибка авторизации:", e)

    def captcha_handler(self, captcha):
        # Save captcha image to a temporary file
        captcha_image_path = os.path.join(os.getcwd(), "temp", "captcha.jpg")
        with open(captcha_image_path, "wb") as f:
            f.write(captcha.get_image())

        # Open a new window for captcha confirmation
        captcha_window = tk.Toplevel(self)
        captcha_window.title("Подтверждение капчи")

        # Display captcha image
        captcha_image = ImageTk.PhotoImage(Image.open(captcha_image_path))
        captcha_label = tk.Label(captcha_window, image=captcha_image)
        captcha_label.image = captcha_image
        captcha_label.pack()

        # Create captcha entry
        self.captcha_entry = tk.Entry(captcha_window)
        self.captcha_entry.pack()

        # Create submit button
        submit_button = tk.Button(captcha_window, text="Подтвердить", command=lambda: self.submit_captcha(self.captcha_entry.get(), captcha_window))
        submit_button.pack()

    def submit_captcha(self, captcha_key, captcha_window):
        captcha_window.destroy()
        self.captcha_entry.delete(0, tk.END)
        self.captcha_entry.insert(0, captcha_key)