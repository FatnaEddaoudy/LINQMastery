using LibraryData.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Repositories
{
    public class SqlBookRepository : IBookRepository
    {
        private readonly LibraryDBContext _context;
        public SqlBookRepository(LibraryDBContext context)
        {
            _context = context;
        }
        public async Task<IEnumerable<object>> GetAllAsync()
        {
            var books = await _context.Books
                .Select(b => new
                {
                    b.BookID,
                    b.Title,
                    b.PhotoUrl,
                    AuthorName = b.Author != null ? b.Author.Name : "Onbekend",
                    GenreName = b.Genre != null ? b.Genre.Name : "Onbekend",
                    b.PublishedYear,
                    b.ISBN,
                    b.Pages,
                    b.CopierAvailable
                })
                .ToListAsync();

            return books;
        }
        public async Task<Book?> GetByIdAsync(int id)
        {
            return await _context.Books.FirstOrDefaultAsync(b => b.BookID == id);
        }
        public async Task AddAsync(Book book)
        {
            await _context.Books.AddAsync(book);
            await _context.SaveChangesAsync();
        }
        public async Task DeleteAsync(int id)
        {
            var book = await _context.Books.FindAsync(id);
            if (book == null)
                throw new KeyNotFoundException($"Book with ID {id} not found.");

            _context.Books.Remove(book);
            await _context.SaveChangesAsync();
        }

        public async Task UpdateAsync(Book book)
        {
            _context.Books.Update(book);
            await _context.SaveChangesAsync();
        }

       
    }
}
