// Author: Rick Kozak
//
// Logic for a simple application that uses two buttons
// to toggle between two messages in a label control.
//

// remove all the unused 'using' statements as a final cleanup step
// VS2019 greys the unused items
using System.Windows;

namespace Exercise1
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        // handle the user's click of the 'Press Me' button
        private void FirstPress_Click(object sender, RoutedEventArgs e)
        {
            // a label control has a Content attribute in XAML
            // here in C#, it will also have a Content property
            // all XAML attributes can be changed in C# by the corresponding property
            Message.Content = "You pressed me";
        }

        // handle the user's click of the 'Press Me Again' button
        private void SecondPress_Click(object sender, RoutedEventArgs e)
        {
            Message.Content = "You pressed me again";
        }
    }
}
