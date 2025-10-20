
//--------------Exercise 22: ------------------
//Write a program in C# Sharp to find the strings for a specific minimum length.
//Test Data :
//Input number of strings to store in the array :4
//Input 4 strings for the array:
//Element[0] : this
//Element[1] : is
//Element[2] : a
//Element[3] : string
//Input the minimum length of the item you want to find : 5
//Expected Output:
//The items of minimum 5 characters are :
//Item: string

//----------Description:-------------------------
//In this exercise, we work with a list of strings and use a LINQ method to find items based on their length.

//The user enters a number of strings to store in the list.

//Then the user specifies a minimum length (minLength).

//Using the LINQ query:

//var query = strings.Where(s => s.Length >= minLength);


//We filter the list to include only strings whose length is greater than or equal to minLength.

//The filtered items are then displayed.

//This exercise demonstrates how to use LINQ to filter a collection based on a condition, in this case the length of the strings.
//-------------------Solution: --------------------


List<string> strings = new List<string>();
Console.WriteLine("Input number of strings to store in the array: ");
int n = int.Parse(Console.ReadLine()!);
for (int i = 0; i < n; i++)
{
    Console.WriteLine($"Element[{i}] : ");
    strings.Add(Console.ReadLine()!);
}

Console.WriteLine($"the {n} strings: ");
for(int i = 0; i < n; i++)
{
    Console.WriteLine($"Element[{i}] : {strings[i]} ");
}
Console.WriteLine("\nInput the minimum length of the item you want to find: ");
int minLength = int.Parse(Console.ReadLine()!);
Console.WriteLine($"The items of minimum {minLength} characters are: ");
var query=strings.Where(s=>s.Length>=minLength);
foreach(var str in query)
{
    Console.WriteLine($"Item: {str}");
}