// See https://aka.ms/new-console-template for more information
using LINQ_to_Objects;
using System.Collections.Generic;
using System.Diagnostics.Metrics;
using System.Linq;
using System.Text.RegularExpressions;


// -------------------------------------------------------
// Initialize a collection of customers with their orders:
// -------------------------------------------------------
var customers = new Customer[] {
  new Customer {Name = "Paolo", City = "Brescia",Country = Countries.Italy, Orders = new Order[] {
 new Order { IdOrder = 1, Quantity = 3, IdProduct = 1 ,Shipped = false, Month = "January"},
 new Order { IdOrder = 2, Quantity = 5, IdProduct = 2 ,Shipped = true, Month = "May"}}},
 new Customer {Name = "Marco", City = "Torino",Country = Countries.Italy, Orders = new Order[] {
 new Order { IdOrder = 3, Quantity = 10, IdProduct = 1 , Shipped = false, Month = "July"},
 new Order { IdOrder = 4, Quantity = 20, IdProduct = 3 , Shipped = true, Month = "December"}}},
 new Customer {Name = "James", City = "Dallas", Country = Countries.USA, Orders = new Order[] {
 new Order { IdOrder = 5, Quantity = 20, IdProduct = 3 ,Shipped = true, Month = "December"}}},
new Customer {Name = "Frank", City = "Seattle",Country = Countries.USA, Orders = new Order[] {
new Order { IdOrder = 6, Quantity = 20, IdProduct = 5 ,Shipped = false, Month = "July"}}}};

var products = new Product[] {
 new Product {IdProduct = 1, Price = 10 },
 new Product {IdProduct = 2, Price = 20 },
 new Product {IdProduct = 3, Price = 30 },
 new Product {IdProduct = 4, Price = 40 },
 new Product {IdProduct = 5, Price = 50 },
 new Product {IdProduct = 6, Price = 60 }};


// Query Operators
// ===============
Console.WriteLine("***** The Where Operator*****\n");
Console.WriteLine("o list the names and cities of customers from Italy");

var expr =
 from c in customers
 where c.Country == Countries.Italy
 select new { c.Name, c.City };
foreach (var item in expr)
{
    Console.WriteLine(item);
}


//A projection with an index argument in the selector predicate

var expr1 =
    customers
    .Select((c, index) => new { index, c.Name, c.Country });
foreach (var item in expr1)
{
    Console.WriteLine(item);
}

//The GroupBy operator used to group customers by Country

var exp3 = customers.GroupBy(c => c.Country);

 foreach(IGrouping<Countries, Customer> customerGroup in exp3)
{
    Console.WriteLine("Country: {0}", customerGroup.Key);
    foreach (var item in customerGroup)
    {
        Console.WriteLine("\t{0}", item);
    }
}

//A query expression with a group … by … syntax
var expr4 =
    from c in customers
    group c by c.Country;
foreach (IGrouping<Countries, Customer> customerGroup in expr4)
{
    Console.WriteLine("Country: {0}", customerGroup.Key);
    foreach (var item in customerGroup)
    {
        Console.WriteLine("\t{0}", item);
    }
}

//The GroupBy operator used to group customer names by Country

var expr6 =
    customers
    .GroupBy(c => c.Country, c => c.Name);
foreach (IGrouping<Countries, String> customerGroup in expr6)
{
    Console.WriteLine("Country: {0}", customerGroup.Key);
    foreach (var item in customerGroup)
    {
        Console.WriteLine("\t{0}", item);
    }
}


//The GroupBy operator used to group customer names by Country
var expr7 = customers
  .GroupBy(c => c.Country,
    (k, c) => new { Key = k, Count = c.Count() });
foreach (var group in expr7)
{
    Console.WriteLine("Key: {0} - Count: {1}", group.Key, group.Count);
}

//The GroupJoin operator used to map products with orders, if present
Console.WriteLine("");
var expr8 =
    products
    .GroupJoin(
        customers.SelectMany(c => c.Orders),
        p => p.IdProduct,
        o => o.IdProduct,
        (p, orders) => new { p.IdProduct, Orders = orders });
foreach (var item in expr8)
{
    Console.WriteLine("Product: {0}", item.IdProduct);
    foreach (var order in item.Orders)
    {
        Console.WriteLine("\t{0}", order);
    }
};

//The Distinct operator applied to the list of products used in orders

var expr9 =
    customers
    .SelectMany(c => c.Orders)
    .Join(products,
          o => o.IdProduct,
          p => p.IdProduct,
          (o, p) => p)
    .Distinct();


//The Union operator applied to sets of Integer numbers

Console.WriteLine("\n***** The Union Operator *****\n");

Int32[] setOne = { 1, 5, 6, 9 };
Int32[] setTwo = { 4, 5, 7, 11 };
var union = setOne.Union(setTwo);
foreach (var i in union)
{
    Console.Write(i + ", ");
}

//The Union operator applied to a couple of sets of products


Product[] productSetOne = {
    new Product {IdProduct = 46, Price = 1000 },
    new Product {IdProduct = 27, Price = 2000 },
    new Product {IdProduct = 14, Price = 500 } };
Product[] productSetTwo = {
    new Product {IdProduct = 11, Price = 350 },
    new Product {IdProduct = 46, Price = 1000 } };
var productsUnion = productSetOne.Union(productSetTwo);
foreach (var item in productsUnion)
{
    Console.WriteLine(item);
}

//Set operators applied to query expressions

var expr10 = (
    from c in customers
    from o in c.Orders
    join p in products on o.IdProduct equals p.IdProduct
    where c.Country == Countries.Italy
    select p)
    .Intersect(
     from c in customers
     from o in c.Orders
     join p in products on o.IdProduct equals p.IdProduct
     where c.Country == Countries.USA
     select p);


//Count 
Console.WriteLine("\n***** The Count Operator *****\n");
var expr11 =
    from c in customers
    select new { c.Name, c.Country, OrdersCount = c.Orders.Count() };



//The Sum operator applied to customer orders

var customersOrders =
    from c in customers
    from o in c.Orders
    join p in products
           on o.IdProduct equals p.IdProduct
    select new { c.Name, OrderAmount = o.Quantity * p.Price };
foreach (var o in customersOrders)
{
    Console.WriteLine(o);
}
Console.WriteLine();


var expr12 =
    from c in customers
    join o in customersOrders
           on c.Name equals o.Name
           into customersWithOrders
    select new
    {
        c.Name,
        TotalAmount = customersWithOrders.Sum(o => o.OrderAmount)
    };
foreach (var item in expr12)
{
    Console.WriteLine(item);
}

//The Sum operator applied to customer orders, with a nested query

var expr13 =
    from c in customers
    join o in (
           from c in customers
           from o in c.Orders
           join p in products
                  on o.IdProduct equals p.IdProduct
           select new { c.Name, OrderAmount = o.Quantity * p.Price }
           ) on c.Name equals o.Name
           into customersWithOrders
    select new
    {
        c.Name,
        TotalAmount = customersWithOrders.Sum(o => o.OrderAmount)
    };

foreach (var item in expr13)
{
    Console.WriteLine(item);
}


// Typical lambda expression using Func delegate
Func<int, int> IncDelegate = delegate (int x) { return x + 1; };
Func<int, int> IncLambda = x => x + 1;
Console.WriteLine(IncDelegate(2));
Console.WriteLine(IncLambda(2));