from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.book import Book

class Author:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorites = []

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM authors;'
        results = connectToMySQL('books_schema').query_db(query)
        authors = []
        for author in results:
            authors.append(cls(author))
        return authors

    @classmethod
    def create(cls, data):
        query = 'INSERT INTO authors (name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW());'
        result = connectToMySQL('books_schema').query_db(query, data)
        return result

    @classmethod
    def one_author_all_favorites(cls, data):
        query = 'SELECT * FROM authors LEFT JOIN favorites on authors.id = author_id LEFT JOIN books on book_id = books.id WHERE authors.id = %(id)s;'
        results = connectToMySQL('books_schema').query_db(query,data)
        author = cls(results[0])
        for row in results:
            book_data = {
                'id' : row['books.id'],
                'title' : row['title'],
                'num_of_pages' : row['num_of_pages'],
                'created_at' : row['books.created_at'],
                'updated_at' : row['books.updated_at']
            }
            author.favorites.append(Book(book_data))
        return author

    @classmethod
    def create_favorite(cls,data):
        query = 'INSERT INTO favorites (author_id, book_id) VALUES(%(author_id)s, %(book_id)s);'
        result = connectToMySQL('books_schema').query_db(query,data)
        return result