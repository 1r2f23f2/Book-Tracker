import json
import os
from tkinter import *
from tkinter import ttk, messagebox

DATA_FILE = "books.json"


class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker - Трекер прочитанных книг")
        self.root.geometry("800x500")
        self.root.resizable(True, True)

        # Данные
        self.books = []
        self.load_data()

        # Создание интерфейса
        self.create_input_frame()
        self.create_filter_frame()
        self.create_table_frame()

        # Обновить таблицу
        self.refresh_table()

    def create_input_frame(self):
        """Форма для добавления книги"""
        input_frame = LabelFrame(self.root, text="Добавить новую книгу", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Название
        Label(input_frame, text="Название книги:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Автор
        Label(input_frame, text="Автор:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.author_entry = Entry(input_frame, width=25)
        self.author_entry.grid(row=0, column=3, padx=5, pady=5)

        # Жанр
        Label(input_frame, text="Жанр:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.genre_entry = Entry(input_frame, width=30)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        # Количество страниц
        Label(input_frame, text="Количество страниц:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.pages_entry = Entry(input_frame, width=25)
        self.pages_entry.grid(row=1, column=3, padx=5, pady=5)

        # Кнопка добавления
        self.add_button = Button(input_frame, text="Добавить книгу", command=self.add_book, bg="lightgreen")
        self.add_button.grid(row=2, column=0, columnspan=4, pady=10)

    def create_filter_frame(self):
        """Фильтрация"""
        filter_frame = LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        # Фильтр по жанру
        Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.genre_filter = Entry(filter_frame, width=25)
        self.genre_filter.grid(row=0, column=1, padx=5, pady=5)

        # Фильтр по страницам
        Label(filter_frame, text="Количество страниц >").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.pages_filter = Entry(filter_frame, width=10)
        self.pages_filter.grid(row=0, column=3, padx=5, pady=5)

        # Кнопка применения фильтра
        self.filter_button = Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        self.filter_button.grid(row=0, column=4, padx=10, pady=5)

        # Кнопка сброса фильтра
        self.reset_button = Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter)
        self.reset_button.grid(row=0, column=5, padx=10, pady=5)

    def create_table_frame(self):
        """Таблица с книгами"""
        self.table_frame = Frame(self.root)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Создание Treeview
        columns = ("Название", "Автор", "Жанр", "Страницы")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        # Определение заголовков
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)

        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(self.table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=LEFT, fill="both", expand=True)
        scrollbar.pack(side=RIGHT, fill="y")

    def add_book(self):
        """Добавление книги с проверкой ввода"""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        # Проверка на пустые поля
        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        # Проверка, что страницы - число
        try:
            pages = int(pages)
            if pages <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
            return

        # Добавление книги
        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        }
        self.books.append(book)
        self.save_data()

        # Очистка полей
        self.title_entry.delete(0, END)
        self.author_entry.delete(0, END)
        self.genre_entry.delete(0, END)
        self.pages_entry.delete(0, END)

        # Обновление таблицы
        self.refresh_table()
        messagebox.showinfo("Успех", f"Книга '{title}' добавлена!")

    def apply_filter(self):
        """Применение фильтров"""
        genre_filter = self.genre_filter.get().strip().lower()
        pages_filter = self.pages_filter.get().strip()

        filtered_books = self.books.copy()

        # Фильтр по жанру
        if genre_filter:
            filtered_books = [book for book in filtered_books if genre_filter in book["genre"].lower()]

        # Фильтр по страницам
        if pages_filter:
            try:
                pages_threshold = int(pages_filter)
                filtered_books = [book for book in filtered_books if book["pages"] > pages_threshold]
            except ValueError:
                messagebox.showerror("Ошибка", "Фильтр по страницам должен быть числом!")

        self.display_books(filtered_books)

    def reset_filter(self):
        """Сброс фильтров"""
        self.genre_filter.delete(0, END)
        self.pages_filter.delete(0, END)
        self.refresh_table()

    def refresh_table(self):
        """Обновление таблицы без фильтров"""
        self.display_books(self.books)

    def display_books(self, books_list):
        """Отображение книг в таблице"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполнение таблицы
        for book in books_list:
            self.tree.insert("", END, values=(book["title"], book["author"], book["genre"], book["pages"]))

    def save_data(self):
        """Сохранение данных в JSON"""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

    def load_data(self):
        """Загрузка данных из JSON"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.books = json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
                self.books = []
        else:
            self.books = []


if __name__ == "__main__":
    root = Tk()
    app = BookTracker(root)
    root.mainloop()