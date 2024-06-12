import os
from io import BytesIO
import pyAesCrypt
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
from PyPDF2 import PdfFileReader, PdfFileWriter

from encryption.info import Info


class Encrypt:
    def __init__(self):
        self.path = None
        self.pdf = None
        self.pdf_dec_reader = None
        self.window = Toplevel()
        self.window.geometry('520x400+440+180')
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

        self.label = ttk.Label(self.window, text="Шифрование и доступ к файлу", font="helvetica 18")
        self.label.grid(row=0, column=0)
        self.label.place(relx=0.05, rely=0.08)

        self.enabled = IntVar()
        self.enabled_checkbutton = ttk.Checkbutton(self.window, text="Шифрование AES256-CBC", variable=self.enabled)
        self.enabled_checkbutton.place(relx=0.08, rely=0.25)

        self.button_choose = ttk.Button(self.window, text="Файл", command=self.check_file)
        self.button_choose.grid(row=2, column=0)
        self.button_choose.place(relx=0.08, rely=0.38, height=30, width=100)

        self.path_label = ttk.Label(self.window, textvariable=self.display_text, font="helvetica 11")
        self.path_label.grid(row=2, column=1)
        self.path_label.place(relx=0.37, rely=0.38)

        self.entry_label = ttk.Label(self.window, text="Пароль:", font="helvetica 11")
        self.entry_label.grid(row=3, column=0)
        self.entry_label.place(relx=0.1, rely=0.5)

        self.entry_label_repeat = ttk.Label(self.window, text="Подтвердить:", font="helvetica 11")
        self.entry_label_repeat.grid(row=4, column=0)
        self.entry_label_repeat.place(relx=0.1, rely=0.63)

        self.entry_pass = ttk.Entry(self.window, textvariable=tk.StringVar(), foreground="#000000",
                                    show="*")
        self.entry_pass.grid(row=2, column=1)
        self.entry_pass.place(relx=0.4, rely=0.5, height=30, width=228)

        self.entry_pass_repeat = ttk.Entry(self.window, textvariable=tk.StringVar(), foreground="#000000",
                                           show="*")
        self.entry_pass_repeat.grid(row=5, column=1)
        self.entry_pass_repeat.place(relx=0.4, rely=0.63, height=30, width=228)

        self.button_open = ttk.Button(self.window, text="Справка", command=Info)
        self.button_open.grid(row=6, column=0)
        self.button_open.place(relx=0.08, rely=0.8, height=30, width=100)

        self.button_open = ttk.Button(self.window, text="Ок", command=self.encrypt)
        self.button_open.grid(row=6, column=1)
        self.button_open.place(relx=0.39, rely=0.8, height=30, width=100)

        self.button_exit = ttk.Button(self.window, text="Отмена", command=self.window.destroy)
        self.button_exit.grid(row=6, column=2)
        self.button_exit.place(relx=0.7, rely=0.8, height=30, width=100)

    def check_file(self):
        filepath = fd.askopenfilename(title='Select a PDF file', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'),))
        if filepath:
            self.path = filepath
            self.pdf_dec_reader = PdfFileReader(self.path)
            self.display_text.set(os.path.basename(self.path))

    def error_message(self):
        if self.pdf_dec_reader.isEncrypted:
            messagebox.showwarning('Ошибка', "Похоже PDF файл уже зашифрован")
        elif self.entry_pass.get() == '':
            messagebox.showwarning('Ошибка', "Пожалуйста, введите пароль")
        elif self.entry_pass.get() != self.entry_pass_repeat.get():
            messagebox.showwarning('Ошибка', "Пароли не совпадают")
        else:
            return True

    @staticmethod
    def cipher_stream(input_file, password):
        output_file = BytesIO()
        input_file.seek(0)
        pyAesCrypt.encryptStream(input_file, output_file, password, 64 * 1024)
        output_file.seek(0)
        return output_file

    def encrypt(self):
        if self.error_message():
            self.pdf = PdfFileReader(self.path)
            pdfWriter = PdfFileWriter()
            for page in range(self.pdf.getNumPages()):
                pdfWriter.addPage(self.pdf.getPage(page))
            pdfWriter.encrypt(user_password=self.entry_pass.get(), owner_pwd=None, use_128bit=True)
            output_buffer = BytesIO()
            pdfWriter.write(output_buffer)
            self.pdf.stream.close()

            if self.enabled.get() == 1:
                output_buffer = self.cipher_stream(output_buffer, password=self.entry_pass.get())

            with open(self.path, mode='wb') as f:
                f.write(output_buffer.getbuffer())
            f.close()

            messagebox.showinfo('Успех', "PDF файл зашифрован")
            self.window.destroy()
