using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Models
{
    public class Borrowing
    {
        public int BorrowId { get; set; }
        [Required(ErrorMessage = "Member is required")]
        public int MemberId { get; set; }
        public Member? Member { get; set; }
        [Required(ErrorMessage = "Book is required")]
        public int BookId { get; set; }
        public Book? Book { get; set; }
        [DataType(DataType.Date)]
        [Required(ErrorMessage = "Member since date is required")]
        public DateTime BorrowDate { get; set; }
        [DataType(DataType.Date)]
        [Required(ErrorMessage = "Member since date is required")]
        public DateTime? ReturnDate { get; set; }
        [DataType(DataType.Date)]
        [Required(ErrorMessage = "Member since date is required")]
        public DateTime DueDate { get; set; }
        public bool Islate { get; set; }
    }
}
