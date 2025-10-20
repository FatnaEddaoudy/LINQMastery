namespace Simple_Member_Management_System
{
    internal static class Program
    {
        /// <summary>
        ///  The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            // To customize application configuration such as set high DPI settings or default font,
            // see https://aka.ms/applicationconfiguration.
            ApplicationConfiguration.Initialize();
            Application.Run(new Main());
        }
    }
}


//*******Description:
//This desktop application manages data using lists and implements basic CRUD (Create, Read, Update, Delete) operations. 
//It includes exception handling and provides functionality to export and import DataGridView data to and from JSON files,
//ensuring data persistence and easy data transfer.