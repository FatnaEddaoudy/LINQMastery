using LibraryData.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Repositories
{
    public interface IUserRepository
    {
        bool IsUsernameTaken(string username);
        bool IsEmailTaken(string email);
        void AddUser(User user);
        User GetUserByUsername(string username);
        User GetUserByEmail(string email);
        User GetUserById(int id);
        User GetALLusers();
    }
}
