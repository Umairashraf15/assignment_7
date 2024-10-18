from typing import List, Optional
import os

# Base User class
class User:
    def __init__(self, user_id: int, name: str, email: str):
        self._user_id = user_id
        self._name = name
        self._email = email

    def display_info(self) -> None:
        print(f"User ID: {self._user_id}, Name: {self._name}, Email: {self._email}")


# Librarian class inheriting from User
class Librarian(User):
    def __init__(self, user_id: int, name: str, email: str):
        super().__init__(user_id, name, email)

    def manage_books(self, library_manager, book, action: str) -> None:
        if action == 'add':
            library_manager.add_book(book)
        elif action == 'update':
            library_manager.update_book(book)
        elif action == 'delete':
            library_manager.delete_book(book)


# Member class inheriting from User
class Member(User):
    def __init__(self, user_id: int, name: str, email: str):
        super().__init__(user_id, name, email)

    def borrow_book(self, library_manager, book_id: int) -> None:
        library_manager.borrow_book(book_id, self._user_id)

    def return_book(self, library_manager, book_id: int) -> None:
        library_manager.return_book(book_id, self._user_id)


# Book class
class Book:
    def __init__(self, book_id: int, title: str, author: str, available: bool = True):
        self._book_id = book_id
        self._title = title
        self._author = author
        self._available = available

    def display_info(self) -> None:
        availability = 'Available' if self._available else 'Unavailable'
        print(f"Book ID: {self._book_id}, Title: {self._title}, Author: {self._author}, Status: {availability}")

    def is_available(self) -> bool:
        return self._available

    def mark_as_borrowed(self) -> None:
        self._available = False

    def mark_as_returned(self) -> None:
        self._available = True


# LibraryManager class
class LibraryManager:
    def __init__(self):
        self.books: List[Book] = []
        self.users: List[User] = []
        self.books_file = 'books.txt'
        self.users_file = 'users.txt'
        self.load_data()

    # Add book
    def add_book(self, book: Book) -> None:
        self.books.append(book)
        self.save_books()

    # Update book
    def update_book(self, updated_book: Book) -> None:
        for book in self.books:
            if book._book_id == updated_book._book_id:
                book._title = updated_book._title
                book._author = updated_book._author
                book._available = updated_book._available
                break
        self.save_books()

    # Delete book
    def delete_book(self, book_id: int) -> None:
        self.books = [book for book in self.books if book._book_id != book_id]
        self.save_books()

    # Borrow book
    def borrow_book(self, book_id: int, user_id: int) -> None:
        for book in self.books:
            if book._book_id == book_id and book.is_available():
                book.mark_as_borrowed()
                print(f"Book '{book._title}' borrowed by user ID {user_id}.")
                break
        else:
            print(f"Book with ID {book_id} is not available.")
        self.save_books()

    # Return book
    def return_book(self, book_id: int, user_id: int) -> None:
        for book in self.books:
            if book._book_id == book_id and not book.is_available():
                book.mark_as_returned()
                print(f"Book '{book._title}' returned by user ID {user_id}.")
                break
        else:
            print(f"Book with ID {book_id} was not borrowed.")
        self.save_books()

    # Save books to file
    def save_books(self) -> None:
        with open(self.books_file, 'w') as f:
            for book in self.books:
                f.write(f"{book._book_id},{book._title},{book._author},{book._available}\n")

    # Load books from file
    def load_data(self) -> None:
        if os.path.exists(self.books_file):
            with open(self.books_file, 'r') as f:
                for line in f:
                    book_id, title, author, available = line.strip().split(',')
                    self.books.append(Book(int(book_id), title, author, available == 'True'))

        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                for line in f:
                    user_id, name, email = line.strip().split(',')
                    self.users.append(User(int(user_id), name, email))

    # Save users to file
    def save_users(self) -> None:
        with open(self.users_file, 'w') as f:
            for user in self.users:
                f.write(f"{user._user_id},{user._name},{user._email}\n")

    # Register new user
    def register_user(self, user: User) -> None:
        self.users.append(user)
        self.save_users()

    # List all available books
    def list_books(self) -> None:
        for book in self.books:
            book.display_info()


# Sample usage

library_manager = LibraryManager()

# Librarian adds books
librarian = Librarian(1, 'Alice Johnson', 'alice.johnson@gmail.com')
book1 = Book(101, 'To Kill a Mockingbird', 'Harper Lee')
book2 = Book(102, 'Pride and Prejudice', 'Jane Austen')

librarian.manage_books(library_manager, book1, 'add')
librarian.manage_books(library_manager, book2, 'add')

# Member borrows and returns books
member = Member(2, 'John Smith', 'john.smith@gmail.com')
member.borrow_book(library_manager, 101)
member.return_book(library_manager, 101)

# List all books
library_manager.list_books()
