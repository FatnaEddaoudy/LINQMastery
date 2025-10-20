using LibraryData.Models;
using LibraryData.Repositories;
using LibraryServices.Services;
using Microsoft.AspNetCore.Mvc;
using System.Net;
using static System.Reflection.Metadata.BlobBuilder;

namespace LibraryApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AuthorController : ControllerBase
    {
        private readonly AuthorServices _authorServices;
        public AuthorController(AuthorServices authorServices)
        {
            _authorServices = authorServices;
        }
        [HttpGet]
        public async Task<IActionResult> GetAllAuthorAsysnc()
        {
            var Authors = await _authorServices.GetAllAuthorAsysnc();
            return Authors == null ? NotFound() : Ok(Authors);
        }
        [HttpGet("id")]
        public async Task<IActionResult> GetAutorBjIdAsync(int id)
        {
            var Author = await _authorServices.GetAutorBjIdAsync(id);
            return Author == null ? NotFound() : Ok(Author);
        }
        [HttpPost]
        public async Task AddAuthorAsync(Author author)
        {
            await _authorServices.AddAuthorAsync(author);
        }
        [HttpDelete("id")]
        public async Task DeleteAuthorAsync(int id)
        {
            await _authorServices.DeleteAuthorAsync(id);
        }
        [HttpPut]
        public async Task<ActionResult> UpdateAuthorAsync(int id, Author author)
        {
            if (author == null)
                return BadRequest("Author is required");

            if (id != author.AuthorId)
                return BadRequest("ID mismatch");

            await _authorServices.UpdateAuthorAsync(author);
            return Ok(author);
        }


    }

}
