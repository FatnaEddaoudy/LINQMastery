//----------------Objective:--------------------
//Create an abstract class.
//Derive an abstract class.
//Implement an abstract method.

//------------------Statement:--------------------
//***Consider the abstract class Employee characterized by the following attributes:
//EmployeeID
//LastName
//FirstName
//DateOfBirth

//The Employee class must have the following methods:
//An initialization constructor
//Properties for each attribute
//The ToString() method
//An abstract method GetSalary()

//***An Worker(Worker) is an employee characterized by their date of joining the company.
//All workers share a common value called SMIG = 2500 DH.

//The worker’s monthly salary is calculated as:
//Salary = SMIG + (Seniority in years) * 100
//The salary cannot exceed SMIG * 2.

//A Manager is an employee characterized by an index.
//The manager’s salary depends on their index:
//1 → 13000 DH per month
//2 → 15000 DH per month
//3 → 17000 DH per month
//4 → 20000 DH per month

//A Patron (Boss) is an employee characterized by a turnover and a percentage.
//The turnover is shared among all bosses.
//The annual salary is calculated as:
//Salary = Turnover * Percentage / 100

//--------------Tasks:------------------------
//Create the abstract class Employee.
//Create the classes Worker, Manager, and Boss that inherit from the Employee class, including constructors and ToString() methods for each.
//Implement the GetSalary() method to calculate the salary for each class.