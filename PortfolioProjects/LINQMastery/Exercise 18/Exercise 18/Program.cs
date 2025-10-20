//------------Exercice18-----------

//Write a program in C# Sharp to remove items from list by creating an object internally by filtering.
//Test Data :
//Here is the list of items :
//Char: m
//Char: n
//Char: o
//Char: p
//Char: q
//Expected Output :
//Here is the list after removing the item 'p' from the list :
//Char: m
//Char: n
//Char: o
//Char: q


//Description

//In this exercise, we work with a list of characters in C#.

//The program displays the original list of characters.

//The user is prompted to enter a character to remove.

//Instead of modifying the original list directly, we use a LINQ query (Where) to create a new filtered sequence that excludes the specified character.

//The filtered sequence is displayed, leaving the original list unchanged.

//This exercise demonstrates how to filter a list using LINQ and create a new collection based on a condition, without altering the original list.

//------------Code Start-----------



using System;
using System.Linq;
using System.Collections.Generic;
class Program
{
    static void Main()
    {
        // Create a list of characters
        var charList = new List<char> { 'm', 'n', 'o', 'p', 'q' };
        Console.WriteLine("Here is the list of items:");
        foreach (var ch in charList)
        {
            Console.WriteLine($"Char: {ch}");
        }
        // Remove the item 'p' from the list using a lambda expression
        Console.WriteLine("\nEnter the character to remove from the list:");
        char carToRemove = char.Parse(Console.ReadLine());
        var query= charList.Where(c => c != carToRemove);

        Console.WriteLine($"\nHere is the list after removing the item {carToRemove} from the list:");
        foreach (var ch in query)
        {
            Console.WriteLine($"Char: {ch}");
        }
    }
}