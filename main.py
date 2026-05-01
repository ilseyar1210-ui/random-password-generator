import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime

# ===== КОНСТАНТЫ =====
HISTORY_FILE = "passwords_history.json"
MIN_LENGTH = 4
MAX_LENGTH = 32
DEFAULT_LENGTH = 12

class RandomPasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.history = self.load_history()

        self.create_widgets()
        self.update_history_display()

    # ===== РАБОТА С JSON =====
    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_history(self):
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

    # ===== ГЕНЕРАЦИЯ ПАРОЛЯ =====
    def generate_password(self):
        length = self.length_var.get()
        use_uppercase = self.uppercase_var.get()
        use_lowercase = self.lowercase_var.get()
        use_digits = self.digits_var.get()
        use_symbols = self.symbols_var.get()

        # Проверка: выбран хотя бы один тип символов
        if not any([use_uppercase, use_lowercase, use_digits, use_symbols]):
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
            return

        # Формируем набор символов
        characters = ""
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_lowercase:
            characters += string.ascii_lowercase
        if use_digits:
            characters += string.digits
        if use_symbols:
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        # Генерация пароля
        password = ''.join(random.choice(characters) for _ in range(length))

        # Отображаем пароль
        self.password_display.config(state="normal")
        self.password_display.delete(1.0, tk.END)
        self.password_display.insert(1.0, password)
        self.password_display.config(state="disabled")

        # Копируем в буфер обмена
        self.root.clipboard_clear()
        self.root.clipboard_append(password)

        # Сохраняем в историю
        history_record = {
            "password": password,
            "length": length,
            "uppercase": use_uppercase,
            "lowercase": use_lowercase,
            "digits": use_digits,
            "symbols": use_symbols,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(history_record)
        self.save_history()
        self.update_history_display()

        messagebox.showinfo("Успех", "Пароль сгенерирован и скопирован в буфер обмена!")

    def copy_password(self):
        password = self.password_display.get(1.0, tk.END).strip()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")

    # ===== ИНТЕРФЕЙС =====
    def create_widgets(self):
        # Рамка генерации
        gen_frame = ttk.LabelFrame(self.root, text="🔐 Настройки пароля", padding=10)
        gen_frame.pack(fill="x", padx=10, pady=5)

        # Длина пароля
        ttk.Label(gen_frame, text="Длина пароля:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.length_var = tk.IntVar(value=DEFAULT_LENGTH)
        self.length_slider = ttk.Scale(gen_frame, from_=MIN_LENGTH, to=MAX_LENGTH, 
                                        orient="horizontal", variable=self.length_var, 
                                        command=self.update_length_label)
        self.length_slider.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.length_label = ttk.Label(gen_frame, text=f"{DEFAULT_LENGTH}")
        self.length_label.grid(row=0, column=2, padx=5, pady=5)

        # Чекбоксы
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(gen_frame, text="ABC - Заглавные буквы", variable=self.uppercase_var).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Checkbutton(gen_frame, text="abc - Строчные буквы", variable=self.lowercase_var).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Checkbutton(gen_frame, text="123 - Цифры", variable=self.digits_var).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Checkbutton(gen_frame, text="!@# - Спецсимволы", variable=self.symbols_var).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Кнопки
        btn_frame = ttk.Frame(gen_frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=10)

        self.generate_btn = ttk.Button(btn_frame, text="✨ Сгенерировать пароль", command=self.generate_password)
        self.generate_btn.pack(side="left", padx=5)

        self.copy_btn = ttk.Button(btn_frame, text="📋 Копировать", command=self.copy_password)
        self.copy_btn.pack(side="left", padx=5)

        # Отображение пароля
        ttk.Label(gen_frame, text="Сгенерированный пароль:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.password_display = tk.Text(gen_frame, height=3, width=50, font=("Courier", 12), 
                                         wrap="word", relief="sunken", borderwidth=1)
        self.password_display.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.password_display.config(state="disabled")

        # Рамка истории
        history_frame = ttk.LabelFrame(self.root, text="📜 История паролей", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Таблица истории
        columns = ("№", "Дата", "Пароль", "Длина", "Символы")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=10)
        
        self.tree.heading("№", text="№")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Пароль", text="Пароль")
        self.tree.heading("Длина", text="Длина")
        self.tree.heading("Символы", text="Символы")

        self.tree.column("№", width=40)
        self.tree.column("Дата", width=150)
        self.tree.column("Пароль", width=250)
        self.tree.column("Длина", width=60)
        self.tree.column("Символы", width=200)

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Привязка двойного клика для копирования
        self.tree.bind("<Double-1>", self.copy_from_history)

        # Кнопки управления
        btn_frame2 = ttk.Frame(self.root)
        btn_frame2.pack(fill="x", padx=10, pady=10)

        self.delete_btn = ttk.Button(btn_frame2, text="❌ Удалить выбранный", command=self.delete_selected)
        self.delete_btn.pack(side="left", padx=5)

        self.clear_btn = ttk.Button(btn_frame2, text="🗑 Очистить историю", command=self.clear_history)
        self.clear_btn.pack(side="left", padx=5)

    def update_length_label(self, value):
        self.length_label.config(text=str(int(float(value))))

    # ===== ОТОБРАЖЕНИЕ ИСТОРИИ =====
    def update_history_display(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for idx, record in enumerate(reversed(self.history), 1):
            chars = []
            if record.get("uppercase", True):
                chars.append("ABC")
            if record.get("lowercase", True):
                chars.append("abc")
            if record.get("digits", True):
                chars.append("123")
            if record.get("symbols", False):
                chars.append("!@#")
            chars_str = ", ".join(chars)

            self.tree.insert("", "end", values=(
                idx,
                record["timestamp"],
                record["password"],
                record["length"],
                chars_str
            ))

    # ===== УДАЛЕНИЕ =====
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите запись для удаления")
            return

        item = self.tree.item(selected[0])
        timestamp = item["values"][1]
        password = item["values"][2]

        for i, record in enumerate(self.history):
            if record["timestamp"] == timestamp and record["password"] == password:
                del self.history[i]
                break

        self.save_history()
        self.update_history_display()
        messagebox.showinfo("Успех", "Запись удалена")

    def clear_history(self):
        if not self.history:
            messagebox.showinfo("Инфо", "История уже пуста")
            return
        if messagebox.askyesno("Подтверждение", "Очистить всю историю паролей?"):
            self.history.clear()
            self.save_history()
            self.update_history_display()
            messagebox.showinfo("Успех", "История очищена")

    def copy_from_history(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        password = item["values"][2]
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo("Успех", f"Пароль скопирован в буфер обмена!")


if __name__ == "__main__":
    root = tk.Tk()
    app = RandomPasswordGenerator(root)
    root.mainloop()
