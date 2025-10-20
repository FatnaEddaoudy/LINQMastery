using LibraryData.Models;
using LibraryData.Repositories;
using LibraryServices.Services;
using Microsoft.AspNetCore.Mvc;

namespace LibraryApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class BookController : ControllerBase
    {
      private readonly BookServices _bookServices;
        public BookController(BookServices bookServices)
        {
            _bookServices = bookServices;
        }
        [HttpGet]
        public async Task<IActionResult> GetAllAsync()
        {
            var books = await _bookServices.GetAllAsync();
            return books == null ? NotFound() : Ok(books);
        }
        [HttpGet("{id}")]
        public async Task<IActionResult> GetByIdAsync(int id)
        {
            var book = await _bookServices.GetByIdAsync(id);
            return book == null ? NotFound() : Ok(book);
        }
        [HttpPost]
        public async Task<IActionResult> AddBook([FromBody] Book book)
        {
            await _bookServices.AddAsync(book);
            return Ok(book);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateBook(int id, [FromBody] Book book)
        {
            if (book == null)
                return BadRequest("Book is required");

            if (id != book.BookID)
                return BadRequest("ID mismatch");

            await _bookServices.UpdateAsync(book);
            return Ok(book);
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteAsync(int id)
        {
            await _bookServices.DeleteAsync(id);
            return Ok();
        }
    }
}
