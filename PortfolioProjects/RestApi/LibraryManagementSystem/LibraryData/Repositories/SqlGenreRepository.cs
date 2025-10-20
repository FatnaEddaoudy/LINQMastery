using LibraryData.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Repositories
{
    public class SqlGenreRepository : IGenreRepository
    {
        private readonly LibraryDBContext _context;
        public SqlGenreRepository(LibraryDBContext context)
        {
            _context = context;
        }
        public async Task AddGenreAsync(Genre genre)
        {
            await _context.Genres.AddAsync(genre);
            await SaveChangeAsync();
        }
         public async Task DeleteGenreAsync(int id)
        {
          var genre= await _context.Genres.FindAsync(id);
            if(genre != null)
            {
                _context.Genres.Remove(genre);
                await SaveChangeAsync();
            }
        }
        public async Task<IEnumerable<Genre>> GetAllGenresAsync()
        {
            return await _context.Genres.ToListAsync();
        }

        public Task<Genre?> GetGenreByIdAsync(int id)
        {
            var genre=  _context.Genres.FirstOrDefaultAsync(g=> g.GenreId==id);
            return genre;
        }

        public async Task SaveChangeAsync()
        {
            await _context.SaveChangesAsync();
        }

        public async Task UpdateGenreAsync(Genre genre)
        {
            var existingGenre = _context.Genres.FirstOrDefault(g => g.GenreId == genre.GenreId);
            if (existingGenre != null)
            {
                existingGenre.Name = genre.Name;
                existingGenre.Description = genre.Description;
                _context.Genres.Update(existingGenre);
                await SaveChangeAsync();
            }
        }
    }
}
