from flask_app.config.mysqlconnection import connectToMySQL
import flask_app.models.author as author

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorites = []

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM books;'
        results = connectToMySQL('books_schema').query_db(query)
        books = []
        for book in results:
            books.append(cls(book))
        return books

    @classmethod
    def create(cls, data):
        query = 'INSERT INTO books (title, num_of_pages, created_at, updated_at) VALUES (%(title)s, %(num_of_pages)s, NOW(), NOW());'
        result = connectToMySQL('books_schema').query_db(query, data)
        return result

    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM books WHERE id=%(id)s;'
        result = connectToMySQL('books_schema').query_db(query, data)
        return cls(result[0])

    @classmethod
    def one_book_all_authors(cls,data):
        query = 'SELECT * from books LEFT JOIN favorites on books.id = book_id LEFT JOIN authors on author_id = authors.id WHERE books.id = %(id)s;'
        results = connectToMySQL('books_schema').query_db(query,data)
        book = cls(results[0])
        for row in results:
            author_data = {
                'id' : row['authors.id'],
                'name' : row['name'],
                'created_at' : row['authors.created_at'],
                'updated_at' : row['authors.updated_at']
            }
            book.favorites.append(author.Author(author_data))
        return book

    @classmethod
    def create_favorite(cls,data):
        query = 'INSERT INTO favorites (author_id, book_id) VALUES(%(author_id)s, %(book_id)s);'
        result = connectToMySQL('books_schema').query_db(query,data)
        return result

