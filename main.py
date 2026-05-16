import json
import os
from datetime import datetime
from typing import List, Dict, Any

DATA_FILE = "books.json"

def load_books() -> List[Dict[str, Any]]:
    """Загрузка книг из JSON файла"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_books(books: List[Dict[str, Any]]) -> None:
    """Сохранение книг в JSON файл"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

def is_duplicate(books: List[Dict[str, Any]], author: str, title: str) -> bool:
    """Проверка на дубликаты по автору и названию"""
    return any(book['author'].lower() == author.lower() 
               and book['title'].lower() == title.lower() 
               for book in books)

def add_book(books: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Добавление новой книги"""
    print("\n--- Добавление книги ---")
    
    author = input("Введите автора: ").strip()
    if not author:
        print("Ошибка: автор не может быть пустым")
        return books
    
    title = input("Введите название: ").strip()
    if not title:
        print("Ошибка: название не может быть пустым")
        return books
    
    # Проверка на дубликаты
    if is_duplicate(books, author, title):
        print(f"Ошибка: книга '{title}' автора '{author}' уже существует")
        return books
    
    try:
        rating = int(input("Введите оценку (1-5): "))
        if rating < 1 or rating > 5:
            print("Ошибка: оценка должна быть от 1 до 5")
            return books
    except ValueError:
        print("Ошибка: введите целое число")
        return books
    
    date = input("Введите дату прочтения (ГГГГ-ММ-ДД): ").strip()
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Ошибка: неверный формат даты. Используйте ГГГГ-ММ-ДД")
        return books
    
    book = {
        "author": author,
        "title": title,
        "rating": rating,
        "date": date
    }
    
    books.append(book)
    save_books(books)
    print(f"Книга '{title}' успешно добавлена")
    return books

def list_books(books: List[Dict[str, Any]]) -> None:
    """Вывод всех книг"""
    print("\n--- Список всех книг ---")
    if not books:
        print("Нет добавленных книг")
        return
    
    for i, book in enumerate(books, 1):
        print(f"{i}. \"{book['title']}\" - {book['author']} | "
              f"Оценка: {book['rating']}/5 | Прочитано: {book['date']}")

def show_average_rating(books: List[Dict[str, Any]]) -> None:
    """Вывод средней оценки"""
    print("\n--- Средняя оценка ---")
    if not books:
        print("Нет книг для расчёта средней оценки")
        return
    
    total = sum(book['rating'] for book in books)
    average = total / len(books)
    print(f"Средняя оценка по {len(books)} книгам: {average:.2f}")

def stats_by_author(books: List[Dict[str, Any]]) -> None:
    """Статистика по авторам"""
    print("\n--- Статистика по авторам ---")
    if not books:
        print("Нет книг для статистики")
        return
    
    author_stats = {}
    for book in books:
        author = book['author']
        author_stats[author] = author_stats.get(author, 0) + 1
    
    for author, count in sorted(author_stats.items()):
        print(f"{author}: {count} книга(и)")

def delete_book(books: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Удаление книги"""
    print("\n--- Удаление книги ---")
    if not books:
        print("Нет книг для удаления")
        return books
    
    print("Способы удаления:")
    print("1. Удалить по индексу")
    print("2. Удалить по автору и названию")
    
    choice = input("Выберите способ (1-2): ").strip()
    
    if choice == '1':
        try:
            index = int(input("Введите номер книги для удаления: "))
            if 1 <= index <= len(books):
                removed = books.pop(index - 1)
                save_books(books)
                print(f"Книга '{removed['title']}' удалена")
            else:
                print(f"Ошибка: номер должен быть от 1 до {len(books)}")
        except ValueError:
            print("Ошибка: введите число")
    
    elif choice == '2':
        author = input("Введите автора: ").strip()
        title = input("Введите название: ").strip()
        
        initial_len = len(books)
        books = [book for book in books 
                 if not (book['author'].lower() == author.lower() 
                         and book['title'].lower() == title.lower())]
        
        if len(books) < initial_len:
            save_books(books)
            print(f"Книга '{title}' автора '{author}' удалена")
        else:
            print("Книга не найдена")
    
    else:
        print("Неверный выбор")
    
    return books

def main():
    """Главное меню приложения"""
    books = load_books()
    
    while True:
        print("\n" + "="*40)
        print("ТРЕКЕР ПРОЧИТАННЫХ КНИГ")
        print("="*40)
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Показать среднюю оценку")
        print("4. Статистика по авторам")
        print("5. Удалить книгу")
        print("6. Выход")
        print("-"*40)
        
        choice = input("Выберите действие (1-6): ").strip()
        
        if choice == '1':
            books = add_book(books)
        elif choice == '2':
            list_books(books)
        elif choice == '3':
            show_average_rating(books)
        elif choice == '4':
            stats_by_author(books)
        elif choice == '5':
            books = delete_book(books)
        elif choice == '6':
            print("\nДо свидания")
            break
        else:
            print("Ошибка: выберите пункт от 1 до 6")
        
        input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    main()
