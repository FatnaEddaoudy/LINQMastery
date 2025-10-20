using LibraryData.Models;
using LibraryData.Repositories;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryServices.Services
{
    public class MemberServices
    {
        private readonly IMemberRepository _memberRepository;
        public MemberServices(IMemberRepository memberRepository)
        {
            _memberRepository = memberRepository;
        }
        public async Task<IEnumerable<Member>> GetAllMembersAsync()
        {
            return await _memberRepository.GetAllMembersAsync();
        }
        public async Task<Member?> GetMemberByIdAsync(int id)
        {
            return await _memberRepository.GetMemberByIdAsync(id);
        }
    }
}
