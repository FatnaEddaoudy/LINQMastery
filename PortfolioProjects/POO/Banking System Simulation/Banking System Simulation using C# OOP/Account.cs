using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Banking_System_Simulation_using_C__OOP
{
    //Define an Account class characterized by:

    //Its balance

    //A code(account number) that is incremented automatically each time an account is created

    //Its owner, who is a Client

    //Use properties to define the access methods for the attributes of the class (the account number and balance are read-only).
    public class Account
    {
        private static int _counter = 0;
        private decimal _Balance;

        public int Code { get; }
        public decimal Balance { get { return _Balance; } } 
        public Client Owner { get; }

        public Account(Client owner)
        {
            Code = ++_counter;
            _Balance = 0;
            Owner = owner;
        }

        public void Credit(decimal amount)
        {
            if (amount > 0) _Balance += amount;
        }

        public void Credit(decimal amount, Account fromAccount)
        {
            if (amount > 0 && fromAccount._Balance >= amount)
            {
                _Balance += amount;
                fromAccount._Balance -= amount;
            }
        }

        public void Debit(decimal amount)
        {
            if (amount > 0 && _Balance >= amount)
                _Balance -= amount;
        }

        public void Debit(decimal amount, Account toAccount)
        {
            if (amount > 0 && _Balance >= amount)
            {
                _Balance -= amount;
                toAccount._Balance += amount;
            }
        }

        public void Display()
        {
            Console.WriteLine("************************");
            Console.WriteLine($"Numero de Compte: {Code}");
            Console.WriteLine($"Solde de compte: {Balance}");
            Console.WriteLine("Propriétaire du compte:");
            Owner.Display();
            Console.WriteLine("************************");
        }

        public static void DisplayTotalAccounts()
        {
            Console.WriteLine($"Total Accounts Created: {_counter}");
        }
    }
}
