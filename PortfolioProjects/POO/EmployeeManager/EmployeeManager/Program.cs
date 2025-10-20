using EmployeeManager;
using System.IO;

class Program
{
    static void Main()
    {

        Boss.Turnover = 1000000;//Static property

        // Create a list of employees (polymorphism)
        // Abstract class:Employee cannot be instantiated directly
        List<Employee> employees = new List<Employee>
            {
                new Worker(1, "Smith", "John", new DateTime(1990, 5, 12), new DateTime(2015, 3, 1)),
                new Worker(2, "Lopez", "Maria", new DateTime(1995, 10, 22), new DateTime(2019, 6, 15)),
                new Manager(3, "Jones", "Alice", new DateTime(1985, 2, 20), 3),
                new Manager(4, "Brown", "David", new DateTime(1980, 8, 9), 1),
                new Boss(5, "Wilson", "Robert", new DateTime(1970, 8, 10), 5),
                new Boss(6, "Garcia", "Laura", new DateTime(1975, 3, 25), 3)
            };

        Console.WriteLine("========== Company Employees ==========\n");

        // Display all employees using ToString()
        foreach (var emp in employees)
        {
            // Polymorphism: Calls the overridden ToString() method
            Console.WriteLine(emp.ToString());//  Displays each employee with details + salary
        }

        Console.WriteLine("\n======================================");
    }


}
