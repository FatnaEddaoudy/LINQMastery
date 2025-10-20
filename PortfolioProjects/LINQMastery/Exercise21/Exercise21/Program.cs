//----------------Exercise21---------------------

//Write a program in C# Sharp to remove a range of items from a list by passing the start index and number of elements to remove.
//Test Data :
//Here is the list of items :
//Char: m
//Char: n
//Char: o
//Char: p
//Char: q
//Expected Output:
//Here is the list after removing the three items starting from the item index 1 from the list :
//Char: m
//Char: q

//Description: 
using System.Collections.Generic;

//Description

//In this exercise, we use a LINQ method to remove a range of items from a list.

//We specify a starting index (startIndex) and the number of elements to remove (count).

//The LINQ expression:

//var query = charList.Where((value, index) => index < startIndex || index >= (startIndex + count))
//                    .ToList()
//Uses the index-aware overload of Where to filter out all items in the specified range.

//This demonstrates how to remove a consecutive range of items using LINQ instead of directly modifying the original list.


//---------Solution-----------------

class Program
{
    static void Main(string[] args)
    {
        // Define a list of characters
        List<char> charList = new List<char> { 'm', 'n', 'o', 'p', 'q' };
        // Display the original list
        Console.WriteLine("Here is the list of items:");
        foreach (char c in charList)
        {
            Console.WriteLine($"Char: {c}");
        }

        // Define the start index and number of elements to remove
        int startIndex = 1;
        int count = 3;
        // Remove the specified range of elements from the list

        var query = charList.Where((value, index) => index < startIndex || index >= (startIndex + count))
                      .ToList();
        // Display the modified list
        Console.WriteLine("\nHere is the list after removing the three items starting from the item index 1 from the list:");
        foreach (char c in query)
        {
            Console.WriteLine($"Char: {c}");
        }
    }
}