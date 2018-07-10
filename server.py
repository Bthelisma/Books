from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = "mySecret!"
mysql = MySQLConnector(app,'booksdb')
all_books = mysql.query_db("SELECT * FROM books")

@app.route('/')
def index():
    books = mysql.query_db("SELECT * FROM books")
    return render_template('index.html', all_books=books)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/create', methods=['POST'])
def create():
    # Write query as a string. Notice how we have multiple values
    # we want to insert into our query.
    query = "INSERT INTO books (Title, Author, Date_added, Created_at, Updated_at) VALUES (:title, :author, NOW(), NOW(), NOW())"
    # We'll then create a dictionary of data from the POST data received.
    data = {
             'title': request.form['title'],
             'author':  request.form['author'],
            }
    # Run query, with dictionary values injected into the query.
    mysql.query_db(query, data)
    session['title']= request.form['title']
    session['author']= request.form['author']
    return redirect('/')

@app.route("/destroy/<book_id>", methods=["GET"])
def destroy(book_id):
    query = "SELECT title FROM books WHERE id = :id"
    data = {"id":int(book_id)}
    book = mysql.query_db(query, data)
    return render_template("delete.html", title=book[0]["title"], book_id=book_id)

@app.route("/delete/<book_id>", methods=["POST"])
def delete(book_id):
    query = "DELETE FROM books WHERE id = :id"
    data = {"id":int(book_id)}
    mysql.query_db(query, data)
    return redirect("/")

@app.route("/update/<book_id>", methods=["GET"])
def update(book_id):
    query = "SELECT title, author FROM books WHERE id = :id"
    data = {"id":int(book_id)}
    book = mysql.query_db(query, data)
    return render_template("update.html", title=book[0]["title"], author=book[0]["author"], book_id=book_id)

@app.route("/edit/<book_id>", methods=["POST"])
def edit(book_id):
    # valid = True
    # if len(request.form["title"]) < 1:
    #     flash("Title cannot be blank!")
    #     valid = False
    # if len(request.form["author"]) < 1:
    #     flash("Author cannot be blank!")
    #     valid = False
    # if valid:
    query = "UPDATE books SET title = :title, author = :author, updated_at = NOW() WHERE id = :id"
    data = {
            "title":request.form["title"],
            "author":request.form["author"],
            "id":int(book_id)
    }
    mysql.query_db(query, data)
    return redirect("/")
    # return redirect("/update/"+book_id)



app.run(debug=True)
