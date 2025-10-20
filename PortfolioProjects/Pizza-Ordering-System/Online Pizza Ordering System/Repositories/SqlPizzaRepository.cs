using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.EntityFrameworkCore;
using Online_Pizza_Ordering_System.Models;
using System.Threading.Tasks;

namespace Online_Pizza_Ordering_System.Repositories
{
    public class SqlPizzaRepository : IPizza
    {
        public SqlPizzaRepository() { }
        private readonly AppDbContext _context;
        public SqlPizzaRepository(AppDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<Pizza>> GetAllPizzas()
        {
            return await _context.Pizzas.ToListAsync();
        }

        public Task<Pizza> GetPizzaById(int id)
        {
            throw new NotImplementedException();
        }

        public Task<Pizza> AddPizza()
        {
            throw new NotImplementedException();
        }

        public Task<Pizza> UpdatePizza(int id)
        {
            throw new NotImplementedException();
        }

        public Task<Pizza> DeletePizza(int id)
        {
            throw new NotImplementedException();
        }
    }
}
