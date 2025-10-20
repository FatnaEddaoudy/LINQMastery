//--------------------Exercise 28------------------
//Write a program in C# Sharp to display the list of items in the array according to the length of the string then by name in ascending order.
//Expected Output :
//Here is the arranged list:
//ROME
//PARIS
//LONDON
//ZURICH
//NAIROBI
//ABU DHABI
//AMSTERDAM
//NEW DELHI
//CALIFORNIA
//--------------------Description----------
//In this exercise we simply use orderby with two keys: first the length of the string,
// and then the string itself, to sort the list of cities.
// Nothing complex, just a basic demonstration of multi-level sorting with LINQ.

//--------------------Solution-------------

using System;
class Program
{
    static void Main()
    {
        string[] cities = { "ROME", "LONDON", "NAIROBI", "CALIFORNIA", "ZURICH", "NEW DELHI", "AMSTERDAM", "ABU DHABI", "PARIS" };
        var query=from city in cities
                  orderby city.Length, city
                  select city;
        Console.WriteLine("Here is the arranged list:");
        foreach (var city in query)
        {
            Console.WriteLine(city);
        }
    }
}