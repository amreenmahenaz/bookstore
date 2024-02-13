class Book:
    def __init__(self, title, author, genre, price):
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price

class BookStore:
    def __init__(self):
        self.inventory = []

    def add_book(self, book):
        self.inventory.append(book)
        print(f"Added {book.title} to the inventory.")

    def remove_book(self, title):
        for book in self.inventory:
            if book.title == title:
                self.inventory.remove(book)
                print(f"Removed {book.title} from the inventory.")
                return
        print(f"Book with title '{title}' not found in the inventory.")

    def search_book(self, title):
        for book in self.inventory:
            if book.title == title:
                print(f"Book Title: {book.title}")
                print(f"Author: {book.author}")
                print(f"Genre: {book.genre}")
                print(f"Price: {book.price}")
                return
        print(f"Book with title '{title}' not found in the inventory.")

    def display_inventory(self):
        if not self.inventory:
            print("No books in the inventory.")
            return
        print("Book Inventory:")
        for book in self.inventory:
            print(f"Title: {book.title}, Author: {book.author}, Genre: {book.genre}, Price: {book.price}")

# Example usage
if __name__ == "__main__":
    bookstore = BookStore()

    # Adding books to inventory
    book1 = Book("Harry Potter and the Philosopher's Stone", "J.K. Rowling", "Fantasy", 10.99)
    book2 = Book("The Great Gatsby", "F. Scott Fitzgerald", "Classics", 8.99)
    bookstore.add_book(book1)
    bookstore.add_book(book2)

    # Displaying inventory
    bookstore.display_inventory()

    # Searching for a book
    bookstore.search_book("The Great Gatsby")

    # Removing a book
    bookstore.remove_book("Harry Potter and the Philosopher's Stone")

    # Displaying updated inventory
    bookstore.display_inventory()
