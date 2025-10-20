using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Models
{
    public class Author
    {
        public int AuthorId { get; set; }
        [Required(ErrorMessage = "the Name Author is Required") ]
        public string Name { get; set; } 
        public int birthyear { get; set; }
        public string Country { get; set; }
        public ICollection<Book> Books { get; set; } = new List<Book>();

    }
}
