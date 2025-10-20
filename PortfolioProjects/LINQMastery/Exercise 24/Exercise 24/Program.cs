//-------------------Exercise 24----------------

//Write a program in C# Sharp to generate a cartesian product of three sets.
//Expected Output :
//The cartesian product are :
//{ letter = X, number = 1, colour = Green }
//{ letter = X, number = 1, colour = Orange }
//{ letter = X, number = 2, colour = Green }
//{ letter = X, number = 2, colour = Orange }
//{ letter = X, number = 3, colour = Green }
//{ letter = X, number = 3, colour = Orange }
//{ letter = Y, number = 1, colour = Green }
//{ letter = Y, number = 1, colour = Orange }


//-------------------Description----------------

//This exercise is similar to Exercise 23, but instead of combining two sets, we now generate the Cartesian product of three sets.

//A Cartesian product with three sets means that each element from the first set is combined with all elements of the second set and all elements of the third set.

//Example:

//Set A = { X, Y }  
//Set B = {1, 2, 3}  
//Set C = { Green, Orange }  

//A × B × C =  
//(X, 1, Green), (X, 1, Orange), (X, 2, Green), (X, 2, Orange), (X, 3, Green), (X, 3, Orange),
//(Y, 1, Green), (Y, 1, Orange), (Y, 2, Green), (Y, 2, Orange), (Y, 3, Green), (Y, 3, Orange)


//Using LINQ query syntax, we achieve this with three nested from clauses:

//var cartesianProduct = from letter in letters
//                       from number in numbers
//                       from colour in colours
//                       select new { letter, number, colour };


//The result is that every possible combination of letter, number, and colour is generated and displayed.

//-------------------Solution----------------

List<string> letters = new List<string> { "X", "Y" };
List<int> numbers = new List<int> { 1, 2, 3 };
List<string> colours = new List<string> { "Green", "Orange" };

var cartesianProduct = from letter in letters
                       from number in numbers
                       from colour in colours
                       select new { letter, number, colour };

foreach (var item in cartesianProduct)
{
    Console.WriteLine($"{{ letter = {item.letter}, number = {item.number}, colour = {item.colour} }}");
}