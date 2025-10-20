//Exercise19:
//Write a program in C# Sharp to remove items from list by passing filters.
//Test Data :
//Here is the list of items :
//Char: m
//Char: n
//Char: o
//Char: p
//Char: q
//Expected Output :
//Here is the list after removing item 'q' from the list :
//Char: m
//Char: n
//Char: o
//Char: p

//---------------------------------Solution-----------------------------------------------
using System;
using System.Collections.Generic;
using System.Linq;

class Program
{
    static void Main()
    {
        // Original list
        List<char> charList = new List<char> { 'm', 'n', 'o', 'p', 'q' };

        Console.WriteLine("Here is the list of items:");
        foreach (var ch in charList)
        {
            Console.WriteLine($"Char: {ch}");
        }

        // Remove 'q' by filtering
        char filterChar = 'q';
        var filteredList = charList.Where(c => c != filterChar);

        Console.WriteLine($"\nHere is the list after removing item '{filterChar}':");
        foreach (var ch in filteredList)
        {
            Console.WriteLine($"Char: {ch}");
        }
    }
}
