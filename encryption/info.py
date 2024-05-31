import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as st


class Info:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.geometry('710x420+440+180')
        self.window.configure(bg="#494949")
        self.window.resizable(width=0, height=0)

        label_style = ttk.Style()
        label_style.configure(".",  # имя стиля
                              foreground="#FFFFFF",  # цвет текста
                              font="helvetica 11",
                              padding=5,  # отступы
                              background="#494949")

        self.label = ttk.Label(self.window, text="Пароль", font="helvetica 18")
        self.label.grid(row=0, column=0)
        self.label.place(relx=0.045, rely=0.08)

        self.text_area = st.ScrolledText(self.window, font="helvetica 13", height=14, width=70, background="#494949",
                                         foreground="#FFFFFF")
        self.text_area.grid(row=1, column=0)
        self.text_area.place(relx=0.05, rely=0.25)
        self.text_area.insert(tk.INSERT,
                              """\
Назначает пароль, чтобы исключить неавторизованные изменения, 
выполняемые пользователем.

Следует использовать пароли, которые другие пользователи или программы не смогут быстро определить. Пароль должен соответствовать следующим 
требованиям:

  • Длина пароля – более восьми символов.

  • Представляет собой сочетание букв в разном регистре, цифр и специальных 
    символов.

  • Отсутствует в словарях и энциклопедиях.

  • Пароль не должен иметь прямую связь с персональными данными 
    пользователя, например, датой рождения или номером автомобиля.
        """)
        self.text_area.configure(state='disabled')

