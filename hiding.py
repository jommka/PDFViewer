import os
from io import BytesIO
import pyAesCrypt
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
from PyPDF2 import PdfFileReader, PdfFileWriter
from info import Info


class Hiding:
    def __init__(self):
        self.path = None
        self.pdf = None
        self.pdf_dec_reader = None
        self.window = Toplevel()
        self.window.geometry('450x320+440+180')
        self.window.configure(bg="#494949")
        self.window.resizable(width=0, height=0)

        self.display_text = tk.StringVar()

        label_style = ttk.Style()
        label_style.configure(".",  # имя стиля
                              foreground="#FFFFFF",  # цвет текста
                              font="helvetica 11",
                              padding=5,  # отступы
                              background="#494949")
        label_style.configure("TButton",  # имя стиля
                              foreground="#494949",  # цвет текста
                              font="helvetica 11",
                              background="#494949")

        self.label = ttk.Label(self.window, text="Скрытие данных в файле", font="helvetica 18")
        self.label.grid(row=0, column=0)
        self.label.place(relx=0.05, rely=0.08)

        self.entry_label = ttk.Label(self.window, text="Выберите PDF файл для скрытия потенциально",
                                     font="helvetica 11")
        self.entry_label.grid(row=1, column=0)
        self.entry_label.place(relx=0.05, rely=0.3)

        self.entry_label = ttk.Label(self.window, text="конфиденциальной информации.",
                                     font="helvetica 11")
        self.entry_label.grid(row=2, column=0)
        self.entry_label.place(relx=0.05, rely=0.4)

        self.button_choose = ttk.Button(self.window, text="Файл", command=self.check_file)
        self.button_choose.grid(row=2, column=0)
        self.button_choose.place(relx=0.07, rely=0.55, height=30, width=100)

        self.path_label = ttk.Label(self.window, textvariable=self.display_text, font="helvetica 11")
        self.path_label.grid(row=2, column=1)
        self.path_label.place(relx=0.35, rely=0.55)

        self.button_open = ttk.Button(self.window, text="Ок", command=self.hiding)
        self.button_open.grid(row=3, column=0)
        self.button_open.place(relx=0.07, rely=0.75, height=30, width=150)

        self.button_exit = ttk.Button(self.window, text="Отмена", command=self.window.destroy)
        self.button_exit.grid(row=3, column=1)
        self.button_exit.place(relx=0.55, rely=0.75, height=30, width=150)

    def check_file(self):
        filepath = fd.askopenfilename(title='Select a PDF file', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'),))
        if filepath:
            self.path = filepath
            self.pdf_dec_reader = PdfFileReader(self.path)
            self.display_text.set(os.path.basename(self.path))

    @staticmethod
    def hiding():
        print("+")
