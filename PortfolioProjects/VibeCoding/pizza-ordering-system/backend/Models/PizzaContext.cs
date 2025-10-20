using Microsoft.EntityFrameworkCore;

namespace PizzaOrderingAPI.Models
{
    public class PizzaContext : DbContext
    {
        public PizzaContext(DbContextOptions<PizzaContext> options) : base(options)
        {
        }
        
        public DbSet<Pizza> Pizzas { get; set; }
        public DbSet<Order> Orders { get; set; }
        public DbSet<OrderItem> OrderItems { get; set; }
        public DbSet<ContactMessage> ContactMessages { get; set; }
        
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Configure Pizza entity with decimal precision
            modelBuilder.Entity<Pizza>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.SmallPrice).HasColumnType("decimal(18,2)");
                entity.Property(e => e.MediumPrice).HasColumnType("decimal(18,2)");
                entity.Property(e => e.LargePrice).HasColumnType("decimal(18,2)");
            });
            
            // Configure Order entity with decimal precision
            modelBuilder.Entity<Order>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.TotalAmount).HasColumnType("decimal(18,2)");
                entity.HasMany(e => e.Items)
                      .WithOne(e => e.Order)
                      .HasForeignKey(e => e.OrderId);
            });
            
            // Configure OrderItem entity with decimal precision
            modelBuilder.Entity<OrderItem>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.UnitPrice).HasColumnType("decimal(18,2)");
                entity.Property(e => e.TotalPrice).HasColumnType("decimal(18,2)");
                entity.HasOne(e => e.Pizza)
                      .WithMany()
                      .HasForeignKey(e => e.PizzaId);
            });
            
            // Configure ContactMessage entity
            modelBuilder.Entity<ContactMessage>(entity =>
            {
                entity.HasKey(e => e.Id);
            });
        }
    }
}