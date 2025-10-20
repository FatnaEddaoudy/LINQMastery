using LibraryData.Models;
using LibraryData.Repositories;
using LibraryServices.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.OpenApi.Models;
using Swashbuckle.AspNetCore.SwaggerGen;


var builder = WebApplication.CreateBuilder(args);

// Register services
builder.Services.AddScoped<GenreServices>();
builder.Services.AddScoped<IGenreRepository, SqlGenreRepository>();
builder.Services.AddScoped<AddressServices>();
builder.Services.AddScoped<IAddressRepository, SqlAddressRepository>();
builder.Services.AddScoped<BookServices>();
builder.Services.AddScoped<IBookRepository, SqlBookRepository>();
builder.Services.AddScoped<AuthorServices>();
builder.Services.AddScoped<IAuthorRepository, SqlAuthorRepository>();
builder.Services.AddScoped<MemberServices>();
builder.Services.AddScoped<IMemberRepository, SqlMemberRepository>();
builder.Services.AddDbContext<LibraryDBContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.ReferenceHandler = System.Text.Json.Serialization.ReferenceHandler.IgnoreCycles;
    });


builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod();
    });
});



// Add controllers
builder.Services.AddControllers();

// Add Swagger/OpenAPI services
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "Library API",
        Version = "v1"
    });
});

var app = builder.Build();
app.UseCors("AllowAll");
// Configure Swagger middleware
app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "Library API V1");
    c.RoutePrefix = string.Empty; // optional: Swagger at root URL
});

app.UseHttpsRedirection();
app.UseAuthorization();

app.MapControllers();

app.Run();
