using System.Security.Cryptography.X509Certificates;
// //         Title: Stock Management System using Lists in C#
// //-----------------------Objective---------------------
//This project aims to practice working with generic collections (List<T>) and to apply exception handling in C#.
/// It focuses on developing a small console-based application for managing a stock of articles, 
/// allowing the user to perform basic operations safely and efficiently.
public class Article
{
    ////Each Article (Item) is characterized by:

    //A reference number

    //A name

    //A selling price

    //A quantity in stock

    //The stock is represented by a collection (List) of articles.

    //---------------Tasks---------------------------
    //1. Create the Article class containing:

    //Attributes / Properties

    //An initialization constructor

    //A ToString() method
    public int Id { get; set; }
    public string Name {  get; set; }   
    public decimal Price { get; set; }
    public int Qty { get; set; }
    public Article (int id,string name, decimal price, int qty)
    {
        Id = id;
        Name = name;
        Price = price;
        Qty = qty;
    }

    public override string ToString()
    {
        return $"RefNummer: {Id} "+
                $"Name Article: {Name} "+
                $"Price: {Price} " +
                $"Quantity in Stock: {Qty} ";
    }
}
public class program
{
    public static void Main(string[] args)
    {
        List<Article> articles = new List<Article>
        {
        new Article(1,"Laptop", 1200.00m, 10),
        new Article(2,"Smartphone", 800.00m, 20),
        new Article(3,"Tablet", 500.00m, 15)
         };
        try
        {
           
            DisplayMenu();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}");
        }
        //--------- Menu Options---------------------

        //Search for an article by reference number

        //Add a new article to the stock (check that the reference number is unique)

        //Delete an article by reference number

        //Modify an article by reference number

        //Search for an article by name

        //Search for articles within a price range

        //Display all articles

        //Quit the program

        void DisplayMenu()
        {
            Console.WriteLine("\n===== STOCK MANAGEMENT MENU =====");
            var exit = false;
            while (!exit)
            {
                Console.WriteLine("\n1. Search Article by Reference Number");
                Console.WriteLine("2. Add New Article");
                Console.WriteLine("3. Delete Article by Reference Number");
                Console.WriteLine("4. Modify Article by Reference Number");
                Console.WriteLine("5. Search Article by Name");
                Console.WriteLine("6. Search Articles within Price Range");
                Console.WriteLine("7. Display All Articles");
                Console.WriteLine("8. Quit");
                Console.Write("Select an option (1-8): ");
                var choice = Console.ReadLine();
                switch (choice)
                {
                    case "1":
                        SearchByReferenceNumber();
                        break;
                    case "2":
                        AddArticle();
                        break;
                    case "3":
                        DeleteArticle();
                        break;
                    case "4":
                        ModifyArticle();
                        break;
                    case "5":
                        SearchByName();
                        break;
                    case "6":
                        SearchByPriceRange();
                        break;
                    case "7":
                        DisplayAllArticles();
                        break;
                    case "8":
                        exit = true;
                        break;
                }
            }
                
        }

        void SearchByReferenceNumber()
        {
            try
            {
                Console.Write("Enter Reference Number: ");
                var id = int.Parse(Console.ReadLine());
                var item = articles.FirstOrDefault(a => a.Id == id);
                if (item != null)
                {
                    Console.WriteLine(item.ToString());
                }
                else
                {
                    Console.WriteLine("Article not found.");
                }
            }
            catch(Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
            }
           

        }
        void AddArticle()
        {

            try
            {
                Console.Write("Enter Reference Number: ");
                var id = int.Parse(Console.ReadLine());
                if (!articles.Any(a => a.Id == id))
                {
                    Console.Write("Enter Article Name: ");
                    var name = Console.ReadLine();
                    if (!string.IsNullOrWhiteSpace(name))
                    {
                        Console.Write("Enter Price: ");
                        var price = decimal.Parse(Console.ReadLine());
                        if (price > 0)
                        {
                            Console.Write("Enter Quantity: ");
                            var qty = int.Parse(Console.ReadLine());
                            if (qty >= 0)
                            {
                                articles.Add(new Article(id, name, price, qty));
                                Console.WriteLine("Article added successfully.");
                            }
                            else
                            {
                                Console.WriteLine("Quantity must be non-negative.");
                                DisplayMenu();
                            }

                        }
                        else
                        {
                            Console.WriteLine("Price must be positive.");
                            DisplayMenu();
                        }
                    }
                    else
                    {
                        Console.WriteLine("Article name cannot be empty.");
                        DisplayMenu();
                    }
                }
                else
                {
                    Console.WriteLine("Reference Number must be unique.");
                    DisplayMenu();
                }
            }
            catch(Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
            }
        }

        void DisplayAllArticles()
        {
            try
            {
                Console.WriteLine("\n--- All Articles in Stock ---");
                foreach (var item in articles)
                {
                    Console.WriteLine(item.ToString());
                }
            }
            catch(Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
            }
        }


        void DeleteArticle()
        {
            try
            {
                Console.Write("Enter Reference Number to Delete: ");
                var id = int.Parse(Console.ReadLine());
                var article = articles.FirstOrDefault(a => a.Id == id);
                if (article != null)
                {
                    articles.Remove(article);
                    Console.WriteLine("Article deleted successfully.");
                }
                else
                {
                    Console.WriteLine("Article not found.");
                }
            }
            catch(Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
            }
        }

        void ModifyArticle()
        {
            try
            {
                Console.Write("Enter Reference Number to Modify: ");
                var id = int.Parse(Console.ReadLine());
                var article = articles.FirstOrDefault(a => a.Id == id);
                if (article != null)
                {
                    Console.Write("Enter New Name (leave blank to keep current): ");
                    var name = Console.ReadLine();
                    if (!string.IsNullOrWhiteSpace(name))
                    {
                        article.Name = name;
                    }
                    Console.Write("Enter New Price (leave blank to keep current): ");
                    var priceInput = Console.ReadLine();
                    if (decimal.TryParse(priceInput, out decimal newPrice))
                    {
                        article.Price = newPrice;
                    }
                    Console.Write("Enter New Quantity (leave blank to keep current): ");
                    string qtyStr = Console.ReadLine();
                    if (int.TryParse(qtyStr, out int newQty))
                        article.Qty = newQty;
                    Console.WriteLine("Article modified successfully.");
                }
                else
                {
                    Console.WriteLine("Article not found.");
                }

            }
            catch (Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
            }

         
        }

        void SearchByName()
        {

            try
            {
                Console.Write("Enter part of the name to search: ");
                string name = Console.ReadLine().ToLower();
                var results = articles.Where(a => a.Name.ToLower().Contains(name)).ToList();

                if (results.Any())
                    results.ForEach(a => Console.WriteLine(a));
                else
                    Console.WriteLine("No articles found with that name.");
            }
            catch(Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
            }
           
        }

        void SearchByPriceRange()
        {
            try
            {
                Console.Write("Enter minimum price: ");
                decimal minPrice = decimal.Parse(Console.ReadLine());
                Console.Write("Enter maximum price: ");
                decimal maxPrice = decimal.Parse(Console.ReadLine());
                var results = articles.Where(a => a.Price >= minPrice && a.Price <= maxPrice).ToList();
                if (results.Any())
                    results.ForEach(a => Console.WriteLine(a));
                else
                    Console.WriteLine("No articles found in that price range.");
            }
            catch(Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
            }
          
        }


    }
 
}

