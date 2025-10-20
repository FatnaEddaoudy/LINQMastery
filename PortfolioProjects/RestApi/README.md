# REST API Projects

## 📝 Description
Collection of RESTful API projects demonstrating modern web service development using various technologies and architectural patterns.

## 🛠️ Technologies Used
- **Backend**: C# / ASP.NET Core
- **Database**: SQL Server, Entity Framework Core
- **Authentication**: JWT, OAuth2
- **Documentation**: Swagger/OpenAPI
- **Testing**: xUnit, Postman
- **Deployment**: Docker, Azure

## 🚀 API Features
- **CRUD Operations** - Complete data management
- **Authentication & Authorization** - Secure endpoints
- **Database Integration** - Entity Framework Core
- **API Documentation** - Swagger UI
- **Error Handling** - Comprehensive error responses
- **Logging** - Request/response logging
- **Validation** - Input data validation

## 📚 Project Structure
```
RestApi/
├── UserManagementAPI/
├── ProductCatalogAPI/
├── OrderProcessingAPI/
├── SharedLibraries/
├── Tests/
└── Documentation/
```

## 🔧 API Endpoints Examples
```
GET    /api/users          # Get all users
POST   /api/users          # Create new user
GET    /api/users/{id}     # Get user by ID
PUT    /api/users/{id}     # Update user
DELETE /api/users/{id}     # Delete user
```

## 📦 Installation & Setup
```bash
# Prerequisites
- .NET 6.0 or later
- SQL Server / SQL Server Express
- Visual Studio 2022 or VS Code

# Setup
1. Clone the repository
2. Restore NuGet packages: dotnet restore
3. Update connection string in appsettings.json
4. Run migrations: dotnet ef database update
5. Start the API: dotnet run
```

## 💻 Usage
```bash
# Access Swagger documentation
https://localhost:5001/swagger

# Test endpoints
curl -X GET "https://localhost:5001/api/users"
```

## 🧪 Testing
```bash
# Run unit tests
dotnet test

# Integration testing with Postman
[Import Postman collection]
```

## 🐳 Docker Support
```dockerfile
# Build and run with Docker
docker build -t restapi .
docker run -p 5000:5000 restapi
```

## 📖 API Documentation
- Swagger UI available at `/swagger`
- Postman collections included
- Detailed endpoint documentation

## 🤝 Contributing
Instructions for contributing to the API projects.

## 📄 License
[Add license information]

---
**Part of [PortfolioProjects](../) collection**