using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Banking_System_Simulation_using_C__OOP
{

    //Define a Client class with the following attributes:

    //CIN(ID number)

    //LastName

    //FirstName

    //Phone

    public class Client
    {
        [Required]
        public string CIN { get; set; }
        [Required,MaxLength(50)]
        public string LastName { get; set; }
        [Required,MaxLength(50)]
        public string FirstName { get; set; }
       [Required,Phone]
        public string Phone { get; set; }
        //Define a constructor that initializes all the attributes.
        public Client(string cin, string lastName, string firstName, string phone)
        {
            CIN = cin;
            LastName = lastName;
            FirstName = firstName;
            Phone = phone;
        }
        //Define another constructor that initializes only CIN, LastName, and FirstName.
        public Client(string cin, string lastName, string firstName)
        {
            CIN = cin;
            LastName = lastName;
            FirstName = firstName;
        }
        //Define the method Display() that prints the information of the current client.
        public void Display()
        {
            Console.WriteLine($"CIN: {CIN}, LastName: {LastName}, FirstName: {FirstName}, Phone: {Phone}");
        }

    }
}
