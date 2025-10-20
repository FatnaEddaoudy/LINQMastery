using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LibraryData.Models
{
    public class LibraryDBContext:DbContext
    {

        public LibraryDBContext()
        {

        }
        public LibraryDBContext(DbContextOptions<LibraryDBContext> options)
       : base(options)
        {
        }
        public DbSet<Address> Addresses { get; set; }
        public DbSet<Author> Authors { get; set; }
        public DbSet<Genre> Genres { get; set; }
        public DbSet<Book> Books { get; set; }
        public DbSet<Member> Members { get; set; }
        public DbSet<Borrowing> Borrowings { get; set; }
        public DbSet<User> Users { get; set; }
        public DbSet<Role> Roles { get; set; }
        public DbSet<UserRole> UserRole{ get; set; }
        protected override void OnModelCreating(ModelBuilder mb)
        {
            mb.Entity<UserRole>().HasKey(x => new { x.UserId, x.RoleId });
            mb.Entity<Member>().HasIndex(m => m.Email).IsUnique();
            mb.Entity<User>().HasIndex(u => u.Email).IsUnique();

            mb.Entity<Member>()
                .HasOne(m => m.User)
                .WithOne(u => u.Member)
               .HasForeignKey<Member>(m => m.UserId); // Member is dependent
            mb.Entity<Address>().HasKey(a => a.AdressId);
            mb.Entity<Author>().HasKey(a => a.AuthorId);
            mb.Entity<Genre>().HasKey(g => g.GenreId);
            mb.Entity<Book>().HasKey(b => b.BookID);
            mb.Entity<Member>().HasKey(m => m.MemeberId);
            mb.Entity<Borrowing>().HasKey(b => b.BorrowId);
            mb.Entity<User>().HasKey(u => u.UserId);
            mb.Entity<Role>().HasKey(r => r.RoleId);

        }
      

    }
}
