//Exercice: Write a program in C# Sharp to count file extensions and group it using LINQ.
//Test Data :
//The files are : aaa.frx, bbb.TXT, xyz.dbf,abc.pdf
//aaaa.PDF,xyz.frt, abc.xml, ccc.txt, zzz.txt
//Expected Output :
//Here is the group of extension of the files :
//1 File(s) with.frx Extension
//3 File(s) with .txt Extension
//1 File(s) with .dbf Extension
//2 File(s) with .pdf Extension
//1 File(s) with .frt Extension
//1 File(s) with .xml Extension

//--------------------Description--------------------
//The exercise asks us to filter and group file extensions from a list of file names.

//The important function to use here is Path.GetExtension(), which makes it easy to extract the extension (like .txt, .pdf, etc.) from each file name.

//To calculate the frequency of each extension, we use group file by extension in LINQ. This way, all files with the same extension are grouped together, and we can simply count them.

//Use GetExtension → to extract the extension.

//Use group by → to count how many files share the same extension.

//-------------solution-----------------------------

List<string> FileName = new List<string> { "aaa.frx", "bbb.TXT", "xyz.dbf", "abc.pdf", "aaaa.PDF", "xyz.frt", "abc.xml", "ccc.txt", "zzz.txt" };
var query= from file in FileName
           let ext = System.IO.Path.GetExtension(file).ToLower()
           orderby file
           group file by ext into g
           select g;


foreach (var group in query)
{
    Console.WriteLine($"{group.Count()} File(s) with  {group.Key} Extension");
}