# 💻 VibeCoding Projects Collection

A comprehensive collection of advanced coding projects showcasing machine learning, full-stack development, and data processing capabilities.

## 🏗️ Projects Overview

### 🪙 **BitcoinPredictor**
**AI-powered Bitcoin price prediction using advanced machine learning models**

- **Technologies**: Python, Streamlit, Scikit-learn, TensorFlow, Pandas, Matplotlib, Plotly
- **Features**: 
  - 📈 **Data Upload & Management**: Upload and manage Bitcoin price datasets with validation
  - 📊 **Interactive Visualizations**: Comprehensive charts, technical indicators, and statistical analysis
  - 🤖 **Multiple ML Models**: Linear Regression, Random Forest, SVM, Neural Networks, LSTM
  - 🔮 **Real-time Predictions**: Price forecasting with confidence intervals and accuracy metrics
  - 📋 **Model Comparison**: Side-by-side performance analysis and best model selection
  - 📄 **PDF Reports**: Generate detailed analysis reports
- **Performance Metrics**: MAE, RMSE, MAPE, R-squared Score, Directional Accuracy
- **Deployment**: Streamlit Cloud, Heroku, Docker ready

### 🍕 **Pizza Ordering System**
**Complete full-stack e-commerce solution for pizza ordering**

- **Technologies**: React 18, C# ASP.NET Core 8.0, SQL Server, Entity Framework, MailKit
- **Architecture**: RESTful API, Entity Framework migrations, responsive design
- **Customer Features**:
  - 🍕 **Menu Browsing**: View pizzas with real images from Unsplash
  - 🛒 **Shopping Cart**: Add pizzas in different sizes, manage quantities
  - 📝 **Order Checkout**: Complete order form with customer details
  - 📧 **Contact Form**: Send messages with success notifications
- **Admin Features**:
  - 🎛️ **Pizza Management**: Create, update, delete pizzas with pricing
  - 📋 **Order Management**: View all orders, update status in real-time
  - 💬 **Message Management**: Read customer messages, reply via email
  - 📊 **Dashboard**: Business statistics and metrics overview
- **Technical Features**: Gmail SMTP integration, real-time updates, SQL Server database

### 📄 **FileTransform**
**Document processing system for multiple file formats**

- **Technologies**: TypeScript, Node.js, Express, Vite
- **Purpose**: Business automation tool for document transformation
- **Features**:
  - 📁 **Multi-format Support**: EDIFACT, PDF, TXT, Word (.doc, .docx) to Excel CSV conversion
  - ⚡ **Batch Processing**: Handle multiple files simultaneously
  - 🔄 **Output Options**: Separate files or combined into single Excel
  - 🌐 **Modern Web Interface**: Built with Vite for hot-reloading and optimal development experience
  - 🚀 **Development-friendly**: `npm run dev` with tsx for instant updates

## 🚀 Quick Start Guide

### BitcoinPredictor
```bash
cd BitcoinPredictor
pip install -r requirements.txt
streamlit run app.py
# Access at http://localhost:8501
```

### Pizza Ordering System
```bash
# Backend
cd pizza-ordering-system/backend
dotnet ef database update
cp appsettings.example.json appsettings.json
# Configure email settings in appsettings.json
dotnet run
# Backend runs on http://localhost:5000

# Frontend
cd ../frontend
npm install
npm run dev
# Frontend runs on http://localhost:3002
# Admin access: /admin with password "admin123"
```

### FileTransform
```bash
cd FileTransform
npm install
npm run dev
# Access at configured port with hot-reloading
```

## 🛠️ Technology Stack Summary

| Technology | Projects | Purpose |
|------------|----------|---------|
| **Python** | BitcoinPredictor | ML model development, data analysis |
| **Streamlit** | BitcoinPredictor | Interactive ML application deployment |
| **React 18** | Pizza System | Modern frontend framework |
| **C# ASP.NET Core** | Pizza System | Backend API development |
| **TypeScript** | FileTransform | Type-safe JavaScript development |
| **Node.js/Express** | FileTransform | Server-side processing |
| **SQL Server** | Pizza System | Database management |
| **Entity Framework** | Pizza System | ORM and migrations |

## 📊 Key Features & Achievements

### Machine Learning Excellence
- **Multi-algorithm approach**: Implemented and compared 6+ ML algorithms
- **Complete ML pipeline**: From data preprocessing to model deployment
- **Interactive visualization**: Real-time charts and performance metrics
- **Production-ready**: Streamlit deployment with PDF report generation

### Full-Stack Development
- **Modern architecture**: React frontend with ASP.NET Core backend
- **Real-time features**: Live order tracking and status updates
- **Email integration**: Automated customer notifications and admin replies
- **Admin dashboard**: Complete business management interface

### Data Processing Innovation
- **Multi-format support**: Handle diverse document types seamlessly
- **Batch operations**: Efficient processing of multiple files
- **Business automation**: Practical tool for document workflow optimization
- **Modern development**: TypeScript with hot-reloading for optimal DX

---

**Part of the [Portfolio Projects Collection](../../../)**

*Showcasing expertise in Machine Learning, Full-Stack Development, and Data Processing*