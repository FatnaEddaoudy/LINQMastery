using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
public class Developer
{
    public string Name;
    public string Language;
    public int Age;
}
public class Customer
{
    public String Name { get; set; }
    public String City { get; set; }
    public Order[] Orders { get; set; }
}
public class Order
{
    public Int32 IdOrder { get; set; }
    public Decimal EuroAmount { get; set; }
    public String Description { get; set; }
}

public class Category
{
    public Int32 IdCategory { get; set; }
    public String Name { get; set; }
}
public class Product
{
    public String IdProduct { get; set; }
    public Int32 IdCategory { get; set; }
    public String Description { get; set; }
}

class App
{
    static void Main()
    {
        //Part I LINQ Foundations
        Console.WriteLine("Part I LINQ Foundations");
        ArrayList developers = new ArrayList();
        developers.Add(new Developer { Name = "Alice", Language = "C#", Age = 30 });
        developers.Add(new Developer { Name = "Bob", Language = "Java", Age = 25 });
        developers.Add(new Developer { Name = "Charlie", Language = "C#", Age = 35 });

        Console.WriteLine("");
        //select developer using C#
        Console.WriteLine("Developers using C#:");
        var developersUsingCSharp =
            from Developer d in developers
            where d.Language == "C#"
            select d.Name;
        foreach (var item in developersUsingCSharp)
        {
            Console.WriteLine(item);
        }

        Customer[] customers = new Customer[]
        {
            new Customer{Name="Alice",City="New York",
                Orders=new Order[]
            {
                new Order{IdOrder=1,EuroAmount=100,Description="Laptop"},
                new Order{IdOrder=2,EuroAmount=50,Description="Mouse"}
            }},
            new Customer{Name="Bob",City="Los Angeles",
                Orders=new Order[]
            {
                new Order{IdOrder=3,EuroAmount=200,Description="Tablet"}
            }},
            new Customer{Name="Charlie",City="New York",
                Orders=new Order[]
            {
                new Order{IdOrder=4,EuroAmount=150,Description="Smartphone"},
                new Order{IdOrder=5,EuroAmount=80,Description="Headphones"}
            }}
        };
        Console.WriteLine();
        //Select all orders with customer name
        Console.WriteLine("All orders with customer name:");
        var ordersQuery = from c in customers
                          from o in c.Orders
                          select new { c.Name, o.IdOrder, o.EuroAmount };
        foreach (var item in ordersQuery)
        {
            Console.WriteLine($"{item.Name} placed order {item.IdOrder} for {item.EuroAmount} euros");
        }
        Console.WriteLine();
        //Select Order with EuroAmount greater than 200 Euros
        Console.WriteLine("Orders with EuroAmount greater than 200 Euros:");
        var selectorder = from c in customers
                          from o in c.Orders
                          where o.EuroAmount > 200
                          select new { c.Name, o.IdOrder, o.EuroAmount };

        foreach (var item in selectorder)
        {
            Console.WriteLine($"{item.Name} placed order {item.IdOrder} for {item.EuroAmount} euros");
        }


        Developer[] developers1 = new Developer[]
        {
            new Developer{Name="Alice",Language="C#",Age=30},
            new Developer{Name="Bob",Language="Java",Age=25},
            new Developer{Name="Charlie",Language="C#",Age=35},
            new Developer{Name="David",Language="Python",Age=28},
            new Developer{Name="Eve",Language="Java",Age=32}
        };

        Console.WriteLine();
        //Group developers by Language
        Console.WriteLine("Developers grouped by Language:");
        var developersGroupedByLanguage =
           from d in developers1
           group d by d.Language;

        foreach(var item in developersGroupedByLanguage)
        {
            Console.WriteLine($"Language: {item.Key}");
            foreach(var dev in item)
            {
                Console.WriteLine($"  Developer: {dev.Name}, Age: {dev.Age}");
            }
        }
        Console.WriteLine();
        Console.WriteLine("A C# query expression to group developers by programming language and age ");
        var groupedByLanguageAndAge =
           from d in developers1
           group d by new { d.Language,Agecluster=( d.Age/10)*10 };
        foreach (var item in groupedByLanguageAndAge)
        {
            Console.WriteLine("Language:"+ item.Key);
            foreach (var dev in item)
            {
                Console.WriteLine($"  Developer: {dev.Name}");
            }
        }


        Console.WriteLine();
        Console.WriteLine("A C# query expression using the into clause");
        var developersGroupByLanguage =
            from d in developers1
            group d by d.Language into developersGrouped
            select new
            {
                language = developersGrouped.Key,
                DevelopersCount = developersGrouped.Count(),
            };
        foreach (var item in developersGroupByLanguage)
        {
            Console.WriteLine($"Language: {item.language}, Count: {item.DevelopersCount}");
        }

        Console.WriteLine();
        Console.WriteLine("A C# query expression with an orderby clause ");
        var ordersSortedByEuroAmount =
            from c in customers
            from o in c.Orders
            orderby o.EuroAmount
            select new { c.Name, o.IdOrder, o.EuroAmount };
        foreach (var item in ordersSortedByEuroAmount)
        {
            Console.WriteLine($"{item.Name} placed order {item.IdOrder} for {item.EuroAmount} euros");
        }

        Console.WriteLine();
        Console.WriteLine("A C# query expression with an orderby clause with multiple ordering conditions");
        var ordersSortedByCustomerCityAndEuroAmount =
            from c in customers
            from o in c.Orders
            orderby c.Name, o.EuroAmount descending
            select new { c.Name, o.IdOrder, o.EuroAmount };
        foreach (var item in ordersSortedByCustomerCityAndEuroAmount)
        {
            Console.WriteLine($"{item.Name} placed order {item.IdOrder} for {item.EuroAmount} euros");
        }

        Console.WriteLine();
        Console.WriteLine("A C# query expression with an inner join");
        Category[] categories = new Category[] {
            new Category { IdCategory = 1, Name = "Pasta"},
            new Category { IdCategory = 2, Name = "Beverages"},
            new Category { IdCategory = 3, Name = "Other food"},
        };
        Product[] products = new Product[] {
            new Product { IdProduct = "PASTA01", IdCategory = 1, Description = "Tortellini" },
            new Product { IdProduct = "PASTA02", IdCategory = 1, Description = "Spaghetti" },
            new Product { IdProduct = "PASTA03", IdCategory = 1, Description = "Fusilli" },
            new Product { IdProduct = "BEV01", IdCategory = 2, Description = "Water" },
            new Product { IdProduct = "BEV02", IdCategory = 2, Description = "Orange Juice" },
        };

        var productcategory = from c in categories
                              join p in products on c.IdCategory equals p.IdCategory
                              select new
                              {
                                  c.IdCategory,
                                  categroryName = c.Name,
                                  Product = p.Description
                              };

        foreach (var item in productcategory)
        {
        Console.WriteLine(item);
        }

        Console.WriteLine();
        Console.WriteLine("A C# query expression with a group join");
        var categoriesAndProducts =
    from c in categories
    join p in products on c.IdCategory equals p.IdCategory
        into productsByCategory
    select new
    {
        c.IdCategory,
        CategoryName = c.Name,
        Products = productsByCategory
    };
        foreach (var category in categoriesAndProducts)
        {
            Console.WriteLine("{0} - {1}", category.IdCategory, category.CategoryName);
            foreach (var product in category.Products)
            {
                Console.WriteLine("\t{0}", product.Description);
            }
        }

        //A C# query expression with a left outer join
        var categoriesAndProductsList =
            from c in categories
            join p in products on c.IdCategory equals p.IdCategory
                into productsByCategory
            from pc in productsByCategory.DefaultIfEmpty(
              new Product
              {
                  IdProduct = String.Empty,
                  Description = String.Empty,
                  IdCategory = 0
              })
            select new
            {
                c.IdCategory,
                CategoryName = c.Name,
                Product = pc.Description
            };
        Console.WriteLine("list Categories:");

        foreach (var item in categoriesAndProductsList)
        {
            Console.WriteLine(value: item);
        
        }

        //Listing C# sample of usage of the let clause
        Console.WriteLine();
        Console.WriteLine("C# sample of usage of the let clause");
        var categoriesByProductsNumberQuery =
    from c in categories
    join p in products on c.IdCategory equals p.IdCategory
       into productsByCategory
    let ProductsCount = productsByCategory.Count()
    orderby ProductsCount
    select new { c.IdCategory, ProductsCount };
        foreach (var item in categoriesByProductsNumberQuery)
        {
            Console.WriteLine(item);
        }

        //C# query expression that references an external method that throws a fictitious exception
        static Boolean DoSomething(Developer dev)
        {
            if(dev.Age>40)
            {
                throw new ArgumentOutOfRangeException("dev");
            }
            return (dev.Language=="C#");
        }
        var query =
        from d in developers1
        select new { d.Name, SomethingResult= DoSomething(d) };
        foreach (var item in query)
        {
            Console.WriteLine(item);
        }
        //C# query expression used with exception handling
        Console.WriteLine();
        Console.WriteLine("C# query expression used with exception handling");
        Developer[] developerslist=new Developer[]
        {
            new Developer{Name="Alice",Language="C#",Age=30},
            new Developer{Name="Bob",Language="Java",Age=25},
            new Developer{Name="Charlie",Language="C#",Age=35},
            new Developer{Name="David",Language="Python",Age=28},
            new Developer{Name="Eve",Language="Java",Age=32},
            new Developer{Name="Frank",Language="C#",Age=45}
        };
        try
        {
            query =
            from d in developerslist
            let SomethingResult = DoSomething(d)
            select new { d.Name, SomethingResult };
            foreach (var item in query)
            {
                Console.WriteLine(item);
            }
        }
        catch(ArgumentOutOfRangeException ex)
        {
            Console.WriteLine(ex.Message);
        }

       

    }
    
}