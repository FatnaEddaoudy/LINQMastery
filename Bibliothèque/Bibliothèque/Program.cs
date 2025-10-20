using System.Net;
using System.Net.NetworkInformation;

//----------Exercise------------------
//Create a Console program with classes and lists:
//Student(StudentId, LastName, FirstName, Address)
//Book(BookId, Title, AuthorId, PublisherId, ThemeId, PublicationYear)
//Author(AuthorId, AuthorName, AuthorAddress)
//Publisher(PublisherId, PublisherName, PublisherAddress)
//Theme(ThemeId, ThemeTitle)
//Loan(StudentId, BookId, LoanDate, ReturnDate)

//Normale this exercise they asking for Relational Algebra Queries but i go to write LINQ Queries instead.
//Then write LINQ queries to answer the following questions:
// 1. The last name, first name and address of the student with last name ‘Alami’  
// 2. The ID of the author named ‘Alami’  
// 3. The list of books written by the author with ID 121  
// 4. The books written by the author named ‘Alami’  
// 5. The ID of the author of the book ‘How to get 20 in DB’  
// 6. The name and address of the author of the book ‘How to get 20 in DB’  
// 7. The books by the author ‘Alami’ published by the publisher ‘Nowhere’  
// 8. The books by the authors ‘Alami’ or ‘Belhadj’  
// 9. The books that have never been borrowed



// --- Classes ---
class Student
{
    public int StudentId { get; set; } // PK
    public string LastName { get; set; }
    public string FirstName { get; set; }
    public string Address { get; set; }
}

class Book
{
    public int BookId { get; set; } // PK
    public string Title { get; set; }
    public int AuthorId { get; set; } // FK
    public int PublisherId { get; set; } // FK
    public int ThemeId { get; set; } // FK
    public int PublicationYear { get; set; }
}

class Author
{
    public int AuthorId { get; set; } // PK
    public string AuthorName { get; set; }
    public string AuthorAddress { get; set; }
}

class Publisher
{
    public int PublisherId { get; set; } // PK
    public string PublisherName { get; set; }
    public string PublisherAddress { get; set; }
}

class Theme
{
    public int ThemeId { get; set; } // PK
    public string ThemeTitle { get; set; }
}

class Loan
{
    public int StudentId { get; set; }   // FK
    public int BookId { get; set; }      // FK
    public DateTime LoanDate { get; set; }
    public DateTime? ReturnDate { get; set; }
}

class Program
{
    static void Main(string[] args)
    {
        // --- Example data Source ---
        // --- Example data Source ---

        List<Student> students = new List<Student>
{
    new Student { StudentId = 1, LastName = "Alami", FirstName = "Youssef", Address = "Rabat" },
    new Student { StudentId = 2, LastName = "Belhadj", FirstName = "Sara", Address = "Casablanca" },
    new Student { StudentId = 3, LastName = "Smith", FirstName = "John", Address = "New York" }
};

        List<Author> authors = new List<Author>
{
    new Author { AuthorId = 121, AuthorName = "Alami", AuthorAddress = "Marrakech" },
    new Author { AuthorId = 122, AuthorName = "Belhadj", AuthorAddress = "Tanger" },
    new Author { AuthorId = 123, AuthorName = "Mark Twain", AuthorAddress = "Missouri" }
};

        List<Publisher> publishers = new List<Publisher>
{
    new Publisher { PublisherId = 1, PublisherName = "Nowhere", PublisherAddress = "Paris" },
    new Publisher { PublisherId = 2, PublisherName = "Penguin", PublisherAddress = "London" }
};

        List<Theme> themes = new List<Theme>
{
    new Theme { ThemeId = 1, ThemeTitle = "Novel" },
    new Theme { ThemeId = 2, ThemeTitle = "Drama" }
};

        List<Book> books = new List<Book>
{
    new Book { BookId = 1, Title = "How to get 20 in DB", AuthorId = 121, PublisherId = 1, ThemeId = 1, PublicationYear = 2025 },
    new Book { BookId = 2, Title = "Learning C#", AuthorId = 122, PublisherId = 2, ThemeId = 1, PublicationYear = 2023 },
    new Book { BookId = 3, Title = "Adventures of Tom Sawyer", AuthorId = 123, PublisherId = 2, ThemeId = 1, PublicationYear = 1876 },
    new Book { BookId = 4, Title = "New Book Never Borrowed", AuthorId = 122, PublisherId = 2, ThemeId = 2, PublicationYear = 2024 }
};

        List<Loan> loans = new List<Loan>
{
    new Loan { StudentId = 1, BookId = 1, LoanDate = new DateTime(2025, 9, 1), ReturnDate = null },
    new Loan { StudentId = 2, BookId = 2, LoanDate = new DateTime(2025, 9, 5), ReturnDate = new DateTime(2025, 9, 15) },
    new Loan { StudentId = 3, BookId = 3, LoanDate = new DateTime(2025, 8, 20), ReturnDate = new DateTime(2025, 9, 1) }
    // BookId 4 is never borrowed
};

        //---------------Query Linq-------------------

        // 1. The last name, first name and address of the student with last name ‘Alami’  
        Console.WriteLine("The last name, first name and address of the student with last name ‘Alami’");
        var q1 = from s in students
                 where s.LastName == "Alami"
                 select new { s.LastName, s.FirstName, s.Address };
        foreach (var item in q1)
        {
            Console.WriteLine($"LastName: {item.LastName}, FirstName: {item.FirstName}, Address: {item.Address}");
        }

        Console.WriteLine("--------------------------------------------------");
        // 2. The ID of the author named ‘Alami’  
        Console.WriteLine("The ID of the author named ‘Alami’");
        var q2 = from a in authors
                 where a.AuthorName == "Alami"
                 select a.AuthorId;

        foreach (var item in q2)
        {
            Console.WriteLine($"AuthorId: {item}");
        }
        Console.WriteLine("--------------------------------------------------");
        // 3. The list of books written by the author with ID 121  
        Console.WriteLine("The list of books written by the author with ID 121");
        var q3 = from b in books
                 where b.AuthorId == 121
                 select b;
        foreach (var item in q3)
        {      
            Console.WriteLine($"BookId: {item.BookId}, Title: {item.Title}, AuthorId: {item.AuthorId}, PublisherId: {item.PublisherId}, ThemeId: {item.ThemeId}, PublicationYear: {item.PublicationYear}");
        }
        Console.WriteLine("--------------------------------------------------");
        // 4. The books written by the author named ‘Alami’
       Console.WriteLine("The books written by the author named ‘Alami’");
        var q4 = from b in books
                 join a in authors on b.AuthorId equals a.AuthorId
                 where a.AuthorName == "Alami"
                 select b;
        foreach (var item in q4)
        {
            Console.WriteLine($"BookId: {item.BookId}, Title: {item.Title}, AuthorId: {item.AuthorId}, PublisherId: {item.PublisherId}, ThemeId: {item.ThemeId}, PublicationYear: {item.PublicationYear}");
        }
        Console.WriteLine("--------------------------------------------------");
        // 5. The ID of the author of the book ‘How to get 20 in DB’  
        Console.WriteLine("The ID of the author of the book ‘How to get 20 in DB’");
        var q5 = from b in books
                 where b.Title == "How to get 20 in DB"
                 select new { b.Title, b.AuthorId };
        foreach (var item in q5)
        {
            Console.WriteLine($"Title: {item.Title}, AuthorId: {item.AuthorId}");
        }
        // 6. The name and address of the author of the book ‘How to get 20 in DB’  
        Console.WriteLine("The name and address of the author of the book ‘How to get 20 in DB’");
        var q6 = from b in books
                 join a in authors on b.AuthorId equals a.AuthorId
                 where b.Title == "How to get 20 in DB"
                 select new { a.AuthorName, a.AuthorAddress };
        foreach (var item in q6)
        {
           Console.WriteLine($"AuthorName: {item.AuthorName}, AuthorAddress: {item.AuthorAddress}");
        }
        Console.WriteLine("--------------------------------------------------");
        // 7. The books by the author ‘Alami’ published by the publisher ‘Nowhere’  
        Console.WriteLine("The books by the author ‘Alami’ published by the publisher ‘Nowhere’");
        var q7 = from b in books
                 join a in authors on b.AuthorId equals a.AuthorId
                 join p in publishers on b.PublisherId equals p.PublisherId
                 where a.AuthorName == "Alami" && p.PublisherName == "Nowhere"
                 select b;

        foreach (var item in q7)
        {
            Console.WriteLine($"BookId: {item.BookId}, Title: {item.Title}, ...");
        }
        Console.WriteLine("--------------------------------------------------");
        // 8. The books by the authors ‘Alami’ or ‘Belhadj’  
        Console.WriteLine("The books by the authors ‘Alami’ or ‘Belhadj’");
        var q8 = from b in books
                 join a in authors on b.AuthorId equals a.AuthorId
                 where a.AuthorName == "Alami" || a.AuthorName == "Belhadj"
                 select b;
        foreach (var item in q8)
        {
            Console.WriteLine($"BookId: {item.BookId}, Title: {item.Title}, AuthorId: {item.AuthorId}, PublisherId: {item.PublisherId}, ThemeId: {item.ThemeId}, PublicationYear: {item.PublicationYear}");
        }
        Console.WriteLine("--------------------------------------------------");
        // 9. The books that have never been borrowed
        Console.WriteLine("The books that have never been borrowed");
        var q9 = from b in books
                 join l in loans on b.BookId equals l.BookId into loanGroup
                 from lg in loanGroup.DefaultIfEmpty() // flatten
                 where lg == null // no matching loan
                 select b;

        foreach (var item in q9)
        {
            Console.WriteLine($"BookId: {item.BookId}, Title: {item.Title}, AuthorId: {item.AuthorId}, PublisherId: {item.PublisherId}, ThemeId: {item.ThemeId}, PublicationYear: {item.PublicationYear}");
        }
        Console.WriteLine("--------------------------------------------------");
        //Using All(all loans do not match)
        Console.WriteLine("The books that have never been borrowed (using All)");
        var q9_1= from b in books
                 where loans.All(l => l.BookId != b.BookId)
                 select b;

        foreach (var item in q9_1)
        {
            Console.WriteLine($"BookId: {item.BookId}, Title: {item.Title}, AuthorId: {item.AuthorId}, PublisherId: {item.PublisherId}, ThemeId: {item.ThemeId}, PublicationYear: {item.PublicationYear}");
        }

    }
}