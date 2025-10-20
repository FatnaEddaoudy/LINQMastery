//------------Exercise 17------------

//Write a program in C# Sharp to remove items from list using remove function by passing the object.
//Test Data :
//Here is the list of items :
//Char: m
//Char: n
//Char: o
//Char: p
//Char: q
//Expected Output:
//Here is the list after removing the item 'o' from the list :
//Char: m
//Char: n
//Char: p
//Char: q

//------------Solution------------
//Description

//In this exercise, we work with a list of characters in C#.

//We use the Add method to insert characters into the list.

//We use RemoveAll to remove all occurrences of a specified character from the list.

//The program allows the user to:

//Enter multiple characters to build the list (stopping with a dot.).

//Display the full list of characters.

//Remove a specific character from the list (all occurrences).

//Display the updated list after removal.

//This exercise demonstrates basic list operations and the use of lambda expressions with RemoveAll.


using System;
using System.Collections.Generic;

  List<char> chars=new List<char>() ;
   Console.WriteLine("Enter chars to add to list, type '.' to stop:");
   char c;
   while ((c = Console.ReadKey(true).KeyChar) != '.')
   {
    if (c != '\n' && c != '\r')  // ignore Enter
        chars.Add(c);
    Console.WriteLine(c);
    Console.WriteLine("Enter chars to add to list, type '.' to stop:");
}
;
    // Display list
    Console.WriteLine("Here is the list of items :");
    foreach (char ch in chars)
     { 
       Console.WriteLine(value: "Char: " + ch); 
     };

Console.WriteLine("Enter char to remove from list: ");
char toRemove = Console.ReadKey().KeyChar;
Console.WriteLine();
chars.RemoveAll(ch=>ch==toRemove);
    Console.WriteLine("Here is the list after removing the item 'o' from the list :");
    // Display updated list
    foreach (char ch in chars)
        Console.WriteLine("Char: " + ch);