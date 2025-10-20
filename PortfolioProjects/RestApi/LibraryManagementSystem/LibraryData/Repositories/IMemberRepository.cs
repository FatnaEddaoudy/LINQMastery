using LibraryData.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Repositories
{
    public interface IMemberRepository
    {
        Task<IEnumerable<Member>> GetAllMembersAsync();
        Task<Member?> GetMemberByIdAsync(int memberId);
        Task AddMemberAsync(Member member);
        Task UpdateMemberAsync(Member member);
        Task DeleteMemberAsync(int memberId);
        Task SavechangeAsync();
    }
}
