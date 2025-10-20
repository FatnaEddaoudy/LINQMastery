
//------------Exercise 16--------------------------------

//Write a program in C# Sharp to calculate size of file using LINQ.
//Expected Output :
////The Average file size is 3.4 MB
///

using System.Dynamic;
using System.IO;

class Program
{
    static void Main(string[] args)
    {
        //first  Read the path file Data source

        string path = @"C:\Users\tdi-f\Pictures";
        //Get all files in that path
        var files =Directory.GetFiles(path);

        //now i use query syntax to get the size of each file
        var fileSizes = from file in files
                        let fileInfo = new FileInfo(file)
                        select fileInfo.Length;

        // Convert bytes to MB (1 MB = 1024 * 1024 bytes)
        double averageSize = fileSizes.Average() / (1024 * 1024); // Convert to MB
        Console.WriteLine($"The Average file size is {averageSize:F1} MB");
    }
}