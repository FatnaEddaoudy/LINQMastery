using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Online_Pizza_Ordering_System.Models;
using Online_Pizza_Ordering_System.Repositories;

namespace Online_Pizza_Ordering_System.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private readonly IPizza _pizzaRepository;

        public HomeController(ILogger<HomeController> logger,IPizza pizza)
        {
            _logger = logger;
            _pizzaRepository = pizza;
        }

        public IActionResult Index()
        {
            // Redirects to the Index action of the PizzaController
            return RedirectToAction("Index", "Pizza");
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
