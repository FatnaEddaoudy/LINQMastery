using LibraryData.Models;
using LibraryData.Repositories;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryServices.Services
{
    public class AddressServices
    {
        private readonly IAddressRepository _addressRepository;
        public AddressServices(IAddressRepository addressRepository)
        {
            _addressRepository = addressRepository;
        }
        public async Task<IEnumerable<Address>> GetAllAddressesAsync()
        {
            return await _addressRepository.GetAllAddressesAsync();

        }
        public async Task<Address?> GetAddressesBjId(int id)
        {
            return await _addressRepository.GetAddressesBjId(id);
        }
        public async Task AddAddressAsync(Address address)
        {
            await _addressRepository.AddAddressAsync(address);
        }

        public async Task DeleteAddressAsync(int id)
        {
             await _addressRepository.DeleteAddressAsync(id);
        }
        public async Task UpdateAddresesAsync(Address address)
        {
            await _addressRepository.UpdateAddresesAsync(address);
        }
    }
}
