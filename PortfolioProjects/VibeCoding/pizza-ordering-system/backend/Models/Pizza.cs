using System.ComponentModel.DataAnnotations;

namespace PizzaOrderingAPI.Models
{
    public class Pizza
    {
        public int Id { get; set; }
        
        [Required]
        [MaxLength(100)]
        public string Name { get; set; } = string.Empty;
        
        [Required]
        [MaxLength(500)]
        public string Description { get; set; } = string.Empty;
        
        [Required]
        [MaxLength(50)]
        public string Category { get; set; } = string.Empty;
        
        [MaxLength(200)]
        public string Image { get; set; } = string.Empty;
        
        [MaxLength(50)]
        public string Badge { get; set; } = string.Empty;
        
        public decimal SmallPrice { get; set; }
        public decimal MediumPrice { get; set; }
        public decimal LargePrice { get; set; }
        
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
    }
    
    public class PizzaDto
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string Category { get; set; } = string.Empty;
        public string Image { get; set; } = string.Empty;
        public string Badge { get; set; } = string.Empty;
        public Dictionary<string, decimal> Prices { get; set; } = new();
    }
}