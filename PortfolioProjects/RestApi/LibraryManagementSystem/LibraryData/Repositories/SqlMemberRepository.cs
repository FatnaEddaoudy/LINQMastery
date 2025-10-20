using LibraryData.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Repositories
{
    public class SqlMemberRepository : IMemberRepository
    {
        private readonly LibraryDBContext _context;
        public SqlMemberRepository(LibraryDBContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<Member>> GetAllMembersAsync()
        { 
            return await _context.Members.ToListAsync();
        }

        public Task<Member?> GetMemberByIdAsync(int memberId)
        {
            return _context.Members.FirstOrDefaultAsync(m => m.MemeberId == memberId);
        }
        public Task AddMemberAsync(Member member)
        {
            throw new NotImplementedException();
        }

        public Task DeleteMemberAsync(int memberId)
        {
            throw new NotImplementedException();
        }

        public Task SavechangeAsync()
        {
            throw new NotImplementedException();
        }

        public Task UpdateMemberAsync(Member member)
        {
            throw new NotImplementedException();
        }
    }
}
