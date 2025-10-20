//----------------------Exercise 26----------------------

//Write a program in C# Sharp to generate a Left Join between two data sets.
//Expected Output :

//Here is the list after joining  :                                                                             

//Item ID         Item Name       Purchase Quantity                                                             
//-------------------------------------------------------                                                       
//1               Biscuit                 458                                                                   
//2               Chocolate               650                                                                   
//3               Butter                  800                                                                   
//3               Butter                  900                                                                   
//3               Butter                  900                                                                   
//4               Brade                   700                                                                   
//4               Brade                   650                                                                   
//5               Honey                   0 

//----------------------Description-----------

//In this exercise, we are tasked with generating a Left Join between two data sets using C#.
//A Left Join returns all records from the left data set (the first data set),
//and the matched records from the right data set (the second data set).
//If there is no match, the result is NULL on the side of the right data set.
//----------------------Solution---------------

class product
{
    public int ItemID { get; set; }
    public string ItemName { get; set; }
}
class purchase
{
    public int ItemID { get; set; }
    public int PurchaseQuantity { get; set; }
}
class program
{
    static void Main(string[] args)
    {
        List<product> products = new List<product>()
        {
            new product(){ItemID=1,ItemName="Biscuit"},
            new product(){ItemID=2,ItemName="Chocolate"},
            new product(){ItemID=3,ItemName="Butter"},
            new product(){ItemID=4,ItemName="Brade"},
            new product(){ItemID=5,ItemName="Honey"}
        };
        List<purchase> purchases = new List<purchase>()
        {
            new purchase(){ItemID=1,PurchaseQuantity=458},
            new purchase(){ItemID=2,PurchaseQuantity=650},
            new purchase(){ItemID=3,PurchaseQuantity=800},
            new purchase(){ItemID=3,PurchaseQuantity=900},
            new purchase(){ItemID=3,PurchaseQuantity=900},
            new purchase(){ItemID=4,PurchaseQuantity=700},
            new purchase(){ItemID=4,PurchaseQuantity=650}
        };
        var leftJoin = from p in products
                       join pur in purchases
                       on p.ItemID equals pur.ItemID into ps
                       //create a fake purchase object with 0 quantity if there is no match
                       from pur in ps.DefaultIfEmpty(new purchase() { ItemID = p.ItemID, PurchaseQuantity = 0 })
                       select new
                       {
                           p.ItemID,
                           p.ItemName,
                           pur.PurchaseQuantity
                       };
        Console.WriteLine("Here is the list after joining  :");
        Console.WriteLine();
        Console.WriteLine("Item ID\t\tItem Name\tPurchase Quantity");
        Console.WriteLine("-------------------------------------------------------");
        foreach (var item in leftJoin)
        {
            Console.WriteLine($"{item.ItemID}\t\t{item.ItemName}\t\t{item.PurchaseQuantity}");
        }
    }
}   