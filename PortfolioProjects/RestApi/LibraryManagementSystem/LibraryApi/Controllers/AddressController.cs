using LibraryData.Models;
using LibraryServices.Services;
using Microsoft.AspNetCore.Mvc;

namespace LibraryApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AddressController : Controller
    {
        private readonly AddressServices _addressServices;
        public AddressController(AddressServices addressServices)
        {
            _addressServices = addressServices;
        }
        [HttpGet]
        public async Task<IActionResult> GetAllAddressesAsync()
        {
            var addresses = await _addressServices.GetAllAddressesAsync();
            return addresses == null ? NotFound() : Ok(addresses);
        }
        [HttpGet("{id}")]
        public async Task<IActionResult> GetAddressesById(int id)
        {
            var address = await _addressServices.GetAddressesBjId(id);
            return address == null ? NotFound() : Ok(address);
        }
        [HttpPost]
        public async Task AddAddressAsync(Address address)
        {
            await _addressServices.AddAddressAsync(address);
        }
        [HttpPut]
        public async Task<IActionResult>  UpdateAddressAsync(int id, [FromBody] Address address)
        {
            if (address == null)
                return BadRequest("Adress is required");
            if (id != address.AdressId)
            {
                return BadRequest("ID mismatch");
            }
                await _addressServices.UpdateAddresesAsync(address);
            return Ok(address);
        }

        [HttpDelete("{id}")]
        public async Task DeleteAddressAsync(int id)
        {
            await _addressServices.DeleteAddressAsync(id);
        }
    }
}