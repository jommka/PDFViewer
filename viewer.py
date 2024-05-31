import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from PyPDF4 import PdfFileReader

from miner import PDFMiner
from encryption.decrypt import Decrypt
from encryption.encrypt import Encrypt
from hide_info.hiding import Hiding


class Viewer:
    def __init__(self, master):
        self.path = None
        self.file_open = None
        self.author = None
        self.name = None
        self.current_page = 0
        self.numPages = None
        self.pdf_dec_reader = None

        self.master = master
        self.master.title('PDF Viewer')
        self.master.geometry('580x520+440+180')
        self.master.resizable(width=0, height=0)
        self.master.iconbitmap(self.master, r'D:\Диплом\PDF Viewer\icons\icon.ico')

        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.filemenu_open = Menu(self.menu)
        self.filemenu_protect = Menu(self.menu)
        self.menu.add_cascade(label="Файл", menu=self.filemenu_open)
        self.filemenu_open.add_command(label="Открыть файл", command=self.check_file)
        self.filemenu_open.add_command(label="Открыть файл с AES256-CBC", command=self.check_file_cbc)
        self.filemenu_open.add_command(label="Выйти", command=self.master.destroy)
        self.menu.add_cascade(label="Защита", menu=self.filemenu_protect)
        self.filemenu_protect.add_command(label="Шифрование", command=Encrypt)
        self.filemenu_protect.add_command(label="Скрытие информации", command=Hiding)

        self.top_frame = ttk.Frame(self.master, width=580, height=460)
        self.top_frame.grid(row=0, column=0)
        self.top_frame.grid_propagate(False)
        self.bottom_frame = ttk.Frame(self.master, width=580, height=50)
        self.bottom_frame.grid(row=1, column=0)
        self.bottom_frame.grid_propagate(False)

        self.scrolly = Scrollbar(self.top_frame, orient=VERTICAL)
        self.scrolly.grid(row=0, column=1, sticky=(N,S))
        self.scrollx = Scrollbar(self.top_frame, orient=HORIZONTAL)
        self.scrollx.grid(row=1, column=0, sticky=(W, E))

        self.output = Canvas(self.top_frame, bg='#ECE8F3', width=560, height=435)
        self.output.configure(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        self.output.grid(row=0, column=0)
        self.scrolly.configure(command=self.output.yview)
        self.scrollx.configure(command=self.output.xview)

        self.uparrow_icon = PhotoImage(file=r'icons/up.png')
        self.downarrow_icon = PhotoImage(file=r'icons/down.png')
        self.uparrow = self.uparrow_icon.subsample(3, 3)
        self.downarrow = self.downarrow_icon.subsample(3, 3)
        self.upbutton = ttk.Button(self.bottom_frame, image=self.uparrow, command=self.previous_page)
        self.upbutton.grid(row=0, column=1, padx=(270, 5), pady=8)
        self.downbutton = ttk.Button(self.bottom_frame, image=self.downarrow, command=self.next_page)
        self.downbutton.grid(row=0, column=3, pady=8)
        self.page_label = ttk.Label(self.bottom_frame, text='страница')
        self.page_label.grid(row=0, column=4, padx=5)
        #
        # keyboard.add_hotkey("win + shift + s", lambda: None, suppress=True)
        # keyboard.add_hotkey("PrtScn", lambda: None, suppress=True)

    def check_file(self):
        filepath = fd.askopenfilename(title='Выберите PDF-файл', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'),))
        if filepath:
            self.path = filepath
            # pdf_dec_reader = PdfFileReader(self.path)
            pdf_dec_reader = PdfFileReader(open(self.path, 'rb'), strict=False)
            if pdf_dec_reader.isEncrypted:
                Decrypt(pdf_dec_reader, self.path, 1)
            else:
                self.open_file()

    def check_file_cbc(self):
        filepath = fd.askopenfilename(title='Выберите PDF-файл', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'),))
        if filepath:
            self.path = filepath
            Decrypt(None, self.path, 2)

    def open_file(self):
        filename = os.path.basename(self.path)
        self.miner = PDFMiner(self.path, newfilepath=None)
        data, numPages = self.miner.get_metadata()
        self.current_page = 0
        if numPages:
            self.name = data.get('заглавие', filename[:-4])
            self.author = data.get('автор', None)
            self.numPages = numPages
            self.file_open = True
            self.display_page()
            self.master.title(self.name)

    def display_page(self):
        if 0 <= self.current_page < self.numPages:
            self.img_file = self.miner.get_page(self.current_page)
            self.output.create_image(0, 0, anchor='nw', image=self.img_file)
            self.stringified_current_page = self.current_page + 1
            self.page_label['text'] = str(self.stringified_current_page) + ' из ' + str(self.numPages)
            region = self.output.bbox(ALL)
            self.output.configure(scrollregion=region)

    def next_page(self):
        if self.file_open:
            if self.current_page <= self.numPages - 1:
                self.current_page += 1
                self.display_page()

    def previous_page(self):
        if self.file_open:
            if self.current_page > 0:
                self.current_page -= 1
                self.display_page()



