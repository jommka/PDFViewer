from io import BytesIO
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from PyPDF4 import PdfFileReader, PdfFileWriter


class Decrypt:
    def __init__(self, pdf_dec_reader, path):
        self.path = path
        self.pdf_dec_reader = pdf_dec_reader
        self.window = Toplevel()
        self.window.geometry('420x350+440+180')
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

        self.label = ttk.Label(self.window, text="Введите пароль", font="helvetica 18")
        self.label.grid(row=0, column=0)
        self.label.place(relx=0.05, rely=0.08)

        self.entry_label = ttk.Label(self.window, text="Этот файл защищен паролем. Введите пароль для",
                                     font="helvetica 11")
        self.entry_label.grid(row=1, column=0)
        self.entry_label.place(relx=0.05, rely=0.3)

        self.entry_label = ttk.Label(self.window, text="открытия файла.",
                                     font="helvetica 11")
        self.entry_label.grid(row=2, column=0)
        self.entry_label.place(relx=0.05, rely=0.4)

        self.entry_pass = ttk.Entry(self.window, textvariable=tk.StringVar(), foreground="#000000",
                                    show="*")
        self.entry_pass.grid(row=3, column=0)
        self.entry_pass.place(relx=0.07, rely=0.55, height=35, width=345)

        self.button_open = ttk.Button(self.window, text="Открыть файл", command=self.decrypt_file)
        self.button_open.grid(row=4, column=0)
        self.button_open.place(relx=0.07, rely=0.73, height=35, width=150)

        self.button_exit = ttk.Button(self.window, text="Отмена", command=self.window.destroy)
        self.button_exit.grid(row=4, column=1)
        self.button_exit.place(relx=0.55, rely=0.73, height=35, width=150)

    def error_message(self):
        if self.entry_pass.get() == '':
            messagebox.showwarning('Ошибка', "Пожалуйста, введите пароль")
        else:
            return True

    def decrypt_file(self):
        if self.error_message():
            self.pdf_dec_reader.decrypt(password=self.entry_pass.get())
            writer = PdfFileWriter()
            for page in range(self.pdf_dec_reader.getNumPages()):
                writer.addPage(self.pdf_dec_reader.getPage(page))

            output_buffer = BytesIO()
            writer.write(output_buffer)
            self.pdf_dec_reader.stream.close()

            with open(self.path, mode='wb') as f:
                f.write(output_buffer.getbuffer())
            f.close()
            #
            # messagebox.showinfo('Успех', "PDF файл расшифрован")


