//-----------------Exercise 25----------------
//Write a program in C# Sharp to generate an Inner Join between two data sets.
//Expected Output :

//Item ID         Item Name       Purchase Quantity                                                             
//-------------------------------------------------------                                                       
//1               Biscuit                 458                                                                   
//2               Chocolate               650                                                                   
//3               Butter                  800                                                                   
//3               Butter                  900                                                                   
//3               Butter                  900                                                                   
//4               Brade                   700                                                                   
//4               Brade                   650

//-----------------Description----------------
//In this exercise, we demonstrate how to use INNER JOIN in LINQ to combine data from two different lists (tables):

//Item class represents a product with ItemId and ItemName.

//Purchase class represents purchase records with ItemId and PurchaseQuantity.

//There is a one-to-many relationship between these two lists:

//One Item can appear in many Purchase records (because many purchases can be made of the same product).

//Using LINQ join, we match each purchase with the corresponding item, based on the common key ItemId:

//var innerJoin = from item in items
//                join purchase in purchases
//                on item.ItemId equals purchase.ItemId
//                select new
//                {
//                    item.ItemId,
//                    item.ItemName,
//                    purchase.PurchaseQuantity
//                };


//This produces a result where every purchase is displayed together with its corresponding Item Name.

//Since it’s an inner join, only purchases that have a matching item in the items list are included.


//-----------------Solution   ----------------

class Item
{
    public int ItemId { get; set; }
    public string ItemName { get; set; }
}
class Purchase
{
    public int ItemId { get; set; }
    public int PurchaseQuantity { get; set; }
}


class program
{
    static void Main(string[] args)
    {
        List<Item> items = new List<Item>()
        {
            new Item(){ItemId=1,ItemName="Biscuit"},
            new Item(){ItemId=2,ItemName="Chocolate"},
            new Item(){ItemId=3,ItemName="Butter"},
            new Item(){ItemId=4,ItemName="Brade"},
        };
        List<Purchase> purchases = new List<Purchase>()
        {
            new Purchase(){ItemId=1,PurchaseQuantity=458},
            new Purchase(){ItemId=2,PurchaseQuantity=650},
            new Purchase(){ItemId=3,PurchaseQuantity=800},
            new Purchase(){ItemId=3,PurchaseQuantity=900},
            new Purchase(){ItemId=3,PurchaseQuantity=900},
            new Purchase(){ItemId=4,PurchaseQuantity=700},
            new Purchase(){ItemId=4,PurchaseQuantity=650},
        };
        var innerJoin = from item in items
                        join purchase in purchases
                        on item.ItemId equals purchase.ItemId
                        select new
                        {
                            item.ItemId,
                            item.ItemName,
                            purchase.PurchaseQuantity
                        };
        Console.WriteLine("Item ID\t\tItem Name\tPurchase Quantity");
        Console.WriteLine("-------------------------------------------------------");
        foreach (var i in innerJoin)
        {
            Console.WriteLine($"{i.ItemId}\t\t{i.ItemName}\t\t{i.PurchaseQuantity}");
        }
    }
}