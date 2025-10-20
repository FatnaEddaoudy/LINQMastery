using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Models
{
    public class Member
    {
        public int MemeberId { get; set; }
        [Required(ErrorMessage = "First name is required")]
        public string FirstName { get; set; }
        [Required(ErrorMessage = "First name is required")]
        public string LastName { get; set; }
        [DataType(DataType.Date)]   
        [Required(ErrorMessage = "Member since date is required")]
        public DateTime JoinDate { get; set; }
        [Required(ErrorMessage = "Email is required")]
        [EmailAddress(ErrorMessage = "Invalid email address")]
        public string Email { get; set; }
        [Phone(ErrorMessage = "Invalid phone number")]
        public string PhoneNumber { get; set; }
        [Required(ErrorMessage = "Address is required")]
        public int AddressId { get; set; }
        public Address? Address { get; set; }
        public DateTime DateOfBirth { get; set; }
        public int BorrowingFrequency { get; set; }
        public int UserId { get; set; }
        public User? User { get; set; } // optional
        public ICollection<Borrowing> Borrowings { get; set; } = new List<Borrowing>();
    }
}
