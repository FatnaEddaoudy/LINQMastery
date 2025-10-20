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
    public class BookServices
    {
        private readonly IBookRepository _bookRepository;
        public BookServices(IBookRepository bookRepository)
        {
            _bookRepository = bookRepository;
        }
        public async Task AddAsync(Book book)
        {
         await  _bookRepository.AddAsync(book);
        }

        public async Task DeleteAsync(int id)
        {
            await _bookRepository.DeleteAsync(id);
        }

        public async Task<IEnumerable<Object>> GetAllAsync()
        {
          return await _bookRepository.GetAllAsync();
        }

        public async Task<Book?> GetByIdAsync(int id)
        {
            return await _bookRepository.GetByIdAsync(id);
        }
        public async Task UpdateAsync(Book book)
        {
          await  _bookRepository.UpdateAsync(book);
        }
    }
}
