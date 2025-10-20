using System.ComponentModel;
using System.Net;
using System.Reflection.Emit;

//Objective: Write SELECT queries involving projection, sorting, grouping, and joins.

//SalesRepresentative(RepCode, LastName, FirstName)
//Customer(CustomerCode, LastName, FirstName, Address, PostalCode, City)
//Apartment(Ref, Area, SalePrice, Sector, RepCode, CustomerCode)

//Write SQL queries to display:

//The list of customers sorted alphabetically

//The average apartment price by sector

//The number of apartments per sector for sectors that have more than 10 apartments

//The number of apartments whose area is greater than 80 m² per sector

//The maximum apartment price by sector, but only for sectors with more than 10 apartments

//The list of customers and the apartments they have rented

//The list of apartments located in Hivernage and managed by Fadoua ALAMI

//The number of customers from Fès per sector





class SalesRepresentative
{
    public string RepCode { get; set; }
    public string LastName { get; set; }
    public string FirstName { get; set; }
}

public class Customer
{
    public string CustomerCode { get; set; }
    public string LastName { get; set; }
    public string FirstName { get; set; }
    public string Address { get; set; }
    public int PostalCode { get; set; }
    public string City { get; set; }
}

public class Apartment
{
    public int Ref { get; set; }
    public string Area { get; set; }
    public decimal SalePrice { get; set; }
    public string Sector { get; set; }
    public string RepCode { get; set; }
    public string CustomerCode { get; set; }
}
class Program
{
    static void Main()
    {

        //--------------------------Data Source------------------------------------
        // --- Sample Sales Representatives ---
        List<SalesRepresentative> reps = new List<SalesRepresentative>
        {
            new SalesRepresentative { RepCode = "R001", LastName = "Alami", FirstName = "Fadoua" },
            new SalesRepresentative { RepCode = "R002", LastName = "Belhadj", FirstName = "Sami" }
        };

        // --- Sample Customers ---
        List<Customer> customers = new List<Customer>
        {
            new Customer { CustomerCode = "C001", LastName = "Alami", FirstName = "Youssef", Address = "12 Main St", PostalCode = 30000, City = "Rabat" },
            new Customer { CustomerCode = "C002", LastName = "Belhadj", FirstName = "Sara", Address = "34 King St", PostalCode = 40000, City = "Casablanca" },
            new Customer { CustomerCode = "C003", LastName = "Smith", FirstName = "John", Address = "56 Elm St", PostalCode = 10000, City = "Fes" }
        };

        // --- Sample Departments (or Apartments) ---
        List<Apartment> apartments = new List<Apartment>
        {
            new Apartment { Ref = 101, Area = "75 m²", SalePrice = 150000m, Sector = "Hivernage", RepCode = "R001", CustomerCode = "C001" },
            new Apartment { Ref = 102, Area = "90 m²", SalePrice = 200000m, Sector = "Agdal", RepCode = "R002", CustomerCode = "C002" },
            new Apartment { Ref = 103, Area = "120 m²", SalePrice = 300000m, Sector = "Hivernage", RepCode = "R001", CustomerCode = "C003" },
            new Apartment { Ref = 104, Area = "60 m²", SalePrice = 100000m, Sector = "Agdal", RepCode = "R002", CustomerCode = "C003" },
            new Apartment { Ref = 105, Area = "85 m²", SalePrice = 180000m, Sector = "Hivernage", RepCode = "R001", CustomerCode = "C003" }
        };



        //--------------------------Queries------------------------------------

        //The list of customers sorted alphabetically
        Console.WriteLine("The list of customers sorted alphabetically:");
        var q = from c in customers
                orderby c.LastName, c.FirstName
                select c;
        foreach (var customer in q)
        {
            Console.WriteLine($"{customer.LastName} {customer.FirstName}");
        }
        Console.WriteLine("--------------------------------------------------");
        //The average apartment price by sector
        Console.WriteLine("The average apartment price by sector:");
        var q2 = from d in apartments
                 group d by d.Sector into g
                 select new { Sector = g.Key, AveragePrice = g.Average(x => x.SalePrice) };
        foreach (var item in q2)
        {
            Console.WriteLine($"{item.Sector}: {item.AveragePrice}");
        }
        Console.WriteLine("--------------------------------------------------");
        //The number of apartments per sector for sectors that have more than 2 apartments
        Console.WriteLine("The number of apartments per sector for sectors that have more than 10 apartments:");

        var q3 = from d in apartments
                 group d by d.Sector into g
                 where g.Count() > 2
                 select new { Sector = g.Key, ApartmentCount = g.Count() };
        foreach (var item in q3)
        {
            Console.WriteLine($"{item.Sector}: {item.ApartmentCount}");
        }
        Console.WriteLine("--------------------------------------------------");
        //The number of apartments whose area is greater than 80 m² per sector
        Console.WriteLine("The number of apartments whose area is greater than 80 m² per sector:");
        var q4 = apartments.Where(d => int.Parse(d.Area.Split(' ')[0]) > 80)
                  .GroupBy(d => d.Sector)
                  .Select(g => new { Sector = g.Key, Count = g.Count() });
        foreach (var item in q4)
        {
            Console.WriteLine($"{item.Sector}: {item.Count}");
        }
        Console.WriteLine("--------------------------------------------------");
        //The maximum apartment price by sector, but only for sectors with more than 2 apartments
        Console.WriteLine("The maximum apartment price by sector, but only for sectors with more than 10 apartments:");
        var q5=apartments.GroupBy(a=>a.Sector)
                 .Where(g => g.Count() > 2)
                 .Select(g => new { Sector = g.Key, MaxPrice = g.Max(a => a.SalePrice) });
        foreach (var item in q5)
        {
            Console.WriteLine($"{item.Sector}: {item.MaxPrice}");
        }
        Console.WriteLine("--------------------------------------------------");
        //The list of customers and the apartments they have rented
        Console.WriteLine("The list of customers and the apartments they have rented:");
        var q6 = from c in customers
                 join d in apartments on c.CustomerCode equals d.CustomerCode
                 select new { CustomerName = c.LastName + " " + c.FirstName, ApartmentRef = d.Ref };

        foreach (var item in q6)
        {
           Console.WriteLine($"{item.CustomerName}: {string.Join(", ", item.ApartmentRef)}");
        }
        Console.WriteLine("--------------------------------------------------");
        //The list of apartments located in Hivernage and managed by Fadoua ALAMI
        Console.WriteLine("The list of apartments located in Hivernage and managed by Fadoua ALAMI:");
        var q7 =apartments.Join(reps,d=>d.RepCode, r=>r.RepCode,(d,r)=>new { Apartment=d, Rep=r})
                 .Where(x => x.Apartment.Sector == "Hivernage" && x.Rep.LastName == "Alami" && x.Rep.FirstName == "Fadoua")
                 .Select(x => x.Apartment).ToList();
        foreach (var item in q7)
            {
            Console.WriteLine($"Ref: {item.Ref}, Area: {item.Area}, Price: {item.SalePrice}, Sector: {item.Sector}");
        }
        Console.WriteLine("--------------------------------------------------");
        //The number of customers from Fès per sector
        Console.WriteLine("The number of customers from Fès per sector:");
        var q8 =customers.Where(c => c.City == "Fes")
                 .Join(apartments, c => c.CustomerCode, d => d.CustomerCode, (c, d) => new { Customer = c, Apartment = d })
                 .GroupBy(x => x.Apartment.Sector)
                 .Select(g => new { Sector = g.Key, CustomerCount = g.Count()});
        foreach (var item in q8)
        {
            Console.WriteLine($"{item.Sector}: {item.CustomerCount}");
        }

    }
}