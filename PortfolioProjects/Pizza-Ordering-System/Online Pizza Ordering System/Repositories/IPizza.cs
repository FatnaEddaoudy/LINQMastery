using Online_Pizza_Ordering_System.Models;
using System.Linq;

namespace Online_Pizza_Ordering_System.Repositories
{
    public interface IPizza
    {
        Task<IEnumerable<Pizza>> GetAllPizzas();
        Task<Pizza> GetPizzaById(int id);
        Task<Pizza> AddPizza();
        Task<Pizza> UpdatePizza(int id);
        Task<Pizza> DeletePizza(int id);

    }
}
