using LibraryData.Models;
using LibraryData.Repositories;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryServices.Services
{
    public class AuthorServices
    {
        private readonly IAuthorRepository _authorRepository;
        public AuthorServices(IAuthorRepository authorRepository)
        {
            _authorRepository = authorRepository;
        }
        public async Task<IEnumerable<Author>> GetAllAuthorAsysnc()
        {
            return await _authorRepository.GetAllAuthorAsysnc();
        }
        public async Task<Author?> GetAutorBjIdAsync(int id)
        {
            return await _authorRepository.GetAutorBjIdAsync(id);
        }
        public async Task AddAuthorAsync(Author author)
        {
            await _authorRepository.AddAuthorAsync(author);
        }
        public async Task DeleteAuthorAsync(int id)
        {
            await _authorRepository.DeleteAuthorAsync(id);
        }
        public async Task UpdateAuthorAsync(Author author)
        {
          await  _authorRepository.UpdateAuthorAsync(author);
        }
    }
}
