using Microsoft.AspNetCore.Http.HttpResults;

namespace Online_Pizza_Ordering_System.Models
{
    public class Pizza
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public string ImageUrl { get; set; }
        public Size Size { get; set; }
        public string Category { get; set; }
        public string Badge { get; set; } 
        public decimal SmallPrice { get; set; }
        public decimal MediumPrice { get; set; }
        public decimal LargePrice { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime UpdatedAt { get; set; }
    }
}
