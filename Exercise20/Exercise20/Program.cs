//Exercise20
using System.Collections.Generic;
using System.Diagnostics.Metrics;

//Write a program in C# Sharp to remove items from list by passing the item index.
//Test Data :
//Here is the list of items :
//Char: m
//Char: n
//Char: o
//Char: p
//Char: q
//Expected Output:
//Here is the list after removing item index 3 from the list :
//Char: m
//Char: n
//Char: o
//Char: q




//Description

//In this exercise, we remove an item from a list by its specific index.

//Instead of removing an item by value, we use the position (index) of the item in the list.

//We create a new filtered sequence using LINQ that excludes the item at the specified index.

//The original list is not modified; the new list contains all items except the one at the given index.

//This exercise demonstrates how to use the index in LINQ’s Where method to filter items based on their position in the list.


//-------------Solution----------------


class Program
{
    static void Main()
    {
        List<char> chars = new List<char>() { 'm', 'n', 'o', 'p', 'q' };
        Console.WriteLine("Here is the list of items :");
        foreach (var c in chars)
        {
            Console.WriteLine($"Char: {c}");
        }
        Console.WriteLine("Enter the index of the item to remove:");
        int indexToRemove =int.Parse(Console.ReadLine());
        if (indexToRemove >= 0 && indexToRemove < chars.Count)
        {
           var query =chars.Where((c, index) => index != indexToRemove).ToList();
        }
        else
        {
            Console.WriteLine("Index out of range.");
        }
        Console.WriteLine("Here is the list after removing item index 3 from the list :");
        foreach (var c in chars)
        {
            Console.WriteLine($"Char: {c}");
        }
    }

}