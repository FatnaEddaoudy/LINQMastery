import React, { useEffect, useState } from "react";
import { getBooks } from "../Services/BookService";

function BooksPage() {
  const [books, setBooks] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const booksPerPage = 8; // adjust how many cards per page
   const [searchText, setSearchText] = useState("");

  useEffect(() => {
    getBooks().then((data) => setBooks(data));
  }, []);

  // Calculate indexes for current page
  const indexOfLastBook = currentPage * booksPerPage;
  const indexOfFirstBook = indexOfLastBook - booksPerPage;
  const currentBooks = books.slice(indexOfFirstBook, indexOfLastBook);

  const totalPages = Math.ceil(books.length / booksPerPage);

  const handleNext = () => {
    if (currentPage < totalPages) setCurrentPage(currentPage + 1);
  };

  const handlePrev = () => {
    if (currentPage > 1) setCurrentPage(currentPage - 1);
  };

  return (
    <div>
      <div className="cards">
        {currentBooks.map((book) => (
          <div className="card" key={book.bookID}>
            <img
              src={book.photoUrl || "/images/BookDefault.png"}
              alt={book.title}
            />
            <div className="card-content">
              <h2>{book.title}</h2>
              <p>
                The book with ISBN <span>{book.isbn}</span> is a{" "}
                {book.genreName} novel, first published in{" "}
                <span>{book.publishedYear || "Onbekend jaar"}</span>. It
                contains <span>{book.pages || "?"}</span> pages of engaging
                content. The author, <span>{book.authorName}</span>, has
                skillfully written this work, making it a valuable addition to
                the library.
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Pagination */}
   <div className="pagination">
    <button onClick={handlePrev} disabled={currentPage === 1}>
      Previous
    </button>
    <span>
      Page {currentPage} of {totalPages}
    </span>
    <button onClick={handleNext} disabled={currentPage === totalPages}>
      Next
    </button>
  </div>
    </div>
  );
}

export default BooksPage;
