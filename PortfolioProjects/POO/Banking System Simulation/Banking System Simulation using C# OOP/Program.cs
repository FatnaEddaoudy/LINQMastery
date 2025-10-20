using System;
using System.Collections.Generic;
using Banking_System_Simulation_using_C__OOP;
using System;

class Program
{
    static void Main(string[] args)
    {
        //----------Clients----------
        Client client1 = new Client("EE111222", "Salim", "Omar", "06111111");
        Client client2 = new Client("EE333444", "Karimi", "Samir", "06222222");

        //----------Accounts----------
        Account account1 = new Account(client1);
        Account account2 = new Account(client2);

        List<Account> accounts = new List<Account> { account1, account2 };

        //----------Account 1----------
        Console.WriteLine("Account 1:");
        Console.WriteLine("Account details:");
        account1.Display();

        Console.WriteLine("Depositing 5000 into Account 1");
        account1.Credit(5000);
        account1.Display();

        Console.WriteLine("Withdrawing 1000 from Account 1");
        account1.Debit(1000);
        account1.Display();

        //----------Account 2 operations----------
        Console.WriteLine("\nAccount 2:");
        Console.WriteLine("Account details:");
        account2.Display();

        Console.WriteLine("Credit Account 2 from Account 1: 3000");
        account2.Credit(3000, account1);

        Console.WriteLine("Debit Account 1 and credit Account 2: 1000");
        account1.Debit(1000, account2);

        //----------Final display----------
        Console.WriteLine("\nFinal state of accounts:");
        account1.Display();
        account2.Display();

        Account.DisplayTotalAccounts();

        Console.WriteLine("\nSimulation finished.");



    }
}