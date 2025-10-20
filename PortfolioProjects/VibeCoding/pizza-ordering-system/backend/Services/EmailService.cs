using MailKit.Net.Smtp;
using MimeKit;
using Microsoft.Extensions.Configuration;

namespace PizzaOrderingAPI.Services
{
    public interface IEmailService
    {
        Task SendEmailAsync(string toEmail, string subject, string message);
        Task SendReplyAsync(string toEmail, string originalMessage, string reply);
    }

    public class EmailService : IEmailService
    {
        private readonly IConfiguration _configuration;

        public EmailService(IConfiguration configuration)
        {
            _configuration = configuration;
        }

        public async Task SendEmailAsync(string toEmail, string subject, string message)
        {
            var email = new MimeMessage();
            email.From.Add(new MailboxAddress("Pizza Ordering System", _configuration["Email:FromEmail"]));
            email.To.Add(new MailboxAddress("", toEmail));
            email.Subject = subject;

            var bodyBuilder = new BodyBuilder
            {
                HtmlBody = $@"
                    <div style='font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;'>
                        <div style='background: #e74c3c; color: white; padding: 20px; text-align: center;'>
                            <h1>🍕 Pizza Ordering System</h1>
                        </div>
                        <div style='padding: 20px; background: #f8f9fa;'>
                            <h2>Message Reply</h2>
                            <div style='background: white; padding: 15px; border-radius: 5px; margin: 10px 0;'>
                                {message}
                            </div>
                            <hr style='margin: 20px 0; border: 1px solid #ddd;'>
                            <p style='color: #666; font-size: 12px;'>
                                This is an automated reply from Pizza Ordering System.<br>
                                Please do not reply to this email.
                            </p>
                        </div>
                    </div>",
                TextBody = message
            };

            email.Body = bodyBuilder.ToMessageBody();

            try
            {
                using var client = new SmtpClient();
                
                // For development, we'll use a fake SMTP or log the email
                // In production, configure with real SMTP settings
                var smtpHost = _configuration["Email:SmtpHost"];
                var smtpPort = int.Parse(_configuration["Email:SmtpPort"] ?? "587");
                var username = _configuration["Email:Username"];
                var password = _configuration["Email:Password"];

                if (string.IsNullOrEmpty(smtpHost))
                {
                    // For development - just log the email instead of sending
                    Console.WriteLine($"[EMAIL SIMULATION] Would send email to: {toEmail}");
                    Console.WriteLine($"Subject: {subject}");
                    Console.WriteLine($"Message: {message}");
                    return;
                }

                await client.ConnectAsync(smtpHost, smtpPort, MailKit.Security.SecureSocketOptions.StartTls);
                await client.AuthenticateAsync(username, password);
                await client.SendAsync(email);
                await client.DisconnectAsync(true);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Failed to send email: {ex.Message}");
                // In development, we'll continue without throwing
                // In production, you might want to throw or log this properly
            }
        }

        public async Task SendReplyAsync(string toEmail, string originalMessage, string reply)
        {
            var subject = "Re: Your message to Pizza Ordering System";
            var fullMessage = $@"
                <h3>Thank you for contacting us!</h3>
                <p><strong>Your original message:</strong></p>
                <blockquote style='border-left: 3px solid #e74c3c; padding-left: 15px; margin: 10px 0; color: #666;'>
                    {originalMessage}
                </blockquote>
                <p><strong>Our reply:</strong></p>
                <div style='background: #f8f9fa; padding: 15px; border-radius: 5px;'>
                    {reply}
                </div>
                <p>Best regards,<br>Pizza Ordering Team</p>";

            await SendEmailAsync(toEmail, subject, fullMessage);
        }
    }
}