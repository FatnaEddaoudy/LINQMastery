using LibraryData.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Repositories
{
    public class SqlAuthorRepository : IAuthorRepository
    {
        private readonly LibraryDBContext _context;
        public SqlAuthorRepository(LibraryDBContext context)
        {
            _context = context;
        }
        public async Task<IEnumerable<Author>> GetAllAuthorAsysnc()
        {
            return await _context.Authors.ToListAsync();
        }
        public async Task<Author?> GetAutorBjIdAsync(int id)
        {
           return await _context.Authors.FirstOrDefaultAsync(a => a.AuthorId==id);
        }
        public async Task AddAuthorAsync(Author author)
        {
         await _context.Authors.AddAsync(author);
            await _context.SaveChangesAsync();
        }
        public async Task DeleteAuthorAsync(int id)
        {
            var author = await GetAutorBjIdAsync(id);
             _context.Authors.Remove(author);
            await _context.SaveChangesAsync();
        }
        public async Task UpdateAuthorAsync(Author author)
        {
            var existingAuthor = await _context.Authors.FindAsync(author.AuthorId);

            if (existingAuthor == null)
                throw new Exception($"Author with ID {author.AuthorId} not found.");

            // Update only the fields that are provided (null checks for optional updates)
            existingAuthor.Name = author.Name ?? existingAuthor.Name;
            existingAuthor.Country = author.Country ?? existingAuthor.Country;
            existingAuthor.birthyear = author.birthyear != default ? author.birthyear : existingAuthor.birthyear;

            await _context.SaveChangesAsync();
        }



    }
}
