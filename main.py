import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker — Трекер прочитанных книг")
        self.root.geometry("800x600")
        
        self.db_file = "books_data.json"
        self.books = []
        
        self.init_ui()
        self.load_from_json()

    def init_ui(self):
        # --- 1. ФОРМА ВВОДА (Пункт 1 задания) ---
        input_frame = tk.LabelFrame(self.root, text="Добавить новую книгу", padx=15, pady=10)
        input_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(input_frame, text="Название книги:").grid(row=0, column=0, sticky="w")
        self.ent_title = tk.Entry(input_frame, width=30)
        self.ent_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Автор:").grid(row=0, column=2, sticky="w", padx=(20, 0))
        self.ent_author = tk.Entry(input_frame, width=30)
        self.ent_author.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Жанр:").grid(row=1, column=0, sticky="w")
        self.ent_genre = tk.Entry(input_frame, width=30)
        self.ent_genre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Кол-во страниц:").grid(row=1, column=2, sticky="w", padx=(20, 0))
        self.ent_pages = tk.Entry(input_frame, width=30)
        self.ent_pages.grid(row=1, column=3, padx=5, pady=5)

        # Кнопка добавить (Пункт 2 задания)
        self.btn_add = tk.Button(input_frame, text="Добавить книгу", command=self.add_book, 
                                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_add.grid(row=2, column=0, columnspan=4, pady=10, sticky="we")

        # --- 2. ФИЛЬТРАЦИЯ (Пункт 3 задания) ---
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация списка", padx=15, pady=10)
        filter_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(filter_frame, text="Жанр:").grid(row=0, column=0)
        self.flt_genre = tk.Entry(filter_frame, width=15)
        self.flt_genre.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Мин. страниц:").grid(row=0, column=2, padx=(10, 0))
        self.flt_pages = tk.Entry(filter_frame, width=10)
        self.flt_pages.grid(row=0, column=3, padx=5)

        tk.Button(filter_frame, text="Применить фильтр", command=self.refresh_table).grid(row=0, column=4, padx=10)


tk.Button(filter_frame, text="Сброс", command=self.reset_filters).grid(row=0, column=5)

        # --- 3. ТАБЛИЦА ВЫВОДА (Пункт 2 задания) ---
        cols = ("title", "author", "genre", "pages")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страниц")
        
        self.tree.column("pages", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=15)

    # 4. ВАЛИДАЦИЯ (Пункт 5 задания)
    def add_book(self):
        title = self.ent_title.get().strip()
        author = self.ent_author.get().strip()
        genre = self.ent_genre.get().strip()
        pages_raw = self.ent_pages.get().strip()

        # Поля не должны быть пустыми
        if not all([title, author, genre, pages_raw]):
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        # Кол-во страниц должно быть числом
        try:
            pages = int(pages_raw)
            if pages <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть целым положительным числом!")
            return

        book = {"title": title, "author": author, "genre": genre, "pages": pages}
        self.books.append(book)
        self.save_to_json()
        self.refresh_table()
        self.clear_fields()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        g_filter = self.flt_genre.get().lower()
        p_filter = self.flt_pages.get().strip()

        for b in self.books:
            # Логика фильтрации
            if g_filter and g_filter not in b['genre'].lower():
                continue
            if p_filter and b['pages'] < int(p_filter if p_filter.isdigit() else 0):
                continue
            
            self.tree.insert("", "end", values=(b['title'], b['author'], b['genre'], b['pages']))

    def reset_filters(self):
        self.flt_genre.delete(0, tk.END)
        self.flt_pages.delete(0, tk.END)
        self.refresh_table()

    def clear_fields(self):
        self.ent_title.delete(0, tk.END)
        self.ent_author.delete(0, tk.END)
        self.ent_genre.delete(0, tk.END)
        self.ent_pages.delete(0, tk.END)

    # 5. JSON (Пункт 4 задания)
    def save_to_json(self):
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_from_json(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r", encoding="utf-8") as f:
                self.books = json.load(f)
            self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()




