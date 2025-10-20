using LibraryData.Models;
using LibraryServices.Services;
using Microsoft.AspNetCore.Mvc;

namespace LibraryApi.Controllers
{
    [Route ("api/[controller]")]
    [ApiController]
    public class GenreController : Controller
    {
        private readonly GenreServices _genreServices;
        public GenreController(GenreServices genreServices)
        {
            _genreServices = genreServices;
        }
        [HttpGet]
        public async Task<IActionResult> GetAllGenres()
        {
            var genres = await _genreServices.GetAllGenresAsync();
            return Ok(genres);
        }
        [HttpGet("{id}")]
        public async Task<IActionResult> GetGenreById(int id)
        {
            var genre = await _genreServices.GetGenreByIdAsync(id);
            if (genre == null)
            {
                return NotFound();
            }
            return Ok(genre);
        }
        [HttpPost]
        public async Task AddGenre(Genre genre)
        {
            await _genreServices.AddGenreAsync(genre);
          
        }
        [HttpPut]
        public async Task UpdateGenre(Genre genre)
        {
            await _genreServices.UpdateGenreAsync(genre);
        }
    }
}
