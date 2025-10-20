//-----------------Exercise 23--------------

//Write a program in C# Sharp to generate a cartesian product of two sets.
//Expected Output :
//The cartesian product are :
//{ letterList = X, numberList = 1 }
//{ letterList = X, numberList = 2 }
//{ letterList = X, numberList = 3 }
//{ letterList = X, numberList = 4 }

//----------------Description---------------
//In this exercise, we generate the Cartesian product of two sets using LINQ query syntax.

//The Cartesian product combines every element of the first set with every element of the second set.

//Example:

//Set A = { 1, 2 }
//Set B = {"a", "b"}
//Cartesian Product A × B = {(1,"a"), (1, "b"), (2, "a"), (2, "b")}


//Based on this rule, we can easily create the Cartesian product in C# using a LINQ query:

//var query = from a in letterListA
//            from b in numberListB
//            select new { a, b };


//Each combination is then displayed in the console.

//This demonstrates how LINQ query syntax can be used to generate all possible pairs between two collections.
//----------------Solution------------------


List<string> numberListA = new List<string>() { "X" };
List<int> numberListB = new List<int>() { 1, 2 ,3,4};
var query = from a in numberListA
            from b in numberListB
            select new { a, b };
foreach (var item in query)
{
    Console.WriteLine($"letterList = {item.a}, numberList = {item.b}");
}
