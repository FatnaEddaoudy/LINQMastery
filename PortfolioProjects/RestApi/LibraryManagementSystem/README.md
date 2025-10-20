# REST API Applications Repository

This repository contains various REST API applications built with modern web technologies and architectural patterns. Each project demonstrates different aspects of API development, from basic CRUD operations to complex business logic implementation.

## 📚 Current Projects

### Library Management System REST API

A comprehensive Library Management System built using **ASP.NET Core** with a clean **3-Layer Architecture** pattern. This REST API provides complete functionality for managing books, authors, genres, members, and borrowing operations in a library system.

## 🏗️ Architecture Overview

This application follows a **3-Layer Architecture** pattern that promotes separation of concerns, maintainability, and scalability:

```
┌─────────────────────────────────────────────┐
│             Presentation Layer              │
│                (LibraryApi)                 │
│   Controllers + API Endpoints + Swagger     │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│              Business Layer                 │
│             (LibraryServices)               │
│     Business Logic + Validation Rules       │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│               Data Layer                    │
│              (LibraryData)                  │
│   Models + DbContext + Repositories + EF    │
└─────────────────────────────────────────────┘
```

### Layer Details

#### 1. **Presentation Layer (LibraryApi)**
- **Purpose**: Handles HTTP requests/responses and API endpoints
- **Components**:
  - Controllers (BookController, AuthorController, GenreController, etc.)
  - API routing and HTTP method handling
  - Swagger/OpenAPI documentation
  - CORS configuration
  - Dependency injection setup

#### 2. **Business Layer (LibraryServices)**
- **Purpose**: Contains business logic and validation rules
- **Components**:
  - Service classes (BookServices, AuthorServices, etc.)
  - Business rule implementation
  - Data validation and processing
  - Acts as intermediary between controllers and repositories

#### 3. **Data Layer (LibraryData)**
- **Purpose**: Handles data access and database operations
- **Components**:
  - Entity models (Book, Author, Genre, Member, etc.)
  - DbContext for Entity Framework Core
  - Repository interfaces and implementations
  - Database migrations
  - SQL Server integration

## 📚 Features

- **Book Management**: Add, update, delete, and retrieve books with author and genre information
- **Author Management**: Manage author information and their published books
- **Genre Management**: Categorize books by genres
- **Member Management**: Handle library member registration and information
- **Address Management**: Store and manage member addresses
- **Database Integration**: Full SQL Server integration with Entity Framework Core
- **API Documentation**: Built-in Swagger/OpenAPI documentation
- **CORS Support**: Cross-origin resource sharing enabled

## 🛠️ Technology Stack

- **Framework**: ASP.NET Core (.NET 9.0)
- **Database**: SQL Server
- **ORM**: Entity Framework Core
- **Documentation**: Swagger/OpenAPI
- **Architecture**: 3-Layer Architecture
- **Design Patterns**: Repository Pattern, Dependency Injection

## 📋 Database Schema

### Core Entities

- **Books**: BookID, Title, PhotoUrl, AuthorId, GenreId, PublishedYear, ISBN, Pages, CopierAvailable
- **Authors**: AuthorID, Name, Biography, BirthDate
- **Genres**: GenreID, Name, Description
- **Members**: MemberID, Name, Email, Phone, AddressId
- **Addresses**: AddressID, Street, City, PostalCode, Country
- **Borrowings**: Relationship between books and members
- **Users & Roles**: User management system

## 🚀 Getting Started

### Prerequisites

- .NET 9.0 SDK
- SQL Server (LocalDB or full version)
- Visual Studio 2022 or VS Code

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/FatnaEddaoudy/RestApi.git
   cd LibraryManagementSystem
   ```

2. **Update Connection String**
   
   Edit `appsettings.json` in the LibraryApi project:
   ```json
   {
     "ConnectionStrings": {
       "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=LibraryDB;Trusted_Connection=true;MultipleActiveResultSets=true"
     }
   }
   ```

3. **Restore Dependencies**
   ```bash
   dotnet restore
   ```

4. **Apply Database Migrations**
   ```bash
   dotnet ef database update --project LibraryData --startup-project LibraryApi
   ```

5. **Run the Application**
   ```bash
   dotnet run --project LibraryApi
   ```

6. **Access Swagger Documentation**
   
   Navigate to: `https://localhost:5001` or `http://localhost:5000`

## 📖 API Endpoints

### Books
- `GET /api/book` - Get all books
- `GET /api/book/{id}` - Get book by ID
- `POST /api/book` - Create new book
- `PUT /api/book/{id}` - Update book
- `DELETE /api/book/{id}` - Delete book

### Authors
- `GET /api/author` - Get all authors
- `GET /api/author/{id}` - Get author by ID
- `POST /api/author` - Create new author
- `PUT /api/author/{id}` - Update author
- `DELETE /api/author/{id}` - Delete author

### Genres
- `GET /api/genre` - Get all genres
- `GET /api/genre/{id}` - Get genre by ID
- `POST /api/genre` - Create new genre
- `PUT /api/genre/{id}` - Update genre
- `DELETE /api/genre/{id}` - Delete genre

### Members
- `GET /api/member` - Get all members
- `GET /api/member/{id}` - Get member by ID
- `POST /api/member` - Create new member
- `PUT /api/member/{id}` - Update member
- `DELETE /api/member/{id}` - Delete member

### Addresses
- `GET /api/address` - Get all addresses
- `GET /api/address/{id}` - Get address by ID
- `POST /api/address` - Create new address
- `PUT /api/address/{id}` - Update address
- `DELETE /api/address/{id}` - Delete address

## 🏛️ Project Structure

```
LibraryManagementSystem/
├── LibraryApi/                          # Presentation Layer
│   ├── Controllers/                     # API Controllers
│   │   ├── BookController.cs
│   │   ├── AuthorController.cs
│   │   ├── GenreController.cs
│   │   ├── MemberController.cs
│   │   └── AddressController.cs
│   ├── Program.cs                       # Application startup
│   ├── appsettings.json                 # Configuration
│   └── LibraryApi.csproj
├── LibraryServices/                     # Business Layer
│   └── Services/                        # Business Logic
│       ├── BookServices.cs
│       ├── AuthorServices.cs
│       ├── GenreServices.cs
│       ├── MemberServices.cs
│       └── AddressServices.cs
├── LibraryData/                         # Data Layer
│   ├── Models/                          # Entity Models
│   │   ├── Book.cs
│   │   ├── Author.cs
│   │   ├── Genre.cs
│   │   ├── Member.cs
│   │   ├── Address.cs
│   │   ├── Borrowing.cs
│   │   ├── User.cs
│   │   ├── Role.cs
│   │   ├── UserRole.cs
│   │   └── LibraryDBContext.cs          # EF DbContext
│   ├── Repositories/                    # Repository Pattern
│   │   ├── IBookRepository.cs
│   │   ├── SqlBookRepository.cs
│   │   └── ... (other repositories)
│   └── Migrations/                      # EF Migrations
└── LibraryManagementSystem.sln          # Solution file
```

## 🎯 Benefits of 3-Layer Architecture

### 🔄 **Separation of Concerns**
Each layer has a specific responsibility, making the code more organized and maintainable.

### 🧪 **Testability**
Layers can be tested independently, improving code quality and reliability.

### 🔧 **Maintainability**
Changes in one layer don't directly affect others, making maintenance easier.

### 📈 **Scalability**
Easy to scale individual layers based on requirements.

### 🔄 **Reusability**
Business logic can be reused across different presentation layers.

### 🛡️ **Security**
Data access is centralized and controlled through the repository pattern.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🚀 Repository Overview

This **RestApi** repository serves as a collection of REST API applications, showcasing:

- **Modern Web Technologies**: ASP.NET Core, Entity Framework Core, SQL Server
- **Architectural Patterns**: 3-Layer Architecture, Repository Pattern, Dependency Injection
- **Best Practices**: Clean Code, SOLID Principles, API Documentation
- **Real-world Applications**: Complete business logic implementations

### 🎯 Repository Goals

- Demonstrate various REST API development approaches
- Showcase different architectural patterns and design principles
- Provide learning resources for API development
- Store reusable code templates and patterns

### 📋 Future Projects

This repository will continue to grow with additional REST API projects covering:
- Microservices architecture
- Authentication and authorization systems
- E-commerce APIs
- Social media APIs
- And more...

## 📧 Contact

**Fatna Eddaoudy** - [GitHub Profile](https://github.com/FatnaEddaoudy)

Repository Link: [https://github.com/FatnaEddaoudy/RestApi](https://github.com/FatnaEddaoudy/RestApi)

---

*A collection of REST API applications built with ❤️ and modern development practices*