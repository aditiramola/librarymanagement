from flask import Flask,render_template ,request, jsonify,redirect
import mysql.connector
from datetime import date, timedelta
import  MySQLdb.cursors
from flask_mysqldb import MySQL

app = Flask(__name__)


# Establish a database connection
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Vasundhara@403",
    "database": "management",
}
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

@app.route('/add-book', methods=['POST'])
def books():
    if request.method == 'GET':
        # Retrieve a list of books
        cursor.execute("SELECT * FROM books")
        books = [{"Book_ID": book_id, "Book_Name": book_name, "Author_Name": author_name, "Quantity": quantity}
                 for (book_id, book_name, author_name, quantity) in cursor]
        return jsonify(books)
    elif request.method == 'POST':
        # Add a new book
        data = request.json
        book_id=data.get("Book_ID")
        book_name = data.get("Book_Name")
        author_name = data.get("Author_Name")
        quantity = data.get("Quantity")

        if not book_name or not author_name or quantity is None:
            return "Invalid book data", 400

        cursor.execute("INSERT INTO books (Book_Name, Author_Name, Quantity) VALUES (%s, %s, %s)",
                       (book_name, author_name, quantity))
        connection.commit()
        return "Book added successfully", 201

@app.route('/books/<int:Book_ID>', methods=['GET', 'PUT', 'DELETE'])
def manage_book(book_id):
    if request.method == 'GET':
        cursor.execute("SELECT * FROM books WHERE Book_ID = %s", (book_id,))
        book = cursor.fetchone()
        if not book:
            return "Book not found", 404
        book_data = {
            "Book_ID": book[0],
            "Book_Name": book[1],
            "Author_Name": book[2],
            "Quantity": book[3]
        }
        return jsonify(book_data)

    elif request.method == 'PUT':
        data = request.json
        book_name = data.get("Book_Name")
        author_name = data.get("Author_Name")
        quantity = data.get("Quantity")

        if not book_name or not author_name or quantity is None:
            return "Invalid book data", 400

        cursor.execute("UPDATE books SET Book_Name = %s, Author_Name = %s, Quantity = %s WHERE Book_ID= %s",
                       (book_name, author_name, quantity, book_id))
        connection.commit()
        return "Book updated successfully", 200

    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM books WHERE Book_ID = %s", (book_id,))
        connection.commit()
        return "Book deleted successfully", 204

@app.route('/borrow-book', methods=['POST'])
def borrow_book():
    data = request.json
    student_id = data.get("Student_ID")
    book_id = data.get("Book_ID")  # Include Book_ID for borrowing
    borrow_date = data.get("Borrow_Date")
    due_date = data.get("Due_Date")

    if not student_id or not book_id or not borrow_date or not due_date:
        return "Invalid borrowing data", 400

    cursor.execute("SELECT * FROM books WHERE Book_ID = %s", (book_id,))
    book = cursor.fetchone()

    if not book:
        return "Book not found", 404

    cursor.execute("INSERT INTO borrowings (Book_ID, Student_ID, Borrow_Date, Due_Date) VALUES (%s, %s, %s, %s)",
                   (book_id, student_id, borrow_date, due_date))
    connection.commit()

    cursor.execute("UPDATE books SET Quantity = Quantity - 1 WHERE Book_ID = %s", (book_id))
    connection.commit()

    return "Book borrowed successfully", 201
if __name__ == '__main__':
    app.run(debug=True,port=5500)
