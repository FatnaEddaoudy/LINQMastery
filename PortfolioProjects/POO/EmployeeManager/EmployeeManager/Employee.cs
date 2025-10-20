using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EmployeeManager
{
    // Abstract class Employee
    public abstract class Employee
    {
        public int EmployeeID { get; set; }
        public string LastName { get; set; }
        public string FirstName { get; set; }
        public DateTime DateOfBirth { get; set; }

        // --- Constructor ---
        public Employee(int employeeID, string lastName, string firstName, DateTime dateOfBirth)
        {
            EmployeeID = employeeID;
            LastName = lastName;
            FirstName = firstName;
            DateOfBirth = dateOfBirth;
        }

   
        public abstract double GetSalary();

        // --- ToString() ---
        public override string ToString()
        {
            return $"ID: {EmployeeID}, Name: {FirstName} {LastName}, DOB: {DateOfBirth.ToShortDateString()}";
        }

    }
}
