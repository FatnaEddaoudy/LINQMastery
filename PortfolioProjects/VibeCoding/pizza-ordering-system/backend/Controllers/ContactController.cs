using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PizzaOrderingAPI.Models;
using PizzaOrderingAPI.Services;

namespace PizzaOrderingAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ContactController : ControllerBase
    {
        private readonly PizzaContext _context;
        private readonly IEmailService _emailService;
        
        public ContactController(PizzaContext context, IEmailService emailService)
        {
            _context = context;
            _emailService = emailService;
        }
        
        /// <summary>
        /// Submit a contact message
        /// </summary>
        /// <param name="createContactDto">Contact message data</param>
        /// <returns>Success response</returns>
        [HttpPost]
        public async Task<ActionResult> SubmitContactMessage(CreateContactMessageDto createContactDto)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }
            
            var contactMessage = new ContactMessage
            {
                Name = createContactDto.Name,
                Email = createContactDto.Email,
                Message = createContactDto.Message,
                CreatedAt = DateTime.UtcNow,
                IsRead = false
            };
            
            _context.ContactMessages.Add(contactMessage);
            await _context.SaveChangesAsync();
            
            return Ok(new { success = true, message = "Message received successfully!" });
        }
        
        /// <summary>
        /// Get all contact messages (Admin only)
        /// </summary>
        /// <returns>List of contact messages</returns>
        [HttpGet]
        public async Task<ActionResult<IEnumerable<ContactMessage>>> GetContactMessages()
        {
            var messages = await _context.ContactMessages
                .OrderByDescending(m => m.CreatedAt)
                .ToListAsync();
                
            return Ok(messages);
        }
        
        /// <summary>
        /// Mark contact message as read (Admin only)
        /// </summary>
        /// <param name="id">Message ID</param>
        /// <returns>Success status</returns>
        [HttpPatch("{id}/read")]
        public async Task<ActionResult> MarkAsRead(int id)
        {
            var message = await _context.ContactMessages.FindAsync(id);
            
            if (message == null)
            {
                return NotFound($"Contact message with ID {id} not found.");
            }
            
            message.IsRead = true;
            await _context.SaveChangesAsync();
            
            return Ok(new { success = true, message = "Message marked as read." });
        }

        /// <summary>
        /// Reply to a contact message (Admin only)
        /// </summary>
        /// <param name="id">Message ID</param>
        /// <param name="replyDto">Reply content</param>
        /// <returns>Success status</returns>
        [HttpPost("{id}/reply")]
        public async Task<ActionResult> ReplyToMessage(int id, [FromBody] ReplyMessageDto replyDto)
        {
            var message = await _context.ContactMessages.FindAsync(id);
            
            if (message == null)
            {
                return NotFound($"Contact message with ID {id} not found.");
            }

            try
            {
                await _emailService.SendReplyAsync(message.Email, message.Message, replyDto.Reply);
                
                // Mark as read when replied
                message.IsRead = true;
                await _context.SaveChangesAsync();
                
                return Ok(new { success = true, message = "Reply sent successfully!" });
            }
            catch (Exception ex)
            {
                return BadRequest($"Failed to send reply: {ex.Message}");
            }
        }
    }

    public class ReplyMessageDto
    {
        public string Reply { get; set; } = string.Empty;
    }
}