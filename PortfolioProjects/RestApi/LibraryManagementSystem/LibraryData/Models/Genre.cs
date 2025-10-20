using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Models
{
    public class Genre
    {
        public int GenreId { get; set; }
        [Required(ErrorMessage = "Genre name is required")]
        [MaxLength(200, ErrorMessage = "Genre name cannot exceed 200 characters")]
        public string Name { get; set; }
        [MaxLength(250, ErrorMessage = "Genre name cannot exceed 250 characters")]
        public string Description { get; set; } 
        public ICollection<Book> Books { get; set; } = new List<Book>();
    }
}
