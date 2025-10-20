# Email Configuration Guide

## Current Status
🔄 **Development Mode**: Emails are simulated and logged to console
📧 **Production Mode**: Requires Gmail SMTP configuration

## To Enable Real Email Sending to Gmail:

### Step 1: Get Gmail App Password
1. Go to your Google Account settings
2. Enable 2-Factor Authentication if not already enabled
3. Go to Security → 2-Step Verification → App passwords
4. Generate an app password for "Mail"
5. Copy the 16-character app password

### Step 2: Update Configuration
Edit `backend/appsettings.json`:

```json
{
  "Email": {
    "FromEmail": "your-email@gmail.com",
    "SmtpHost": "smtp.gmail.com",
    "SmtpPort": "587",
    "Username": "your-email@gmail.com",
    "Password": "your-16-char-app-password"
  }
}
```

### Step 3: Restart Backend
```bash
cd backend
dotnet run
```

## Security Notes
- Never commit real passwords to version control
- Use environment variables in production
- App passwords are safer than regular passwords

## Test the Email
1. Go to Admin Panel → Messages
2. Click Reply on any message
3. Send a reply
4. Check the recipient's Gmail inbox