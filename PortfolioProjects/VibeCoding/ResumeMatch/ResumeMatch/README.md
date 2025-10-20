# 🎯 CV Matcher - AI-Powered HR Candidate Matching System

An intelligent HR application that uses Machine Learning and Natural Language Processing to match job descriptions with candidate CVs, providing ranked results with detailed skill comparisons.

![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat&logo=node.js&logoColor=white)

## ✨ Key Features

### 🤖 AI-Powered Analysis
- **TF-IDF Vectorization**: Uses scikit-learn for intelligent text similarity matching
- **spaCy NLP**: Advanced natural language processing for contextual understanding
- **Cosine Similarity**: Calculates precise match scores between CVs and job requirements

### 📄 Smart Document Processing
- **Multi-format Support**: Handles PDF and Word documents (DOCX, DOC)
- **Bulk Upload**: Process multiple CVs simultaneously via drag-and-drop interface
- **Automatic Extraction**: Intelligent parsing of candidate names, skills, experience, and education

### 🎨 Modern User Interface
- **Dark/Light Theme**: Full theme support with smooth transitions
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Real-time Progress**: Live feedback during CV processing
- **Interactive Results**: Grid and table view modes for candidate comparison

### 🔍 Advanced Skills Matching
- **Multi-word Technical Skills**: Recognizes compound terms like ".NET Core", "ASP.NET Core", "SQL Server"
- **Contextual Extraction**: Identifies skills near relevant phrases ("experience with", "proficient in")
- **Stop Words Filtering**: Removes Dutch words and programming keywords for cleaner results
- **Comprehensive Database**: Covers programming languages, frameworks, databases, cloud platforms, DevOps tools

## 🛠️ Technical Stack

### Frontend
- **React** with **TypeScript** for type-safe development
- **Tailwind CSS** + **Shadcn UI** for modern, accessible components
- **TanStack Query** for efficient data fetching and caching
- **Wouter** for lightweight routing
- **Vite** for fast development and optimized builds

### Backend
- **Express.js** for REST API
- **Multer** for secure file upload handling
- **Python ML Service** for CV analysis
- **In-memory storage** with extensible interface

### ML/NLP
- **spaCy** (en_core_web_sm) for advanced NLP
- **scikit-learn** for TF-IDF vectorization and similarity
- **PyPDF2** for PDF text extraction
- **python-docx** for Word document processing
- **NumPy** for numerical operations

## 🚀 How It Works

1. **Upload CVs**: Drag and drop multiple PDF or Word files
2. **Enter Job Description**: Describe the role requirements and skills needed
3. **AI Analysis**: ML algorithms process and compare documents
4. **Get Results**: View ranked candidates with match scores (0-100%)
5. **Compare Details**: Side-by-side comparison of skills, experience, and education

## 📊 Matching Algorithm

```
1. Text Extraction: Parse CVs and job description
2. Skills Detection: NLP-based contextual skill extraction
3. TF-IDF Vectorization: Convert text to numerical vectors
4. Cosine Similarity: Calculate match percentage
5. Ranking: Sort candidates by relevance score
```

## 🔒 Security Features

- Command injection prevention using `execFile` with argument arrays
- File type validation (PDF, DOC, DOCX only)
- File size limits (10MB per file)
- Temporary file cleanup in all code paths
- Input validation for job descriptions and uploads

## 💼 Use Cases

- **HR Departments**: Quickly screen large volumes of applicants
- **Recruiters**: Match candidates to job requirements efficiently
- **Hiring Managers**: Get data-driven insights on candidate fit
- **Job Seekers**: Understand how well their CV matches job descriptions

## 🎯 Project Highlights

- **Real-world Application**: Solves actual HR screening challenges
- **Full-stack Architecture**: Demonstrates end-to-end development skills
- **ML Integration**: Practical application of machine learning
- **Modern Tech Stack**: Uses current industry-standard tools
- **Clean Code**: Well-structured, maintainable codebase
- **Type Safety**: Full TypeScript implementation on frontend

## 📝 Future Enhancements

- [ ] Export results to PDF/Excel
- [ ] Save job postings and candidate pools
- [ ] Email integration for candidate outreach
- [ ] Advanced filters (location, salary, availability)
- [ ] Multi-language support for international CVs
- [ ] ATS (Applicant Tracking System) integration

## 🏗️ Project Structure

```
├── cv_matcher.py           # Python ML service
├── server/
│   ├── routes.ts          # API endpoints
│   └── storage.ts         # Data persistence
├── client/
│   ├── src/
│   │   ├── components/    # React components
│   │   └── pages/         # Application pages
│   └── index.css          # Theme configuration
└── shared/
    └── schema.ts          # TypeScript types
```

## 👨‍💻 Developer

**Fatna Eddaoudy**
- GitHub: [@FatnaEddaoudy](https://github.com/FatnaEddaoudy)

## 📄 License

This project is available for portfolio purposes.

---

⭐ **Star this repo** if you find it useful for your HR or recruitment needs!
