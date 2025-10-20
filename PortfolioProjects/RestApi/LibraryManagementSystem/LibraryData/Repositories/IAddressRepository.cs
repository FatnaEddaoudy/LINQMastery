using LibraryData.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Repositories
{
    public interface IAddressRepository
    {
        Task<IEnumerable<Address>> GetAllAddressesAsync();
        Task <Address?> GetAddressesBjId(int id);
        Task AddAddressAsync(Address address);
        Task UpdateAddresesAsync(Address address);
        Task DeleteAddressAsync(int id);
        

    }
}
