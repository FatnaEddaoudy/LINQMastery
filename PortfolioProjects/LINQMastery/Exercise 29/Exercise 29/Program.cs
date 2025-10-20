//-----------------------Exercise 29-----------------
//Write a program in C# Sharp to split a collection of strings into some groups.
//Expected Output :
//Here is the group of cities :

//ROME; LONDON; NAIROBI
//-- here is a group of cities --

//CALIFORNIA; ZURICH; NEW DELHI
//-- here is a group of cities --

//AMSTERDAM; ABU DHABI; PARIS
//-- here is a group of cities --

//NEW YORK
//-- here is a group of cities -
//-----------------------Description-----------------
//We take a list of cities and split it into smaller groups of 3 cities each. To do this, we use the index of every city and divide it by the group size (3). Cities with the same result go into the same group. Finally, we only keep the city names inside each group.

//So the idea is:

//Use the index to decide in which group each city belongs.

//Make groups of 3 cities.

//Print each group separately.

//Nothing more complicated than “cutting a list into chunks of 3 elements”.
//-----------------------Solution--------------------


List<string> cities = new List<string> {
    "ROME", "LONDON", "NAIROBI",
    "CALIFORNIA", "ZURICH", "NEW DELHI",
    "AMSTERDAM", "ABU DHABI", "PARIS",
    "NEW YORK"
};

int groupSize = 3;

var groupedCities = cities
    .Select((city, index) => new { city, index })   // keep index with each city
    .GroupBy(x => x.index / groupSize, x => x.city); // divide index to group in chunks

foreach (var group in groupedCities)
{
    Console.WriteLine(string.Join("; ", group));
    Console.WriteLine("-- here is a group of cities --");
}
