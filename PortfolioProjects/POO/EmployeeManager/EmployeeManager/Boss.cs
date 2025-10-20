using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EmployeeManager
{
    public class Boss : Employee
    {
        public static double Turnover { get; set; }
        public double Percentage { get; set; }

        public Boss(int id, string last, string first, DateTime dob, double percentage)
            : base(id, last, first, dob)
        {
            Percentage = percentage;
        }

        public override double GetSalary()
        {
            // Annual salary
            return Turnover * Percentage / 100;
        }

        public override string ToString()
        {
            return base.ToString() + $", Percentage: {Percentage}%, Annual Salary: {GetSalary()} DH";
        }
    }
}
