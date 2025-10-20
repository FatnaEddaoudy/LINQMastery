using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EmployeeManager
{
    //Inheritance Manager derive from Employee
    public class Manager : Employee
    {
        public int Index { get; set; }

        public Manager(int id, string last, string first, DateTime dob, int index)
            : base(id, last, first, dob)
        {
            Index = index;
        }

        public override double GetSalary()
        {
            return Index switch
            {
                1 => 13000,
                2 => 15000,
                3 => 17000,
                4 => 20000,
                _ => 0
            };
        }

        public override string ToString()
        {
            return base.ToString() + $", Index: {Index}, Salary: {GetSalary()} DH";
        }
    }
}
