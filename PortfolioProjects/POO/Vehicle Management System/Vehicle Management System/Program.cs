using System;

namespace VehicleManagementSystem
{
    // ===== Abstract Class =====
    abstract class Vehicle
    {
        // Static field to auto-increment registration number
        private static int counter = 0;

        // Private fields
        private int registrationNumber;
        private int modelYear;
        private double price;

        // Constructor
        public Vehicle(int modelYear, double price)
        {
            counter++;
            this.registrationNumber = counter;
            this.modelYear = modelYear;
            this.price = price;
        }

        // Properties
        public int RegistrationNumber => registrationNumber;
        public int ModelYear
        {
            get { return modelYear; }
            set { modelYear = value; }
        }

        public double Price
        {
            get { return price; }
            set { price = value; }
        }

        // Abstract methods
        public abstract void Start();
        public abstract void Accelerate();

        // ToString override
        public override string ToString()
        {
            return $"[Vehicle {registrationNumber}] Model Year: {modelYear}, Price: {price} DH";
        }
    }

    // ===== Car Class =====
    class Car : Vehicle
    {
        public Car(int modelYear, double price)
            : base(modelYear, price)
        {
        }

        public override void Start()
        {
            Console.WriteLine($"Car {RegistrationNumber} is starting...");
        }

        public override void Accelerate()
        {
            Console.WriteLine($"Car {RegistrationNumber} is accelerating quickly!");
        }

        public override string ToString()
        {
            return $"Car: {base.ToString()}";
        }
    }

    // ===== Truck Class =====
    class Truck : Vehicle
    {
        public Truck(int modelYear, double price)
            : base(modelYear, price)
        {
        }

        public override void Start()
        {
            Console.WriteLine($"Truck {RegistrationNumber} engine roars to life...");
        }

        public override void Accelerate()
        {
            Console.WriteLine($"Truck {RegistrationNumber} is gaining speed steadily!");
        }

        public override string ToString()
        {
            return $"Truck {base.ToString()}";
        }
    }

    // ===== Test Class =====
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Vehicle Management System ===\n");

            // Create a list of vehicles
            List<Vehicle> vehicles = new List<Vehicle>
            {
                new Car(2022, 150000),
                new Car(2020, 120000),
                new Truck(2018, 350000),
                new Truck(2023, 400000)
            };

            // Loop through and display all vehicles
            foreach (var v in vehicles)
            {
                Console.WriteLine(v.ToString());   // Calls ToString()
                v.Start();
                v.Accelerate();
                Console.WriteLine();
            }

            Console.WriteLine("=== End of Test ===");
        }
    }
}
