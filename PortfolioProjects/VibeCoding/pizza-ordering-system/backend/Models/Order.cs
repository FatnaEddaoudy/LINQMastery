using System.ComponentModel.DataAnnotations;

namespace PizzaOrderingAPI.Models
{
    public class Order
    {
        public int Id { get; set; }
        
        [Required]
        [MaxLength(100)]
        public string CustomerName { get; set; } = string.Empty;
        
        [Required]
        [MaxLength(100)]
        public string CustomerEmail { get; set; } = string.Empty;
        
        [Required]
        [MaxLength(15)]
        public string CustomerPhone { get; set; } = string.Empty;
        
        [Required]
        [MaxLength(200)]
        public string DeliveryAddress { get; set; } = string.Empty;
        
        public decimal TotalAmount { get; set; }
        
        [Required]
        [MaxLength(20)]
        public string Status { get; set; } = "Pending";
        
        public DateTime OrderDate { get; set; } = DateTime.UtcNow;
        public DateTime? EstimatedDelivery { get; set; }
        
        public List<OrderItem> Items { get; set; } = new();
    }
    
    public class OrderItem
    {
        public int Id { get; set; }
        public int OrderId { get; set; }
        public int PizzaId { get; set; }
        
        [Required]
        [MaxLength(20)]
        public string Size { get; set; } = string.Empty;
        
        public int Quantity { get; set; }
        public decimal UnitPrice { get; set; }
        public decimal TotalPrice { get; set; }
        
        public Pizza? Pizza { get; set; }
        public Order? Order { get; set; }
    }
    
    public class CreateOrderDto
    {
        [Required]
        public string CustomerName { get; set; } = string.Empty;
        
        [Required]
        [EmailAddress]
        public string CustomerEmail { get; set; } = string.Empty;
        
        [Required]
        public string CustomerPhone { get; set; } = string.Empty;
        
        [Required]
        public string DeliveryAddress { get; set; } = string.Empty;
        
        [Required]
        public List<CreateOrderItemDto> Items { get; set; } = new();
    }
    
    public class CreateOrderItemDto
    {
        public int PizzaId { get; set; }
        
        [Required]
        public string Size { get; set; } = string.Empty;
        
        [Range(1, 10)]
        public int Quantity { get; set; }
    }
    
    public class OrderDto
    {
        public int Id { get; set; }
        public string CustomerName { get; set; } = string.Empty;
        public string CustomerEmail { get; set; } = string.Empty;
        public string CustomerPhone { get; set; } = string.Empty;
        public string DeliveryAddress { get; set; } = string.Empty;
        public decimal TotalAmount { get; set; }
        public string Status { get; set; } = string.Empty;
        public DateTime OrderDate { get; set; }
        public DateTime? EstimatedDelivery { get; set; }
        public List<OrderItemDto> Items { get; set; } = new();
    }
    
    public class OrderItemDto
    {
        public int Id { get; set; }
        public int PizzaId { get; set; }
        public string PizzaName { get; set; } = string.Empty;
        public string Size { get; set; } = string.Empty;
        public int Quantity { get; set; }
        public decimal UnitPrice { get; set; }
        public decimal TotalPrice { get; set; }
    }
}