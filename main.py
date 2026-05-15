import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("950x600")
        self.root.resizable(False, False)

        self.books = []

        # =========================
        # ПОЛЯ ВВОДА
        # =========================
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Название книги:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Автор:").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = tk.Entry(input_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=5)

        tk.Label(input_frame, text="Жанр:").grid(row=2, column=0, padx=5, pady=5)
        self.genre_entry = tk.Entry(input_frame, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5)

        tk.Label(input_frame, text="Количество страниц:").grid(row=3, column=0, padx=5, pady=5)
        self.pages_entry = tk.Entry(input_frame, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5)

        # =========================
        # КНОПКИ
        # =========================
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        add_button = tk.Button(
            button_frame,
            text="Добавить книгу",
            command=self.add_book,
            bg="#4CAF50",
            fg="white",
            width=20
        )
        add_button.grid(row=0, column=0, padx=5)

        save_button = tk.Button(
            button_frame,
            text="Сохранить в JSON",
            command=self.save_books,
            bg="#2196F3",
            fg="white",
            width=20
        )
        save_button.grid(row=0, column=1, padx=5)

        load_button = tk.Button(
            button_frame,
            text="Загрузить из JSON",
            command=self.load_books,
            bg="#FF9800",
            fg="white",
            width=20
        )
        load_button.grid(row=0, column=2, padx=5)

        # =========================
        # ФИЛЬТРЫ
        # =========================
        filter_frame = tk.LabelFrame(root, text="Фильтрация")
        filter_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, padx=5, pady=5)

        self.genre_filter = tk.Entry(filter_frame, width=20)
        self.genre_filter.grid(row=0, column=1, padx=5)

        genre_button = tk.Button(
            filter_frame,
            text="Фильтр по жанру",
            command=self.filter_by_genre
        )
        genre_button.grid(row=0, column=2, padx=5)

        tk.Label(filter_frame, text="Страниц больше:").grid(row=0, column=3, padx=5)

        self.pages_filter = tk.Entry(filter_frame, width=10)
        self.pages_filter.grid(row=0, column=4, padx=5)

        pages_button = tk.Button(
            filter_frame,
            text="Фильтр по страницам",
            command=self.filter_by_pages
        )
        pages_button.grid(row=0, column=5, padx=5)

        show_all_button = tk.Button(
            filter_frame,
            text="Показать все",
            command=self.show_all_books
        )
        show_all_button.grid(row=0, column=6, padx=5)

        # =========================
        # ТАБЛИЦА
        # =========================
        columns = ("title", "author", "genre", "pages")

        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=18)

        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страницы")

        self.tree.column("title", width=250)
        self.tree.column("author", width=200)
        self.tree.column("genre", width=150)
        self.tree.column("pages", width=100)

        self.tree.pack(padx=10, pady=10)

        self.load_books()

    # =========================
    # ДОБАВЛЕНИЕ КНИГИ
    # =========================
    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        # Проверка пустых полей
        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        # Проверка числа страниц
        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }

        self.books.append(book)

        self.tree.insert(
            "",
            tk.END,
            values=(title, author, genre, pages)
        )

        self.clear_entries()

    # =========================
    # ОЧИСТКА ПОЛЕЙ
    # =========================
    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

    # =========================
    # ОБНОВЛЕНИЕ ТАБЛИЦЫ
    # =========================
    def update_table(self, books_list):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for book in books_list:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    book["title"],
                    book["author"],
                    book["genre"],
                    book["pages"]
                )
            )

    # =========================
    # ФИЛЬТР ПО ЖАНРУ
    # =========================
    def filter_by_genre(self):
        genre = self.genre_filter.get().strip().lower()

        filtered = [
            book for book in self.books
            if genre in book["genre"].lower()
        ]

        self.update_table(filtered)

    # =========================
    # ФИЛЬТР ПО СТРАНИЦАМ
    # =========================
    def filter_by_pages(self):
        pages = self.pages_filter.get().strip()

        if not pages.isdigit():
            messagebox.showerror(
                "Ошибка",
                "Введите корректное число страниц!"
            )
            return

        pages = int(pages)

        filtered = [
            book for book in self.books
            if book["pages"] > pages
        ]

        self.update_table(filtered)

    # =========================
    # ПОКАЗАТЬ ВСЕ
    # =========================
    def show_all_books(self):
        self.update_table(self.books)

    # =========================
    # СОХРАНЕНИЕ В JSON
    # =========================
    def save_books(self):
        with open("books.json", "w", encoding="utf-8") as file:
            json.dump(self.books, file, ensure_ascii=False, indent=4)

        messagebox.showinfo(
            "Успех",
            "Данные успешно сохранены!"
        )

    # =========================
    # ЗАГРУЗКА ИЗ JSON
    # =========================
    def load_books(self):
        if os.path.exists("books.json"):
            with open("books.json", "r", encoding="utf-8") as file:
                try:
                    self.books = json.load(file)
                except json.JSONDecodeError:
                    self.books = []

        self.update_table(self.books)

# =========================
# ЗАПУСК ПРОГРАММЫ
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
