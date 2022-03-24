from audioop import add
from flask import redirect, render_template, request
from flask_app import app
from flask_app.models.author import Author
from flask_app.models.book import Book

@app.route('/authors')
def show_all_authors():
    authors = Author.get_all()
    return render_template('authors.html', authors=authors)

@app.route('/authors/create', methods = ['POST'])
def create_author():
    Author.create(request.form)
    return redirect('/authors')

@app.route('/authors/<int:id>')
def show_favorites(id):
    data = {
        'id':id
    }
    author = Author.one_author_all_favorites(data)
    books = Book.get_all()
    return render_template('author_favorites.html', author = author, books=books)

@app.route('/authors/create_favorite', methods=['POST'])
def create_favorite():
    Author.create_favorite(request.form)
    return redirect(f"/authors/{request.form['author_id']}")