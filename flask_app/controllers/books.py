from flask import redirect, render_template, request
from flask_app import app
from flask_app.models.author import Author
from flask_app.models.book import Book


@app.route('/books')
def show_books():
    books = Book.get_all()
    return render_template('books.html', books=books)

@app.route('/books/create', methods = ['POST'])
def create_book():
    Book.create(request.form)
    return redirect('/books')

@app.route('/books/<int:id>')
def show_book(id):
    data = {
        'id':id
    }
    book = Book.one_book_all_authors(data)
    authors = Author.get_all()
    return render_template('book_favorites.html', book=book, authors=authors)

@app.route('/books/create_favorite', methods=['POST'])
def create_favorited():
    Book.create_favorite(request.form)
    return redirect(f"/books/{request.form['book_id']}")

