using LibraryData.Models;
using LibraryData.Repositories;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryServices.Services
{
    public class GenreServices
    {
        private readonly IGenreRepository _genreRepository;
        public GenreServices(IGenreRepository genreRepository)
        {
            _genreRepository = genreRepository;
        }
        public async Task<IEnumerable<Genre>> GetAllGenresAsync()
        {
            return await _genreRepository.GetAllGenresAsync();
        }
        public async Task<Genre?> GetGenreByIdAsync(int id)
        {
            return await _genreRepository.GetGenreByIdAsync(id);
        }
        public async Task  AddGenreAsync(Genre genre)
        {
           await _genreRepository.AddGenreAsync(genre);
        }
        public async Task UpdateGenreAsync(Genre genre)
        {      
           await _genreRepository.UpdateGenreAsync(genre);
        }
    }
}
