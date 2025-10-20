//-----------------------Exercise 27-----------------------
//Write a program in C# Sharp to generate a Right Outer Join between two data sets.
//Expected Output :

//Here is the list after joining  :                                                                             

//Item ID         Item Name       Purchase Quantity                                                             
//-------------------------------------------------------                                                       
//3               Butter                  800                                                                   
//5               Honey                   650                                                                   
//3               Butter                  900                                                                   
//4               Brade                   700                                                                   
//3               Butter                  900                                                                   
//4               Brade                   650                                                                   
//1               Biscuit                 458  
//-----------------------Description-----------------------

//A right outer join returns all records from the right table (table2), and the matched records from the left table (table1).
//INNER JOIN → Only matches on both sides.

//LEFT OUTER JOIN → All elements from the left table, even if no match (with defaults for the right).

//RIGHT OUTER JOIN → All elements from the right table, even if no match (with defaults for the left).

//With Left Join → all products appear.

//With Right Join → all purchases appear, even if they don’t match any product.

//-----------------------Solution--------------------------

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
        List<product> productList = new List<product>()
        {
            new product(){ItemID=1,ItemName="Biscuit"},
            new product(){ItemID=2,ItemName="Cake"},
            new product(){ItemID=3,ItemName="Butter"},
            new product(){ItemID=4,ItemName="Brade"},
            new product(){ItemID=5,ItemName="Honey"}
        };
        List<purchase> purchaseList = new List<purchase>()
        {
            new purchase(){ItemID=3,PurchaseQuantity=800},
            new purchase(){ItemID=5,PurchaseQuantity=650},
            new purchase(){ItemID=3,PurchaseQuantity=900},
            new purchase(){ItemID=4,PurchaseQuantity=700},
            new purchase(){ItemID=3,PurchaseQuantity=900},
            new purchase(){ItemID=4,PurchaseQuantity=650},
            new purchase(){ItemID=1,PurchaseQuantity=458}
        };
        var rightJoin = from pur in purchaseList
                        join item in productList
                        on pur.ItemID equals item.ItemID into ps
                        from item in ps.DefaultIfEmpty(new product() { ItemID = pur.ItemID, ItemName = "Unknown" })
                        select new
                        {
                            item.ItemID,
                            item.ItemName,
                            pur.PurchaseQuantity
                        };
        Console.WriteLine("Here is the list after joining  :");
        Console.WriteLine();
        Console.WriteLine("Item ID\t\tItem Name\tPurchase Quantity");
        Console.WriteLine("-------------------------------------------------------");
        foreach (var item in rightJoin)
        {
            Console.WriteLine($"{item.ItemID}\t\t{item.ItemName}\t\t{item.PurchaseQuantity}");
        }
    }
}