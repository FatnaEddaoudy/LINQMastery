using Microsoft.EntityFrameworkCore;
using PizzaOrderingAPI.Models;

namespace PizzaOrderingAPI.Services
{
    public interface IOrderService
    {
        Task<OrderDto> CreateOrderAsync(CreateOrderDto createOrderDto);
        Task<OrderDto?> GetOrderByIdAsync(int id);
        Task<IEnumerable<OrderDto>> GetAllOrdersAsync();
        Task<OrderDto?> UpdateOrderStatusAsync(int id, string status);
    }
    
    public class OrderService : IOrderService
    {
        private readonly PizzaContext _context;
        
        public OrderService(PizzaContext context)
        {
            _context = context;
        }
        
        public async Task<OrderDto> CreateOrderAsync(CreateOrderDto createOrderDto)
        {
            var order = new Order
            {
                CustomerName = createOrderDto.CustomerName,
                CustomerEmail = createOrderDto.CustomerEmail,
                CustomerPhone = createOrderDto.CustomerPhone,
                DeliveryAddress = createOrderDto.DeliveryAddress,
                Status = "Pending",
                OrderDate = DateTime.UtcNow,
                EstimatedDelivery = DateTime.UtcNow.AddMinutes(30)
            };
            
            decimal totalAmount = 0;
            
            foreach (var itemDto in createOrderDto.Items)
            {
                var pizza = await _context.Pizzas.FindAsync(itemDto.PizzaId);
                if (pizza == null) continue;
                
                decimal unitPrice = itemDto.Size.ToLower() switch
                {
                    "small" => pizza.SmallPrice,
                    "medium" => pizza.MediumPrice,
                    "large" => pizza.LargePrice,
                    _ => pizza.MediumPrice
                };
                
                var orderItem = new OrderItem
                {
                    PizzaId = itemDto.PizzaId,
                    Size = itemDto.Size,
                    Quantity = itemDto.Quantity,
                    UnitPrice = unitPrice,
                    TotalPrice = unitPrice * itemDto.Quantity
                };
                
                order.Items.Add(orderItem);
                totalAmount += orderItem.TotalPrice;
            }
            
            order.TotalAmount = totalAmount;
            
            _context.Orders.Add(order);
            await _context.SaveChangesAsync();
            
            return await GetOrderByIdAsync(order.Id) ?? throw new InvalidOperationException("Failed to create order");
        }
        
        public async Task<OrderDto?> GetOrderByIdAsync(int id)
        {
            var order = await _context.Orders
                .Include(o => o.Items)
                .ThenInclude(i => i.Pizza)
                .FirstOrDefaultAsync(o => o.Id == id);
                
            return order != null ? MapToDto(order) : null;
        }
        
        public async Task<IEnumerable<OrderDto>> GetAllOrdersAsync()
        {
            var orders = await _context.Orders
                .Include(o => o.Items)
                .ThenInclude(i => i.Pizza)
                .OrderByDescending(o => o.OrderDate)
                .ToListAsync();
                
            return orders.Select(MapToDto);
        }
        
        public async Task<OrderDto?> UpdateOrderStatusAsync(int id, string status)
        {
            var order = await _context.Orders.FindAsync(id);
            if (order == null) return null;
            
            order.Status = status;
            await _context.SaveChangesAsync();
            
            return await GetOrderByIdAsync(id);
        }
        
        private static OrderDto MapToDto(Order order)
        {
            return new OrderDto
            {
                Id = order.Id,
                CustomerName = order.CustomerName,
                CustomerEmail = order.CustomerEmail,
                CustomerPhone = order.CustomerPhone,
                DeliveryAddress = order.DeliveryAddress,
                TotalAmount = order.TotalAmount,
                Status = order.Status,
                OrderDate = order.OrderDate,
                EstimatedDelivery = order.EstimatedDelivery,
                Items = order.Items.Select(item => new OrderItemDto
                {
                    Id = item.Id,
                    PizzaId = item.PizzaId,
                    PizzaName = item.Pizza?.Name ?? "",
                    Size = item.Size,
                    Quantity = item.Quantity,
                    UnitPrice = item.UnitPrice,
                    TotalPrice = item.TotalPrice
                }).ToList()
            };
        }
    }
}