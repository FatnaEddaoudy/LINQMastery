using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Simple_Member_Management_System.Models
{
    public class Member
    {
        public int Id { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string Address { get; set; }
        public int Age { get; set; }
        public Gender Gender { get; set; }
        public Member() { } // ✅ allows creating empty objects
        public Member(int id, string firstName, string lastName, string address, int age, Gender gender)
        {
            Id = id;
            FirstName = firstName;
            LastName = lastName;
            Address = address;
            Age = age;
            Gender = gender;
        }

    }

}
