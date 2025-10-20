using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LINQ_to_Objects
{
    public enum Countries
    {
        USA,
        Italy,
    }

    public class Customer
    {
        public string Name;
        public string City;
        public Countries Country;
        public Order[] Orders;
    }
    public class Order
    {
        public int IdOrder;
        public int Quantity;
        public bool Shipped;
        public string Month;
        public int IdProduct;
        public override string ToString()
        {
            return String.Format("IdOrder: {0} – IdProduct: {1} – " +
            "Quantity: {2} – Shipped: {3} – " +
            "Month: {4}", this.IdOrder, this.IdProduct,
            this.Quantity, this.Shipped, this.Month);
        }
    }
    public class Product
    {
        public int IdProduct;
        public decimal Price;
        public override string ToString()
        {
            return String.Format("IdProduct: {0} – Price: {1}", this.IdProduct,
            this.Price);
        }
    }

}
