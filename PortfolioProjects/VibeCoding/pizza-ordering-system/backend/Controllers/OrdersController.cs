using Microsoft.AspNetCore.Mvc;
using PizzaOrderingAPI.Models;
using PizzaOrderingAPI.Services;

namespace PizzaOrderingAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class OrdersController : ControllerBase
    {
        private readonly IOrderService _orderService;
        
        public OrdersController(IOrderService orderService)
        {
            _orderService = orderService;
        }
        
        /// <summary>
        /// Create a new order
        /// </summary>
        /// <param name="createOrderDto">Order data</param>
        /// <returns>Created order</returns>
        [HttpPost]
        public async Task<ActionResult<OrderDto>> CreateOrder(CreateOrderDto createOrderDto)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }
            
            try
            {
                var order = await _orderService.CreateOrderAsync(createOrderDto);
                return CreatedAtAction(nameof(GetOrder), new { id = order.Id }, order);
            }
            catch (Exception ex)
            {
                return BadRequest($"Failed to create order: {ex.Message}");
            }
        }
        
        /// <summary>
        /// Get a specific order by ID
        /// </summary>
        /// <param name="id">Order ID</param>
        /// <returns>Order details</returns>
        [HttpGet("{id}")]
        public async Task<ActionResult<OrderDto>> GetOrder(int id)
        {
            var order = await _orderService.GetOrderByIdAsync(id);
            
            if (order == null)
            {
                return NotFound($"Order with ID {id} not found.");
            }
            
            return Ok(order);
        }
        
        /// <summary>
        /// Get all orders (Admin only)
        /// </summary>
        /// <returns>List of all orders</returns>
        [HttpGet]
        public async Task<ActionResult<IEnumerable<OrderDto>>> GetOrders()
        {
            var orders = await _orderService.GetAllOrdersAsync();
            return Ok(orders);
        }
        
        /// <summary>
        /// Update order status (Admin only)
        /// </summary>
        /// <param name="id">Order ID</param>
        /// <param name="status">New status</param>
        /// <returns>Updated order</returns>
        [HttpPatch("{id}/status")]
        public async Task<ActionResult<OrderDto>> UpdateOrderStatus(int id, [FromBody] string status)
        {
            var validStatuses = new[] { "Pending", "Confirmed", "Preparing", "Baking", "Ready", "Out for Delivery", "Delivered", "Cancelled" };
            
            if (!validStatuses.Contains(status))
            {
                return BadRequest($"Invalid status. Valid statuses are: {string.Join(", ", validStatuses)}");
            }
            
            var updatedOrder = await _orderService.UpdateOrderStatusAsync(id, status);
            
            if (updatedOrder == null)
            {
                return NotFound($"Order with ID {id} not found.");
            }
            
            return Ok(updatedOrder);
        }
    }
}