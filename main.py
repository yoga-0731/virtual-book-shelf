from flask import Flask, render_template, request, redirect, url_for
# import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# all_books = []

# Connecting to sqlite3
# db = sqlite3.connect('books-collection.db')  #-> creates the table 'books-collection'
# cursor = db.cursor()

# Creating table "books"
# cursor.execute("CREATE TABLE books(id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE,"
#                 "author varchar(250) NOT NULL, rating FLOAT NOT NULL)")

# Adding data to table
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J.K.Rowling', 9.1)")
# db.commit()

# Since it's hard to write SQL commands, we use SQLAlchemy
# https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/
# Create Database
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../virtual-book-shelf.db"  # configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # initialize the app with the extension


# Create Table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()  # Do this after creating all models and tables
    # new_book = Book(title="Harry Potter", author="J. K. Rowling", rating=9.3)  # Create record
    # db.session.add(new_book)
    # db.session.commit()


@app.route('/')
def home():
    return render_template('index.html', books=db.session.query(Book).all())


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        book_name = request.form.get('name')
        author = request.form.get('author')
        rating = request.form.get('rating')
        new_book = Book(title=book_name, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
        # all_books.append({"title": book_name, "author": author, "rating": rating})
    # print(all_books)
    return render_template('add.html')


@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        book_id = request.form.get('id')
        print(book_id)
        book = db.session.query(Book).filter_by(id=book_id).first()
        print(book)
        book.rating = request.form.get('rating')
        print(book)
        db.session.commit()
        return redirect(url_for('home'))
    # print(request.args.to_dict()['book_id'])  # request args sent from index.html url_for, these args will appear in request url too
    book_id = request.args.to_dict()['book_id']
    book = db.session.query(Book).filter_by(id=book_id).first()
    # print(book)
    return render_template('edit_rating.html', book=book)


@app.route('/delete')
def delete():
    book_id = request.args.to_dict()['book_id']
    book = db.session.query(Book).filter_by(id=book_id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

