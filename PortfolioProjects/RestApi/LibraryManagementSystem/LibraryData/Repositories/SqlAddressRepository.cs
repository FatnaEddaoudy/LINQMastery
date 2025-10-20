using LibraryData.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.VisualBasic;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Repositories
{
    public class SqlAddressRepository : IAddressRepository
    {
        private readonly LibraryDBContext _context;
        public SqlAddressRepository(LibraryDBContext context)
        {
            _context = context;
        }
        public async Task AddAddressAsync(Address address)
        {
           await _context.Addresses.AddAsync(address);
              await _context.SaveChangesAsync();
        }

        public async Task DeleteAddressAsync(int id)
        {
           var address = await _context.Addresses.FindAsync(id);
            if(address != null)
            {
                _context.Addresses.Remove(address);
                await _context.SaveChangesAsync();
            }
        }

        public async Task<Address?> GetAddressesBjId(int id)
        {
           return await _context.Addresses.FindAsync(id);
        }

        public async Task<IEnumerable<Address>> GetAllAddressesAsync()
        {
          return await _context.Addresses.ToListAsync();
           
        }      

        public Task UpdateAddresesAsync(Address address)
        {
           var existingAddress =  _context.Addresses.Find(address.AdressId);
            if(existingAddress != null)
            {
                // Update only the simple properties
                existingAddress.Street = address.Street;
                existingAddress.City = address.City;
                existingAddress.State = address.State;
                existingAddress.PostCode = address.PostCode;
                existingAddress.Country = address.Country;
                _context.Addresses.Update(existingAddress);
               return _context.SaveChangesAsync();
            }
            return Task.CompletedTask;
        }
    }
}
