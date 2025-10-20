using LibraryServices.Services;
using Microsoft.AspNetCore.Mvc;

namespace LibraryApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class MemberController : Controller
    {

        private readonly MemberServices _memberService;
        public MemberController(MemberServices memberService)
        {
            _memberService = memberService;
        }
        [HttpGet]
        public async Task<IActionResult> GetAllMembers()
        {
            var members = await _memberService.GetAllMembersAsync();
            return Ok(members);

        }
        [HttpGet("{id}")]
        public async Task<IActionResult> GetMemberById(int id)
        {
            var member = await _memberService.GetMemberByIdAsync(id);
            if (member == null)
            {
                return NotFound();
            }
            return Ok(member);
        }
    }
}
