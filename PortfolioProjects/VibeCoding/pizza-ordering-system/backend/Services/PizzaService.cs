using Microsoft.EntityFrameworkCore;
using PizzaOrderingAPI.Models;

namespace PizzaOrderingAPI.Services
{
    public interface IPizzaService
    {
        Task<IEnumerable<PizzaDto>> GetAllPizzasAsync();
        Task<PizzaDto?> GetPizzaByIdAsync(int id);
        Task<PizzaDto> CreatePizzaAsync(Pizza pizza);
        Task<PizzaDto?> UpdatePizzaAsync(int id, Pizza pizza);
        Task<bool> DeletePizzaAsync(int id);
        Task SeedDataAsync();
    }
    
    public class PizzaService : IPizzaService
    {
        private readonly PizzaContext _context;
        
        public PizzaService(PizzaContext context)
        {
            _context = context;
        }
        
        public async Task<IEnumerable<PizzaDto>> GetAllPizzasAsync()
        {
            var pizzas = await _context.Pizzas.ToListAsync();
            return pizzas.Select(MapToDto);
        }
        
        public async Task<PizzaDto?> GetPizzaByIdAsync(int id)
        {
            var pizza = await _context.Pizzas.FindAsync(id);
            return pizza != null ? MapToDto(pizza) : null;
        }
        
        public async Task<PizzaDto> CreatePizzaAsync(Pizza pizza)
        {
            _context.Pizzas.Add(pizza);
            await _context.SaveChangesAsync();
            return MapToDto(pizza);
        }
        
        public async Task<PizzaDto?> UpdatePizzaAsync(int id, Pizza pizza)
        {
            var existingPizza = await _context.Pizzas.FindAsync(id);
            if (existingPizza == null) return null;
            
            existingPizza.Name = pizza.Name;
            existingPizza.Description = pizza.Description;
            existingPizza.Category = pizza.Category;
            existingPizza.Image = pizza.Image;
            existingPizza.Badge = pizza.Badge;
            existingPizza.SmallPrice = pizza.SmallPrice;
            existingPizza.MediumPrice = pizza.MediumPrice;
            existingPizza.LargePrice = pizza.LargePrice;
            existingPizza.UpdatedAt = DateTime.UtcNow;
            
            await _context.SaveChangesAsync();
            return MapToDto(existingPizza);
        }
        
        public async Task<bool> DeletePizzaAsync(int id)
        {
            var pizza = await _context.Pizzas.FindAsync(id);
            if (pizza == null) return false;
            
            _context.Pizzas.Remove(pizza);
            await _context.SaveChangesAsync();
            return true;
        }
        
        public async Task SeedDataAsync()
        {
            if (await _context.Pizzas.AnyAsync()) return;
            
            var pizzas = new List<Pizza>
            {
                new Pizza
                {
                    Name = "Margherita",
                    Description = "Fresh tomatoes, mozzarella cheese, basil, and olive oil",
                    Category = "classic",
                    Image = "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&h=300&fit=crop&crop=center",
                    Badge = "Popular",
                    SmallPrice = 12.99m,
                    MediumPrice = 16.99m,
                    LargePrice = 20.99m
                },
                new Pizza
                {
                    Name = "Pepperoni",
                    Description = "Classic pepperoni with mozzarella cheese and tomato sauce",
                    Category = "classic",
                    Image = "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400&h=300&fit=crop&crop=center",
                    Badge = "Best Seller",
                    SmallPrice = 14.99m,
                    MediumPrice = 18.99m,
                    LargePrice = 22.99m
                },
                new Pizza
                {
                    Name = "Supreme",
                    Description = "Pepperoni, sausage, mushrooms, bell peppers, onions, and olives",
                    Category = "specialty",
                    Image = "https://images.unsplash.com/photo-1571997478779-2adcbbe9ab2f?w=400&h=300&fit=crop&crop=center",
                    Badge = "Chef's Choice",
                    SmallPrice = 18.99m,
                    MediumPrice = 22.99m,
                    LargePrice = 26.99m
                },
                new Pizza
                {
                    Name = "Hawaiian",
                    Description = "Ham, pineapple, and mozzarella cheese",
                    Category = "specialty",
                    Image = "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop&crop=center",
                    Badge = "",
                    SmallPrice = 16.99m,
                    MediumPrice = 20.99m,
                    LargePrice = 24.99m
                },
                new Pizza
                {
                    Name = "Vegetarian Deluxe",
                    Description = "Mushrooms, bell peppers, onions, tomatoes, and olives",
                    Category = "vegetarian",
                    Image = "https://images.unsplash.com/photo-1593560708920-61dd61444791?w=400&h=300&fit=crop&crop=center",
                    Badge = "Healthy",
                    SmallPrice = 15.99m,
                    MediumPrice = 19.99m,
                    LargePrice = 23.99m
                },
                new Pizza
                {
                    Name = "Meat Lovers",
                    Description = "Pepperoni, sausage, ham, bacon, and ground beef",
                    Category = "specialty",
                    Image = "https://images.unsplash.com/photo-1594007654729-407eedc4be65?w=400&h=300&fit=crop&crop=center",
                    Badge = "Protein Packed",
                    SmallPrice = 19.99m,
                    MediumPrice = 24.99m,
                    LargePrice = 28.99m
                },
                new Pizza
                {
                    Name = "BBQ Chicken",
                    Description = "Grilled chicken, BBQ sauce, red onions, and cilantro",
                    Category = "specialty",
                    Image = "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop&crop=center",
                    Badge = "",
                    SmallPrice = 17.99m,
                    MediumPrice = 21.99m,
                    LargePrice = 25.99m
                },
                new Pizza
                {
                    Name = "Four Cheese",
                    Description = "Mozzarella, parmesan, cheddar, and goat cheese",
                    Category = "classic",
                    Image = "https://images.unsplash.com/photo-1541745537411-b8046dc6d66c?w=400&h=300&fit=crop&crop=center",
                    Badge = "Cheese Lovers",
                    SmallPrice = 16.99m,
                    MediumPrice = 20.99m,
                    LargePrice = 24.99m
                },
                new Pizza
                {
                    Name = "Mediterranean",
                    Description = "Feta cheese, olives, tomatoes, red onions, and herbs",
                    Category = "vegetarian",
                    Image = "https://images.unsplash.com/photo-1579952363873-27d3bfad9c0d?w=400&h=300&fit=crop&crop=center",
                    Badge = "Fresh",
                    SmallPrice = 17.99m,
                    MediumPrice = 21.99m,
                    LargePrice = 25.99m
                },
                new Pizza
                {
                    Name = "Buffalo Chicken",
                    Description = "Buffalo chicken, celery, red onions, and ranch dressing",
                    Category = "specialty",
                    Image = "https://images.unsplash.com/photo-1555072956-7758afb20e8f?w=400&h=300&fit=crop&crop=center",
                    Badge = "Spicy",
                    SmallPrice = 18.99m,
                    MediumPrice = 22.99m,
                    LargePrice = 26.99m
                },
                new Pizza
                {
                    Name = "Veggie Supreme",
                    Description = "Spinach, artichokes, sun-dried tomatoes, and feta cheese",
                    Category = "vegetarian",
                    Image = "https://images.unsplash.com/photo-1552539618-7eec9b4d1796?w=400&h=300&fit=crop&crop=center",
                    Badge = "Gourmet",
                    SmallPrice = 16.99m,
                    MediumPrice = 20.99m,
                    LargePrice = 24.99m
                },
                new Pizza
                {
                    Name = "White Pizza",
                    Description = "Ricotta, mozzarella, garlic, and fresh herbs",
                    Category = "classic",
                    Image = "https://images.unsplash.com/photo-1585238342024-78d387f4a707?w=400&h=300&fit=crop&crop=center",
                    Badge = "",
                    SmallPrice = 15.99m,
                    MediumPrice = 19.99m,
                    LargePrice = 23.99m
                }
            };
            
            _context.Pizzas.AddRange(pizzas);
            await _context.SaveChangesAsync();
        }
        
        private static PizzaDto MapToDto(Pizza pizza)
        {
            return new PizzaDto
            {
                Id = pizza.Id,
                Name = pizza.Name,
                Description = pizza.Description,
                Category = pizza.Category,
                Image = pizza.Image,
                Badge = pizza.Badge,
                Prices = new Dictionary<string, decimal>
                {
                    { "small", pizza.SmallPrice },
                    { "medium", pizza.MediumPrice },
                    { "large", pizza.LargePrice }
                }
            };
        }
    }
}