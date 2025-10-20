using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Models
{
    public class Book
    {
        public int BookID { get; set; }
        [Required(ErrorMessage = "the Title is Required")]
        public string Title { get; set; }
        [Required(ErrorMessage = "the Author is Required")]
        public string? PhotoUrl { get; set; }
        public int AuthorId { get; set; }
        public Author? Author { get; set; }
        [Required(ErrorMessage = "the Genre is Required")]
        public int GenreId { get; set; }
        public Genre? Genre { get; set; }
        public int PublishedYear { get; set; }
        [Required(ErrorMessage = "the ISBN is Required")]
        public string ISBN { get; set; }
        public int Pages { get; set; }
        [Required(ErrorMessage = "the Copier Available is Required")]
        public int CopierAvailable { get; set; }
        public ICollection<Borrowing> Borrowings { get; set; } = new List<Borrowing>();

    }
}
