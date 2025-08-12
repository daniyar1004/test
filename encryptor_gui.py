"""
Encryptor GUI (Windows / Linux)

- Выбор файла
- Шифрование/дешифрование XOR с паролем
- Сохранение в .encx формат
- GUI на Tkinter с базовыми элементами
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

CHUNK_SIZE = 64 * 1024

# Простой XOR-алгоритм
def xor_encrypt(data, key):
    key_bytes = key.encode('utf-8')
    return bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])

def encrypt_file(in_path, out_path, password, progress_callback=None):
    total = os.path.getsize(in_path)
    processed = 0
    with open(in_path, 'rb') as fin, open(out_path, 'wb') as fout:
        while True:
            chunk = fin.read(CHUNK_SIZE)
            if not chunk:
                break
            enc_chunk = xor_encrypt(chunk, password)
            fout.write(enc_chunk)
            processed += len(chunk)
            if progress_callback:
                progress_callback(processed, total)

def decrypt_file(in_path, out_path, password, progress_callback=None):
    total = os.path.getsize(in_path)
    processed = 0
    with open(in_path, 'rb') as fin, open(out_path, 'wb') as fout:
        while True:
            chunk = fin.read(CHUNK_SIZE)
            if not chunk:
                break
            dec_chunk = xor_encrypt(chunk, password)
            fout.write(dec_chunk)
            processed += len(chunk)
            if progress_callback:
                progress_callback(processed, total)

class EncryptorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Учебный шифратор файлов')
        self.geometry('640x300')
        self.resizable(False, False)

        self.file_path = None

        frm = ttk.Frame(self, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)

        # File selection
        file_row = ttk.Frame(frm)
        file_row.pack(fill=tk.X, pady=6)
        ttk.Label(file_row, text='Файл:').pack(side=tk.LEFT)
        self.file_label = ttk.Label(file_row, text='(не выбран)', width=60)
        self.file_label.pack(side=tk.LEFT, padx=8)
        ttk.Button(file_row, text='Выбрать...', command=self.choose_file).pack(side=tk.RIGHT)

        # Password
        pass_row = ttk.Frame(frm)
        pass_row.pack(fill=tk.X, pady=6)
        ttk.Label(pass_row, text='Пароль:').pack(side=tk.LEFT)
        self.pass_entry = ttk.Entry(pass_row, show='*', width=40)
        self.pass_entry.pack(side=tk.LEFT, padx=8)

        # Buttons
        btn_row = ttk.Frame(frm)
        btn_row.pack(fill=tk.X, pady=12)
        ttk.Button(btn_row, text='Зашифровать', command=self.encrypt_action).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_row, text='Расшифровать', command=self.decrypt_action).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_row, text='Выход', command=self.quit).pack(side=tk.RIGHT)

        # Progress
        prog_row = ttk.Frame(frm)
        prog_row.pack(fill=tk.X, pady=6)
        self.progress = ttk.Progressbar(prog_row, orient='horizontal', length=520, mode='determinate')
        self.progress.pack(side=tk.LEFT, padx=4)
        self.progress_label = ttk.Label(prog_row, text='0%')
        self.progress_label.pack(side=tk.LEFT, padx=6)

        # Log
        log_row = ttk.Frame(frm)
        log_row.pack(fill=tk.BOTH, expand=True, pady=6)
        self.log = tk.Text(log_row, height=6, state='disabled')
        self.log.pack(fill=tk.BOTH, expand=True)

    def log_msg(self, text):
        self.log.configure(state='normal')
        self.log.insert('end', text + '\n')
        self.log.see('end')
        self.log.configure(state='disabled')

    def choose_file(self):
        p = filedialog.askopenfilename()
        if p:
            self.file_path = p
            self.file_label.config(text=p)
            self.log_msg(f'Выбран файл: {p}')

    def set_progress(self, processed, total):
        pct = int(processed / total * 100) if total else 0
        self.progress['value'] = pct
        self.progress_label.config(text=f'{pct}%')
        self.update_idletasks()

    def encrypt_action(self):
        if not self.file_path:
            messagebox.showwarning('Ошибка', 'Файл не выбран')
            return
        password = self.pass_entry.get()
        if not password:
            messagebox.showwarning('Ошибка', 'Введите пароль')
            return
        out_path = filedialog.asksaveasfilename(defaultextension='.encx')
        if not out_path:
            return
        self.log_msg('Начало шифрования...')
        encrypt_file(self.file_path, out_path, password, progress_callback=self.set_progress)
        self.log_msg(f'Файл записан: {out_path}')
        messagebox.showinfo('Готово', 'Шифрование завершено')

    def decrypt_action(self):
        if not self.file_path:
            messagebox.showwarning('Ошибка', 'Файл не выбран')
            return
        password = self.pass_entry.get()
        if not password:
            messagebox.showwarning('Ошибка', 'Введите пароль')
            return
        out_path = filedialog.asksaveasfilename()
        if not out_path:
            return
        self.log_msg('Начало расшифровки...')
        decrypt_file(self.file_path, out_path, password, progress_callback=self.set_progress)
        self.log_msg(f'Файл расшифрован: {out_path}')
        messagebox.showinfo('Готово', 'Расшифровка завершена')

if __name__ == '__main__':
    app = EncryptorApp()
    app.mainloop()
