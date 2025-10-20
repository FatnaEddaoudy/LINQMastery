# 🍕 Pizza Online Ordering System

A complete full-stack pizza ordering application built with React and C# ASP.NET Core.

## 🚀 Features

### Customer Features
- **Menu Browsing**: View pizzas with real images from Unsplash
- **Shopping Cart**: Add pizzas in different sizes, manage quantities
- **Order Checkout**: Complete order form with customer details
- **Contact Form**: Send messages to restaurant with success notifications

### Admin Features
- **Pizza Management**: Create, update, delete pizzas with pricing
- **Order Management**: View all orders, update order status in real-time
- **Message Management**: Read customer messages, reply via email
- **Dashboard**: Statistics and overview of business metrics

### Technical Features
- **SQL Server Database**: Persistent data storage with Entity Framework
- **Email System**: Gmail SMTP integration for customer replies
- **Real-time Updates**: Order status changes reflect immediately
- **Responsive Design**: Works on desktop and mobile devices
- **Professional UI**: Modern design with Font Awesome icons

## 🛠️ Tech Stack

### Frontend
- **React 18** with Vite
- **React Router** for navigation
- **Axios** for API calls
- **CSS3** with Grid and Flexbox
- **Font Awesome** icons

### Backend
- **ASP.NET Core 8.0** Web API
- **Entity Framework Core** with SQL Server
- **MailKit** for email sending
- **Swagger** for API documentation
- **CORS** enabled for frontend communication

### Database
- **SQL Server LocalDB** for development
- **Entity Framework Migrations** for schema management
- **Proper relationships** between entities

## 📋 Prerequisites

- **Node.js** (v16 or higher)
- **.NET 8.0 SDK**
- **SQL Server LocalDB** (included with Visual Studio)
- **Git**

## ⚡ Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/vibe-coding/pizza-ordering-system.git
cd pizza-ordering-system
```

### 2. Database Setup
```bash
cd backend
dotnet ef database update
```

### 3. Email Configuration
```bash
# Copy and configure email settings
cp appsettings.example.json appsettings.json
# Edit appsettings.json with your Gmail credentials
```

### 4. Start Backend
```bash
cd backend
dotnet run
```
Backend will run on `http://localhost:5000`

### 5. Start Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend will run on `http://localhost:3002`

## 🔧 Configuration

### Email Setup (Gmail)
1. Enable 2-Factor Authentication in your Google Account
2. Generate an App Password: Google Account → Security → App passwords
3. Update `backend/appsettings.json`:
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

### Database Configuration
The system uses SQL Server LocalDB by default. For production:
1. Update connection string in `appsettings.json`
2. Run migrations: `dotnet ef database update`

## 🔐 Admin Access

- **URL**: `http://localhost:3002/admin`
- **Password**: `admin123`
- **Features**: Pizza management, order tracking, message replies

## 📁 Project Structure

```
pizza-ordering-system/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── admin/          # Admin panel components
│   │   ├── services/       # API service functions
│   │   └── App.jsx         # Main application
│   └── package.json
├── backend/                 # ASP.NET Core API
│   ├── Controllers/        # API controllers
│   ├── Models/            # Entity models
│   ├── Services/          # Business logic
│   ├── Migrations/        # Database migrations
│   └── Program.cs         # Application startup
├── README.md
└── EMAIL_SETUP.md
```

## 🌐 API Endpoints

### Pizzas
- `GET /api/pizzas` - Get all pizzas
- `POST /api/pizzas` - Create pizza (Admin)
- `PUT /api/pizzas/{id}` - Update pizza (Admin)
- `DELETE /api/pizzas/{id}` - Delete pizza (Admin)

### Orders
- `POST /api/orders` - Create order
- `GET /api/orders` - Get all orders (Admin)
- `PATCH /api/orders/{id}/status` - Update order status (Admin)

### Contact
- `POST /api/contact` - Submit contact message
- `GET /api/contact` - Get all messages (Admin)
- `POST /api/contact/{id}/reply` - Reply to message (Admin)
- `PATCH /api/contact/{id}/read` - Mark as read (Admin)

## 🚀 Deployment

### Development
Both servers run locally with hot reload enabled.

### Production
1. Build frontend: `npm run build`
2. Publish backend: `dotnet publish -c Release`
3. Configure production database connection
4. Set up reverse proxy (nginx/IIS)
5. Configure SSL certificates
6. Set environment variables for sensitive data

## 🔒 Security Notes

- **Never commit real passwords** to version control
- **Use environment variables** in production
- **App passwords are safer** than regular Gmail passwords
- **Admin authentication** required for management functions
- **CORS configured** for specific origins only

## 🐛 Troubleshooting

### Common Issues

**Port conflicts**: Frontend tries ports 3000, 3001, 3002 automatically
**CORS errors**: Backend must be running on port 5000
**Email not sending**: Check Gmail app password and SMTP settings
**Database errors**: Ensure SQL Server LocalDB is installed

### Development Mode
- Emails are logged to console when SMTP not configured
- Admin panel shows configuration status
- Swagger UI available at `http://localhost:5000/swagger`

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

For issues and questions, please open a GitHub issue or contact the development team.

---

**Built with ❤️ using React and ASP.NET Core**