using LibraryData.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Repositories
{
    public interface IAuthorRepository
    {
        Task<IEnumerable<Author>> GetAllAuthorAsysnc();
        Task<Author?> GetAutorBjIdAsync(int id);
        Task AddAuthorAsync(Author author);
        Task UpdateAuthorAsync(Author author);
        Task DeleteAuthorAsync(int id);
    }
}
