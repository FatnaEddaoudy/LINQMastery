using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EmployeeManager
{

    //Inheritance Worker derive from Employee
    public class Worker : Employee
    {
        public DateTime DateOfJoining { get; set; }
        public const double SMIG = 2500;

        public Worker(int id, string last, string first, DateTime dob, DateTime joining)
            : base(id, last, first, dob)
        {
            DateOfJoining = joining;
        }

        public override double GetSalary()
        {
            int seniority = DateTime.Now.Year - DateOfJoining.Year;
            if (DateTime.Now.Month < DateOfJoining.Month ||
                (DateTime.Now.Month == DateOfJoining.Month && DateTime.Now.Day < DateOfJoining.Day))
            {
                seniority--;
            }

            double salary = SMIG + (seniority * 100);
            if (salary > SMIG * 2)
                salary = SMIG * 2;

            return salary;
        }

        public override string ToString()
        {
            return base.ToString() + $", Joined: {DateOfJoining.ToShortDateString()}, Salary: {GetSalary()} DH";
        }
    }
}
