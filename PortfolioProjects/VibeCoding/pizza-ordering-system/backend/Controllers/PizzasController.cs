using Microsoft.AspNetCore.Mvc;
using PizzaOrderingAPI.Models;
using PizzaOrderingAPI.Services;

namespace PizzaOrderingAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class PizzasController : ControllerBase
    {
        private readonly IPizzaService _pizzaService;
        
        public PizzasController(IPizzaService pizzaService)
        {
            _pizzaService = pizzaService;
        }
        
        /// <summary>
        /// Get all pizzas
        /// </summary>
        /// <returns>List of all pizzas</returns>
        [HttpGet]
        public async Task<ActionResult<IEnumerable<PizzaDto>>> GetPizzas()
        {
            var pizzas = await _pizzaService.GetAllPizzasAsync();
            return Ok(pizzas);
        }
        
        /// <summary>
        /// Get a specific pizza by ID
        /// </summary>
        /// <param name="id">Pizza ID</param>
        /// <returns>Pizza details</returns>
        [HttpGet("{id}")]
        public async Task<ActionResult<PizzaDto>> GetPizza(int id)
        {
            var pizza = await _pizzaService.GetPizzaByIdAsync(id);
            
            if (pizza == null)
            {
                return NotFound($"Pizza with ID {id} not found.");
            }
            
            return Ok(pizza);
        }
        
        /// <summary>
        /// Create a new pizza (Admin only)
        /// </summary>
        /// <param name="pizza">Pizza data</param>
        /// <returns>Created pizza</returns>
        [HttpPost]
        public async Task<ActionResult<PizzaDto>> CreatePizza(Pizza pizza)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }
            
            var createdPizza = await _pizzaService.CreatePizzaAsync(pizza);
            return CreatedAtAction(nameof(GetPizza), new { id = createdPizza.Id }, createdPizza);
        }
        
        /// <summary>
        /// Update an existing pizza (Admin only)
        /// </summary>
        /// <param name="id">Pizza ID</param>
        /// <param name="pizza">Updated pizza data</param>
        /// <returns>Updated pizza</returns>
        [HttpPut("{id}")]
        public async Task<ActionResult<PizzaDto>> UpdatePizza(int id, Pizza pizza)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }
            
            var updatedPizza = await _pizzaService.UpdatePizzaAsync(id, pizza);
            
            if (updatedPizza == null)
            {
                return NotFound($"Pizza with ID {id} not found.");
            }
            
            return Ok(updatedPizza);
        }
        
        /// <summary>
        /// Delete a pizza (Admin only)
        /// </summary>
        /// <param name="id">Pizza ID</param>
        /// <returns>Success status</returns>
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeletePizza(int id)
        {
            var success = await _pizzaService.DeletePizzaAsync(id);
            
            if (!success)
            {
                return NotFound($"Pizza with ID {id} not found.");
            }
            
            return NoContent();
        }
    }
}