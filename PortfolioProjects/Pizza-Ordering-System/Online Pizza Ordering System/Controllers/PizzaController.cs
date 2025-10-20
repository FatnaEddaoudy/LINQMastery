using Microsoft.AspNetCore.Mvc;
using Online_Pizza_Ordering_System.Models;
using Online_Pizza_Ordering_System.Repositories;

namespace Online_Pizza_Ordering_System.Controllers
{
    public class PizzaController : Controller
    {
      
        private readonly IPizza _pizzaRepository;

        public PizzaController( IPizza pizza)
        {
            _pizzaRepository = pizza;
        }

        public async Task<IActionResult> Index()
        {
            var pizzas =await _pizzaRepository.GetAllPizzas();
            return View(pizzas);
        }

    }
}
