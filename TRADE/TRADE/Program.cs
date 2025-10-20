//

// Clients(ClientCode, Company, Contact, Position, Address, City, Region, PostalCode, Country, Phone, Fax)
// Orders(OrderNumber, ClientCode, EmployeeNumber, OrderDate, ShipBefore, ShipDate, CourierNumber, Freight, Recipient, ShippingAddress, ShippingCity, ShippingRegion, ShippingPostalCode, ShippingCountry)
// OrderDetails(OrderNumber, ProductRef, UnitPrice, Quantity, Discount)
// Products(ProductRef, ProductName, SupplierNumber, CategoryCode, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOrdered, ReorderLevel)
// Suppliers(SupplierNumber, Company, Contact, Position, Address, City, Region, PostalCode, Country, Phone, Fax)
// Employees(EmployeeNumber, LastName, FirstName, Position, CourtesyTitle, BirthDate, HireDate, Address, City, Region, PostalCode, Country, HomePhone, Extension, Photo, Notes, ReportsTo)
// Categories(CategoryCode, CategoryName)
// Courier(CourierNumber, CourierName, Phone)

//Objective: Write SELECT queries that include projection, sorting, grouping, and joins.



// Entities
using System;
using System.ComponentModel;
using System.ComponentModel.Design;
using System.Drawing;
using System.Linq;
using System.Numerics;
using System.Reflection.Emit;
using System.Reflection.Metadata;
using static System.Net.Mime.MediaTypeNames;
using static System.Runtime.InteropServices.JavaScript.JSType;

public class Client
{
    public string ClientCode { get; set; }
    public string Company { get; set; }
    public string Contact { get; set; }
    public string Position { get; set; }
    public string Address { get; set; }
    public string City { get; set; }
    public string Region { get; set; }
    public string PostalCode { get; set; }
    public string Country { get; set; }
    public string Phone { get; set; }
    public string Fax { get; set; }
}

public class Order
{
    public int OrderNumber { get; set; }
    public string ClientCode { get; set; }
    public int EmployeeNumber { get; set; }
    public DateTime OrderDate { get; set; }
    public DateTime ShipBefore { get; set; }
    public DateTime? ShippedDate { get; set; }
    public int CourierNumber { get; set; }
    public decimal Freight { get; set; }
    public string Recipient { get; set; }
    public string ShipAddress { get; set; }
    public string ShipCity { get; set; }
    public string ShipRegion { get; set; }
    public string ShipPostalCode { get; set; }
    public string ShipCountry { get; set; }
}

public class OrderDetail
{
    public int OrderNumber { get; set; }
    public int ProductRef { get; set; }
    public decimal UnitPrice { get; set; }
    public int Quantity { get; set; }
    public decimal Discount { get; set; }
}

public class Product
{
    public int ProductRef { get; set; }
    public string ProductName { get; set; }
    public int SupplierNumber { get; set; }
    public int CategoryCode { get; set; }
    public string QuantityPerUnit { get; set; }
    public decimal UnitPrice { get; set; }
    public int UnitsInStock { get; set; }
    public int UnitsOrdered { get; set; }
    public int ReorderLevel { get; set; }
}

public class Supplier
{
    public int SupplierNumber { get; set; }
    public string Company { get; set; }
    public string Contact { get; set; }
    public string Position { get; set; }
    public string Address { get; set; }
    public string City { get; set; }
    public string Region { get; set; }
    public string PostalCode { get; set; }
    public string Country { get; set; }
    public string Phone { get; set; }
    public string Fax { get; set; }
}

public class Employee
{
    public int EmployeeNumber { get; set; }
    public string LastName { get; set; }
    public string FirstName { get; set; }
    public string Position { get; set; }
    public string CourtesyTitle { get; set; }
    public DateTime BirthDate { get; set; }
    public DateTime HireDate { get; set; }
    public string Address { get; set; }
    public string City { get; set; }
    public string Region { get; set; }
    public string PostalCode { get; set; }
    public string Country { get; set; }
    public string HomePhone { get; set; }
    public string Extension { get; set; }
    public string Photo { get; set; }
    public string Notes { get; set; }
    public int? ReportsTo { get; set; }
}

public class Category
{
    public int CategoryCode { get; set; }
    public string CategoryName { get; set; }
}

public class Courier
{
    public int CourierNumber { get; set; }
    public string CourierName { get; set; }
    public string Phone { get; set; }
}


class Program
{
    
    //------------Data source----------------//
    public static List<Client> Clients = new List<Client>
{
    new Client { ClientCode="123", Company="ACME", Contact="John Doe", Position="Owner", City="Paris", Country="France"},
    new Client { ClientCode="ALFKI", Company="Alfreds Futterkiste", Contact="Maria Anders", Position="Buyer", City="Berlin", Country="Germany"},
    new Client { ClientCode="456", Company="MegaCorp", Contact="Anna Smith", Position="Sales Manager", City="New York", Country="USA"},
    new Client { ClientCode="789", Company="XYZ Ltd", Contact="Paul Brown", Position="Owner", City="Paris", Country="France"},
    new Client { ClientCode="321", Company="Delta Inc", Contact="Laura White", Position="Sales Manager", City="London", Country="UK"},
    new Client { ClientCode="654", Company="Omega Ltd", Contact="James Black", Position="Buyer", City="Berlin", Country="Germany"},
    new Client { ClientCode="987", Company="Beta Corp", Contact="Emily Green", Position="Owner", City="Paris", Country="France"}
};

    public static List<Employee> Employees = new List<Employee>
{
    new Employee { EmployeeNumber=1, LastName="Fuller", FirstName="Nancy", Position="Salesperson", HireDate=new DateTime(1992,1,5), BirthDate=new DateTime(1968,1,15), Address="123 Main St", City="Paris", Region="Ile-de-France", PostalCode="75001", Country="France", CourtesyTitle="Ms.", HomePhone="01-2345678", Extension="101", Photo="", Notes="", ReportsTo=null },
    new Employee { EmployeeNumber=2, LastName="Peacock", FirstName="Margaret", Position="Sales Manager", HireDate=new DateTime(1993,4,10), BirthDate=new DateTime(1958,1,19), Address="45 Queen St", City="Berlin", Region="Berlin", PostalCode="10115", Country="Germany", CourtesyTitle="Ms.", HomePhone="030-123456", Extension="102", Photo="", Notes="", ReportsTo=null },
    new Employee { EmployeeNumber=3, LastName="Buchanan", FirstName="Steven", Position="HR Manager", HireDate=new DateTime(1994,6,15), BirthDate=new DateTime(1955,11,15), Address="78 King St", City="London", Region="Greater London", PostalCode="SW1A", Country="UK", CourtesyTitle="Mr.", HomePhone="020-987654", Extension="103", Photo="", Notes="", ReportsTo=null },
    new Employee { EmployeeNumber=4, LastName="Leverling", FirstName="Janet", Position="Salesperson", HireDate=new DateTime(1990,2,1), BirthDate=new DateTime(1963,7,27), Address="12 Rue Lafayette", City="Paris", Region="Ile-de-France", PostalCode="75009", Country="France", CourtesyTitle="Ms.", HomePhone="01-8765432", Extension="104", Photo="", Notes="", ReportsTo=2 },
    new Employee { EmployeeNumber=5, LastName="Suyama", FirstName="Michael", Position="Operations Manager", HireDate=new DateTime(1993,9,12), BirthDate=new DateTime(1969,1,30), Address="23 Harbor Rd", City="Tokyo", Region="Tokyo", PostalCode="100-0001", Country="Japan", CourtesyTitle="Mr.", HomePhone="03-1234567", Extension="105", Photo="", Notes="", ReportsTo=null }
};
    public static List<Product> Products = new List<Product>
{
    new Product { ProductRef=1, ProductName="Chai", CategoryCode=1, UnitPrice=18, UnitsInStock=39, UnitsOrdered=10 },
    new Product { ProductRef=2, ProductName="Chang", CategoryCode=1, UnitPrice=19, UnitsInStock=17, UnitsOrdered=5 },
    new Product { ProductRef=3, ProductName="Aniseed Syrup", CategoryCode=2, UnitPrice=55, UnitsInStock=13, UnitsOrdered=120 },
    new Product { ProductRef=4, ProductName="Chef Anton's Cajun Seasoning", CategoryCode=2, UnitPrice=22, UnitsInStock=53, UnitsOrdered=200 },
    new Product { ProductRef=5, ProductName="Chef Anton's Gumbo Mix", CategoryCode=2, UnitPrice=21, UnitsInStock=0, UnitsOrdered=0 },
    new Product { ProductRef=6, ProductName="Grandma's Boysenberry Spread", CategoryCode=3, UnitPrice=25, UnitsInStock=120, UnitsOrdered=150 },
    new Product { ProductRef=7, ProductName="Uncle Bob's Organic Dried Pears", CategoryCode=3, UnitPrice=60, UnitsInStock=25, UnitsOrdered=80 },
    new Product { ProductRef=8, ProductName="Northwoods Cranberry Sauce", CategoryCode=3, UnitPrice=52, UnitsInStock=30, UnitsOrdered=90 },
    new Product { ProductRef=9, ProductName="Mishi Kobe Niku", CategoryCode=4, UnitPrice=97, UnitsInStock=20, UnitsOrdered=10 },
    new Product { ProductRef=10, ProductName="Ikura", CategoryCode=5, UnitPrice=31, UnitsInStock=25, UnitsOrdered=0 }
};

    public static List<Category> Categories = new List<Category>
{
    new Category { CategoryCode=1, CategoryName="Beverages" },
    new Category { CategoryCode=2, CategoryName="Grocery" },
    new Category { CategoryCode=3, CategoryName="Jams" },
    new Category { CategoryCode=4, CategoryName="Meat" },
    new Category { CategoryCode=5, CategoryName="Seafood" },
    new Category { CategoryCode=6, CategoryName="Produce" },
    new Category { CategoryCode=7, CategoryName="Dairy" },
    new Category { CategoryCode=8, CategoryName="Snacks" }
};

    public static List<Supplier> Suppliers = new List<Supplier>
{
    new Supplier { SupplierNumber=1, Company="Exotic Liquids", City="London", Country="UK" },
    new Supplier { SupplierNumber=2, Company="New Orleans Cajun Delights", City="New Orleans", Country="USA" },
    new Supplier { SupplierNumber=3, Company="Grandma Kelly's Homestead", City="Ann Arbor", Country="USA" },
    new Supplier { SupplierNumber=4, Company="Tokyo Traders", City="Tokyo", Country="Japan" },
    new Supplier { SupplierNumber=5, Company="Cooperativa de Quesos", City="Paris", Country="France" }
};

    public static List<Courier> Couriers = new List<Courier>
{
    new Courier { CourierNumber=1, CourierName="Speedy Express" },
    new Courier { CourierNumber=2, CourierName="United Package" },
    new Courier { CourierNumber=3, CourierName="Federal Shipping" }
};

    public static List<Order> Orders = new List<Order>
{
    new Order { OrderNumber=10248, ClientCode="123", EmployeeNumber=1, OrderDate=new DateTime(1996,7,4), ShipBefore=new DateTime(1996,8,1), CourierNumber=1 },
    new Order { OrderNumber=10249, ClientCode="ALFKI", EmployeeNumber=2, OrderDate=new DateTime(1996,7,5), ShipBefore=new DateTime(1996,8,2), CourierNumber=2 },
    new Order { OrderNumber=10250, ClientCode="456", EmployeeNumber=3, OrderDate=new DateTime(1996,7,8), ShipBefore=new DateTime(1996,8,5), CourierNumber=1 },
    new Order { OrderNumber=10251, ClientCode="123", EmployeeNumber=4, OrderDate=new DateTime(1996,7,10), ShipBefore=new DateTime(1996,8,10), CourierNumber=3 },
    new Order { OrderNumber=10252, ClientCode="654", EmployeeNumber=5, OrderDate=new DateTime(1996,7,12), ShipBefore=new DateTime(1996,8,15), CourierNumber=2 }
};

    public static List<OrderDetail> OrderDetails = new List<OrderDetail>
{
    new OrderDetail { OrderNumber=10248, ProductRef=1, UnitPrice=18, Quantity=12, Discount=0 },
    new OrderDetail { OrderNumber=10248, ProductRef=3, UnitPrice=55, Quantity=10, Discount=0 },
    new OrderDetail { OrderNumber=10249, ProductRef=2, UnitPrice=19, Quantity=5, Discount=0.1m },
    new OrderDetail { OrderNumber=10250, ProductRef=4, UnitPrice=22, Quantity=8, Discount=0 },
    new OrderDetail { OrderNumber=10250, ProductRef=6, UnitPrice=25, Quantity=20, Discount=0.05m },
    new OrderDetail { OrderNumber=10251, ProductRef=3, UnitPrice=55, Quantity=100, Discount=0 },
    new OrderDetail { OrderNumber=10251, ProductRef=7, UnitPrice=60, Quantity=50, Discount=0.05m },
    new OrderDetail { OrderNumber=10252, ProductRef=8, UnitPrice=52, Quantity=75, Discount=0 }
};


    static void Main(string[] args)
    {
  
        // 1:Number of orders placed by client 123
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("1:Number of orders placed by client 123");
        int count = Orders
        .Where(o => o.ClientCode == "123")
        .Count();
        Console.WriteLine($"Count: {count}");

        //2: List of employees hired in 1992
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("List of employees hired in 1992");
        var q2=Employees.Where(e=>e.HireDate.Year==1992)
            .Select(e=>e.FirstName+"  " + e.LastName).ToList();
        foreach(var item in q2)
        {
            Console.WriteLine(item);
        }
        //3: List of employees hired between 1993 and 1994
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("List of employees hired between 1993 and 1994");
        var q3=Employees.Where (e=>e.HireDate.Year >= 1993 && e.HireDate.Year <= 1994)
            .Select(e => e.FirstName + "  " + e.LastName).ToList();
        foreach (var item in q3)
        {
            Console.WriteLine(item);
        }
        //4: List of employees born in the month of January  
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("4:List of employees born in the month of January");
        var q4=Employees.Where(e=>e.BirthDate.Month==1)
            .Select(e => e.FirstName + "  " + e.LastName).ToList();
        foreach (var item in q4)    
         {
            Console.WriteLine(item);
        }

        //5: Show the total number of different products that belong to categories 2, 3, 4, 5, or 8
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("5:Show the total number of different products that belong to categories 2, 3, 4, 5, or 8");
        int q5=Products.Where(p=>p.CategoryCode==2 || p.CategoryCode==3 || p.CategoryCode==4 || p.CategoryCode==5 || p.CategoryCode==8)
            .Select(p=>p.ProductRef)
            .Count();
        Console.WriteLine($"Count: {q5}");

        //6: List of products (reference, name, and unit price) with prices between 50 and 80, sorted by price and product name
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("6:List of products (reference, name, and unit price) with prices between 50 and 80, sorted by price and product name");
         var q6=Products.Where(p=>p.UnitPrice>=50 && p.UnitPrice<=80)
            .OrderBy(p=>p.UnitPrice)
            .ThenBy(p=>p.ProductName)
            .Select(p=> new {p.ProductRef,p.ProductName,p.UnitPrice}).ToList();
        foreach(var item in q6)
         {
            Console.WriteLine($"ProductRef: {item.ProductRef}, ProductName: {item.ProductName}, UnitPrice: {item.UnitPrice}");
        }
        //7: Show the total number of suppliers who live in France, USA, or Germany
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("7:Show the total number of suppliers who live in France, USA, or Germany");
        var q7=Suppliers.Where(s=>s.Country=="France" || s.Country=="USA" || s.Country=="Germany")
            .Select(s=>s.SupplierNumber)
            .Count();
        Console.WriteLine($"Count: {q7}");
        //8: Show the list of employees (last name, first name, position) whose position contains "Manager" of something (e.g., "Sales Manager", "HR Manager", etc.)
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("8:Show the list of employees (last name, first name, position) whose position contains 'Manager' of something (e.g., 'Sales Manager', 'HR Manager', etc.)");
        var q8=Employees.Where(e=>new[] { "Manager", "Sales Manager", "HR Manager" }.Contains(e.Position))
            .Select(e=> new {e.LastName,e.FirstName,e.Position}).ToList();
        foreach(var item in q8)
        {
            Console.WriteLine($"LastName: {item.LastName}, FirstName: {item.FirstName}, Position: {item.Position}");
        }
        //9: Show the total amount ordered for all orders with order number less than or equal to 10270 (also show the order number)
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("9:Show the total amount ordered for all orders with order number less than or equal to 10270 (also show the order number)");
        var q9=OrderDetails.Where(od=>od.OrderNumber<=10270)
            .GroupBy(od=>od.OrderNumber)
            .Select(g=> new { OrderNumber=g.Key, TotalAmount=g.Sum(od=>od.UnitPrice * od.Quantity * (1 - od.Discount))}).ToList();
        foreach(var item in q9)
        {
                       Console.WriteLine($"OrderNumber: {item.OrderNumber}, TotalAmount: {item.TotalAmount}");
        }
        Console.WriteLine("-----------------------------------------");
        //10: Show the lowest product price for all products in categories 2, 4, and 5
        //this is the solution for the lowest price between the categories 2,4 and 5
        Console.WriteLine("10:Show the lowest product price for all products in categories 2, 4, and 5");
        var q10=Products.Where(p=>p.CategoryCode==2 || p.CategoryCode==4 || p.CategoryCode==5)
            .Select(p=>p.UnitPrice)
            .Min();
        Console.WriteLine($"Lowest Price: {q10}");
        // "This is the solution for the lowest price in each of the categories 2, 4, and 5."
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("10-1 the lowest price in each of the categories 2, 4, and 5.");
        var q10_1=Products.Where(p=>p.CategoryCode==2 || p.CategoryCode==4 || p.CategoryCode==5)
            .GroupBy(p=>p.CategoryCode)
            .Select(g=> new { CategoryCode=g.Key, LowestPrice=g.Min(p=>p.UnitPrice)}).ToList();
        foreach(var item in q10_1)
        {
                       Console.WriteLine($"CategoryCode: {item.CategoryCode}, LowestPrice: {item.LowestPrice}");
        }
        // 11: Number of different items per supplier
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("11: Number of different items per supplier");

        var q11 = Products
            .Join(Suppliers,
                  p => p.SupplierNumber,
                  s => s.SupplierNumber,
                  (p, s) => new { s.SupplierNumber, s.Company })
            .GroupBy(x => new { x.SupplierNumber, x.Company })
            .Select(g => new { g.Key.SupplierNumber, g.Key.Company, NumberOfItems = g.Count() })
            .ToList();

        foreach (var item in q11)
        {
            Console.WriteLine($"Supplier: {item.Company} (ID: {item.SupplierNumber}), Number of Items: {item.NumberOfItems}");
        }
        Console.WriteLine("-----------------------------------------");
        //12: Number of items per order
        Console.WriteLine("12: Number of items per order");
        var q12 = OrderDetails
            .GroupBy(od => od.OrderNumber)
            .Select(g => new { OrderNumber = g.Key, NumberOfItems = g.Count() })
            .ToList();
        foreach (var item in q12)
        {
                       Console.WriteLine($"OrderNumber: {item.OrderNumber}, Number of Items: {item.NumberOfItems}");
        }
        Console.WriteLine("-----------------------------------------");
        //13 Show the total amount ordered (without considering discounts) for all orders with order number greater than 150 (also show the order number)
        Console.WriteLine("13: Show the total amount ordered (without considering discounts) for all orders with order number greater than 150 (also show the order number)");
        var q13 = OrderDetails
                 .Where(od => od.OrderNumber > 150)
                 .GroupBy(od => od.OrderNumber)  // per order groeperen
                 .Select(g => new {
                  OrderNumber = g.Key,
                  TotalAmount = g.Sum(od => od.UnitPrice * od.Quantity)})
                 .ToList();

        foreach (var item in q13)
        {
            Console.WriteLine($"Order {item.OrderNumber}: {item.TotalAmount}");
        }


        Console.WriteLine("-----------------------------------------");
        //13-1 Total amount for all orders > 15
        Console.WriteLine("13-1: Total amount for all orders > 150");
        var totalAmount = OrderDetails
            .Where(od => od.OrderNumber > 150)
            .Sum(od => od.UnitPrice * od.Quantity);

        Console.WriteLine($"Total amount for all orders > 150: {totalAmount}");

        Console.WriteLine("-----------------------------------------");
        //14: Number of items per order, for orders with numbers after 150
        Console.WriteLine("14: Number of items per order, for orders with numbers after 150");
        var q14 = OrderDetails
            .Where(od => od.OrderNumber > 150)
            .GroupBy(od => od.OrderNumber)
            .Select(g => new { OrderNumber = g.Key, NumberOfItems = g.Count() })
            .ToList();
        foreach (var item in q14)
         {
            Console.WriteLine($"OrderNumber: {item.OrderNumber}, Number of Items: {item.NumberOfItems}");
        }
        //16: Show for each product category (category_code) the total number of units ordered (use the "units_ordered" field in the Products table)
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("16: Total number of units ordered per category");

        var q16 = Products
            .GroupBy(p => p.CategoryCode)
            .Select(g => new {
                CategoryCode = g.Key,
                TotalUnitsOrdered = g.Sum(p => p.UnitsOrdered)
            });

        foreach (var item in q16)
        {
            Console.WriteLine($"Category {item.CategoryCode}: {item.TotalUnitsOrdered} units ordered");
        }
        Console.WriteLine("-----------------------------------------");
        //17: Limit to category codes less than 5 and total units ordered greater than 100
        Console.WriteLine("17: Total number of units ordered per category (CategoryCode < 5 and TotalUnitsOrdered > 100)");
        var q17 = Products
            .Where(p => p.CategoryCode < 5)
            .GroupBy(p => p.CategoryCode)
            .Select(g => new {
                CategoryCode = g.Key,
                TotalUnitsOrdered = g.Sum(p => p.UnitsOrdered)
            })
            .Where(result => result.TotalUnitsOrdered > 100);
        foreach (var item in q17)
        {
            Console.WriteLine($"Category {item.CategoryCode}: {item.TotalUnitsOrdered} units ordered");
        }   
        Console.WriteLine("-----------------------------------------");
        //18: Average age of employees by their position
        Console.WriteLine("18: Average age of employees by their position");
        var q18 = Employees
            .GroupBy(e => e.Position)
            .Select(g => new {
                Position = g.Key,
                AverageAge = g.Average(e => DateTime.Now.Year - e.BirthDate.Year)
            });
        foreach (var item in q18)
        {
                       Console.WriteLine($"Position: {item.Position}, Average Age: {item.AverageAge}");
        }
        //19: Find countries for which we have 3 or more clients who are "Owner", "Buyer", or "Sales Manager"
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("19: Countries with 3 or more clients who are 'Owner', 'Buyer', or 'Sales Manager'");
        var q19 = Clients
            .Where(c => new[] { "Owner", "Buyer", "Sales Manager" }.Contains(c.Position))
            .GroupBy(c => c.Country)
            .Select(g => new {
                Country = g.Key,
                ClientCount = g.Count()
            })
            .Where(result => result.ClientCount >= 3);
        foreach (var item in q19)
        {
                       Console.WriteLine($"Country: {item.Country}, Client Count: {item.ClientCount}");
        }

        Console.WriteLine("-----------------------------------------");
        //20: List of clients (company name, contact, position) in cities where there is at least one supplier
        Console.WriteLine("20: List of clients (company name, contact, position) in cities where there is at least one supplier");
        var citiesWithSuppliers = Suppliers
            .GroupBy(s => s.City)
            .Where(g => g.Count() >= 1) 
            .Select(g => g.Key)
            .ToList();

        var q20_1 = Clients
            .Where(c => citiesWithSuppliers.Contains(c.City))
            .Select(c => new { c.Company, c.Contact, c.Position })
            .ToList();


        foreach (var item in q20_1)
            {
            Console.WriteLine($"Company: {item.Company}, Contact: {item.Contact}, Position: {item.Position}");
        }

      
        //21: Select all orders (order number, order date, client Code) placed by the client with code "ALFKI"
        Console.WriteLine(  "-----------------------------------------");
        Console.WriteLine("21: Select all orders (order number, order date, client Code) placed by the client with code 'ALFKI'");
        var q21 = Orders
            .Where(o => o.ClientCode == "ALFKI")
            .Select(o => new { o.OrderNumber, o.OrderDate, o.ClientCode })
            .ToList();
        foreach (var item in q21)
        {
                       Console.WriteLine($"OrderNumber: {item.OrderNumber}, OrderDate: {item.OrderDate.ToShortDateString()}, ClientCode: {item.ClientCode}");
        }
        //22: Show for each client (client_code) the number of orders placed with a French employee
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("22: Show for each client (client_code) the number of orders placed with a French employee");
        var frenchEmployees = Employees
            .Where(e => e.Country == "France")
            .Select(e => e.EmployeeNumber)
            .ToList();
        var q22 = Orders
            .Where(o => frenchEmployees.Contains(o.EmployeeNumber))
            .GroupBy(o => o.ClientCode)
            .Select(g => new { ClientCode = g.Key, OrderCount = g.Count() })
            .ToList();
        foreach (var item in q22)
        {
            Console.WriteLine($"ClientCode: {item.ClientCode}, OrderCount: {item.OrderCount}");
        }
        //23: Orders handled by the salesperson "Fuller"
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("23: Orders handled by the salesperson 'Fuller'");
        var q23 = Orders
             .Join(Employees.Where(e => e.LastName == "Fuller" ),
                   o => o.EmployeeNumber,
                   e => e.EmployeeNumber,
                   (o, e) => o)
              .Select(g=>new { g.OrderNumber, g.ClientCode })
              .ToList();  
        foreach (var item in q23)
        {
            Console.WriteLine($"OrderNumber: {item.OrderNumber}, ClientCode: {item.ClientCode}");
        }
        //24: Show the number of items per order (with order number) for orders containing more than 5 items
        Console.WriteLine("-----------------------------------------"); 
        Console.WriteLine("24: Show the number of items per order (with order number) for orders containing more than 5 items");
        var q24 = OrderDetails
      .GroupBy(od => od.OrderNumber)
      .Select(g => new
      {
          OrderNumber = g.Key,
          TotalItems = g.Sum(od => od.Quantity)
      })
      .Where(result => result.TotalItems > 5)
      .ToList();

        foreach (var item in q24)
        {
            Console.WriteLine($"OrderNumber: {item.OrderNumber}, Total Items: {item.TotalItems}");
        }

        Console.WriteLine("-----------------------------------------");
        //25: Show for each product (product reference, product name) in category "2" (use the category code stored as text)
        //the total number of products ordered (use the quantity in the order details table)
         Console.WriteLine("25: Show for each product (product reference, product name) in category '2' the total number of products ordered");
        var q25 = Products
            .Where(p => p.CategoryCode == 2)
            .GroupJoin(OrderDetails,
                       p => p.ProductRef,
                       od => od.ProductRef,
                       (p, ods) => new { p.ProductRef, p.ProductName, TotalOrdered = ods.Sum(od => od.Quantity) })
            .ToList();
        foreach (var item in q25)
        {
            Console.WriteLine($"ProductRef: {item.ProductRef}, ProductName: {item.ProductName}, TotalOrdered: {item.TotalOrdered}");
        }
        //26: Note: do not display products for which fewer than 100 units have been ordered
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("26: Show for each product (product reference, product name) in category '2' the total number of products ordered (only if TotalOrdered >= 100)");
        var q26 = Products
            .Where(p => p.CategoryCode == 2)
            .GroupJoin(OrderDetails,
                       p => p.ProductRef,
                       od => od.ProductRef,
                       (p, ods) => new { p.ProductRef, p.ProductName, TotalOrdered = ods.Sum(od => od.Quantity) })
            .Where(result => result.TotalOrdered >= 100)
            .ToList();
        foreach (var item in q26)
        {           
         Console.WriteLine($"ProductRef: {item.ProductRef}, ProductName: {item.ProductName}, TotalOrdered: {item.TotalOrdered}");
        }
        Console.WriteLine("-----------------------------------------");
        //27: Select all products (product number, product name, category name) in category 3 (category code stored as text)
        Console.WriteLine("27: Select all products (product number, product name, category name) in category 3");

        var q27 = Products
            .Where(p => p.CategoryCode == 3)
            .Join(Categories,
                  p => p.CategoryCode,
                  c => c.CategoryCode,
                  (p, c) => new { p.ProductRef, p.ProductName, c.CategoryName })
            .ToList();
        foreach (var item in q27)
        {
                       Console.WriteLine($"ProductRef: {item.ProductRef}, ProductName: {item.ProductName}, CategoryName: {item.CategoryName}");
        }
        Console.WriteLine("-----------------------------------------");
        //28: Show for each employee (employee number) the number of orders handled
        Console.WriteLine("28: Show for each employee (employee number) the number of orders handled");
       var q28 = Orders
             .GroupBy(e => e.EmployeeNumber)
                .Select(g => new { EmployeeNumber = g.Key, OrderCount = g.Count() })
                .ToList();
        foreach (var item in q28)
        {
            Console.WriteLine($"EmployeeNumber: {item.EmployeeNumber}, OrderCount: {item.OrderCount}");
        }

        Console.WriteLine("-----------------------------------------");
        //29: Show for each client (company name) the total number of orders to be delivered after May 31, 1994 (use the "ship_before" field). If the number is less than 10, do not display the client
        Console.WriteLine("29: Show for each client (company name) the total number of orders to be delivered after May 31, 1994");
        var q29 = Orders
            .Where(o => o.ShipBefore > new DateTime(1994, 5, 31))
            .GroupBy(o => o.ClientCode)
            .Join(Clients,
                  g => g.Key,
                  c => c.ClientCode,
                  (g, c) => new { c.Company, OrderCount = g.Count() })
            .Where(result => result.OrderCount >= 10)
            .ToList();
          foreach (var item in q29)
        {
              Console.WriteLine($"Company: {item.Company}, OrderCount: {item.OrderCount}");
        }
        //30: Show for each courier (courier number, courier name) the number of orders handled
        Console.WriteLine("-----------------------------------------");
        Console.WriteLine("30: Show for each courier (courier number, courier name) the number of orders handled");
        var q30 = Orders
            .GroupBy(o => o.CourierNumber)
            .Join(Couriers,
                  g => g.Key,
                  c => c.CourierNumber,
                  (g, c) => new { c.CourierNumber, c.CourierName, OrderCount = g.Count() })
            .ToList();
        foreach (var item in q30)
        {
            Console.WriteLine($"CourierNumber: {item.CourierNumber}, CourierName: {item.CourierName}, OrderCount: {item.OrderCount}");
        }


    }

}
