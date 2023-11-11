import mysql.connector
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vasundhara@403",
    database="management"
    )
# Create a database
cursor = connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS management")
cursor.execute("USE management")
#library collection table- Books
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Books (
        Book_ID INT PRIMARY KEY,
        Book_Name VARCHAR(255),
        Author_Name VARCHAR(255),
        Quantity INT  
    )
    """
)
#borrowed books table- Currently_Borrowed
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Currently_Borrowed (
        Student_ID INT,
        Book_ID INT,
        Borrow_Date DATE,
        Due_Date DATE
    )
    """
)
#borrowing history table- Borrowing_History
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Borrowing_History (
        Student_ID INT,
        Book_ID INT,
        Borrow_Date DATE,
        Due_Date DATE,
        Fine INT
    )
    """
)
# Commit the changes and close the connection
connection.commit()
connection.close()
print("\nAll table are ready !!!\n")


#to add references if needed-----> FOREIGN KEY (Book_ID) REFERENCES Books (Book_ID)