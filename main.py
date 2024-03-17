from tkinter import *
from viewer import Viewer

if __name__ == '__main__':
    root = Tk()
    app = Viewer(root)
    root.mainloop()



# import pyAesCrypt
# import os
#
#
# # Функция для шифрования PDF
# def encrypt_pdf(input_file, output_file, password):
#     bufferSize = 64 * 1024
#     try:
#         with open(input_file, "rb") as fIn:
#             with open(output_file, "wb") as fOut:
#                 pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)
#         os.remove(input_file)  # Удаление исходного файла после шифрования
#         print("Файл успешно зашифрован")
#     except Exception as e:
#         print("Ошибка при шифровании файла:", str(e))
#
#
# def decrypt_file(input_file, output_file, password):
#     bufferSize = 64 * 1024
#     try:
#         with open(input_file, "rb") as encrypted_file:
#             with open(output_file, "wb") as decrypted_file:
#                 pyAesCrypt.decryptStream(encrypted_file, decrypted_file, password, bufferSize)
#         print("Файл успешно дешифрован.")
#     except Exception as e:
#         print(f"Ошибка при дешифровании файла: {str(e)}")
#
#
# # Задайте пути к исходному и выходному файлам, а также пароль
# input_file = "test_1.pdf"
# output_file = "encrypted.pdf"
# password = "1234"
#
# # Вызов функции для шифрования PDF
# # encrypt_pdf(input_file, output_file, password)
# decrypt_file(output_file, "decrypted.pdf", "1234")

# import PyPDF4
#
#
# def read_protected_pdf(file_path, password):
#     with open(file_path, 'rb') as file:
#         pdf = PyPDF4.PdfFileReader(file, strict=False)
#         if pdf.isEncrypted:
#             pdf.decrypt(password)
#             print("+")
#         num_pages = len(pdf.pages)
#         for page_num in range(num_pages):
#             page = pdf.pages[page_num]
#             text = page.extractText()
#             print(text)
#
#
# # Пример вызова функции
# pdf_file_path = 'пароль.pdf'
# pdf_password = '1234'
# read_protected_pdf(pdf_file_path, pdf_password)
