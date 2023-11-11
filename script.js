document.addEventListener("DOMContentLoaded", function () {
  // Add Book Form
  const addBookForm = document.getElementById("add-book-form");
  const addBookFeedback = document.getElementById("success-message");
  const addBookError = document.getElementById("error-message");

  addBookForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(addBookForm);
    const bookData = {
      book_id: formData.get("Book_ID"),
      book_name: formData.get("Book_Name"),
      author_name: formData.get("Author_Name"),
      quantity: parseInt(formData.get("Quantity"))
    };
  
    fetch('/add-book', {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(bookData)
    })
      .then(response => {
        if (response.status === 201) {
          return response.json();
        } else {
          throw new Error("Failed to add book");
        }
      })
      .then(data => {
        addBookFeedback.textContent = data.message;
        addBookError.textContent = "";
        addBookForm.reset();
      })
      .catch(error => {
        addBookError.textContent = error.message;
        addBookFeedback.textContent = "";
      });
  });

  // Borrow Book Form
  const borrowBookForm = document.getElementById("borrow-book-form");
  const borrowBookFeedback = document.getElementById("success-message");
  const borrowBookError = document.getElementById("error-message");

  borrowBookForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(borrowBookForm);
    const borrowData = {
      student_id: formData.get("student_id"),
      book_name: formData.get("book_name"),
      borrow_date: formData.get("borrow_date"),
      due_date: formData.get("due_date")
    };

    fetch("/borrow-book", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(borrowData)
    })
      .then(response => {
        if (response.status === 201) {
          return response.json();
        } else {
          throw new Error("Failed to borrow book");
        }
      })
      .then(data => {
        borrowBookFeedback.textContent = data.message;
        borrowBookError.textContent = "";
        borrowBookForm.reset();
      })
      .catch(error => {
        borrowBookError.textContent = error.message;
        borrowBookFeedback.textContent = "";
      });
  });
});
