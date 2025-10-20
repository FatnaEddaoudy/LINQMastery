using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Models
{
    public class Role
    {
        public int RoleId { get; set; }
        [Required(ErrorMessage = "Role name is required")]
        public string Name { get; set; }
        public ICollection<UserRole> UserRoles { get; set; }=new List<UserRole>();
    }
}
