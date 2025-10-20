using LibraryData.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Repositories
{
    public interface IGenreRepository
    {
        Task<IEnumerable<Genre>> GetAllGenresAsync();
        Task<Genre?> GetGenreByIdAsync(int id);
        Task AddGenreAsync(Genre genre);
        Task UpdateGenreAsync(Genre genre);
        Task DeleteGenreAsync(int id);
        Task SaveChangeAsync();
    }
}
