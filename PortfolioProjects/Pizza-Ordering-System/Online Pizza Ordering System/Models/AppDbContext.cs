using Microsoft.EntityFrameworkCore;

namespace Online_Pizza_Ordering_System.Models
{
    public class AppDbContext: DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
        }
        public DbSet<Pizza> Pizzas { get; set; }


    }
}
