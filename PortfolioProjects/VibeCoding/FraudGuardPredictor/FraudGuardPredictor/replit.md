# Loan Fraud Detection System

## Overview

This is a comprehensive loan fraud detection and risk assessment system built with Streamlit. The application provides end-to-end machine learning capabilities for analyzing loan data, training fraud detection models, making predictions, and monitoring model performance. It features interactive data exploration, multiple ML algorithms (Random Forest, XGBoost, Logistic Regression, Neural Networks, KNN, Decision Tree), model explainability using LIME, a simple prediction interface for instant Good/Bad loan classification, and production deployment capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## Design System

**Modern Flat Design** (Updated: October 2025)

The application uses a modern flat design aesthetic with clean, minimalist styling:

**Color Palette**:
- Primary Blue: `#2E86DE` (buttons, primary actions, chart 1)
- Success Green: `#10AC84` (success states, chart 2)
- Accent Purple: `#5F27CD` (highlights, chart 3)
- Text Dark: `#2C3E50` (main text)
- Border Light: `#E1E8ED` (card borders, dividers)
- Background: `#FFFFFF` (main background)
- Secondary Background: `#F5F7FA` (subtle backgrounds)

**Design Principles**:
- Clean borders (1px solid) instead of heavy shadows
- 8px border radius for subtle rounded corners
- Transparent chart backgrounds
- Sans-serif font family
- Ample whitespace for readability
- Card-based layouts with consistent spacing
- Section headers with left accent border

**Key UI Elements**:
- Metric cards: White background, light border, 1.5rem padding
- Charts: Branded color palette, transparent backgrounds
- Navigation cards: Clean borders, consistent typography
- Forms: Minimal styling, clear labels

## System Architecture

### Frontend Architecture
**Technology**: Streamlit multi-page application
- **Main Entry**: `app.py` serves as the application homepage
- **Page Structure**: 7 separate pages organized in `pages/` directory for distinct workflows:
  1. Data Exploration (`1_Data_Exploration.py`)
  2. Model Training (`2_Model_Training.py`)
  3. Predictions (`3_Predictions.py`) - 4 prediction modes:
     - **Simple Prediction**: Input all features, click button, get instant Good/Bad loan classification
     - **Approval Level Analysis**: Optimize approval thresholds for business metrics
     - **Individual Prediction**: Detailed loan assessment with risk levels
     - **Batch Analysis**: Process multiple loans at once
  4. Feature Selection (`4_Feature_Selection.py`)
  5. Model Explainability (`5_Model_Explainability.py`)
  6. Model Deployment (`6_Model_Deployment.py`)
  7. Performance Monitoring (`7_Performance_Monitoring.py`)

**Design Pattern**: Session state management for sharing data and trained models across pages
- Models, scalers, and feature selections stored in `st.session_state`
- Caching decorator (`@st.cache_data`) used for expensive data loading operations

**Visualization**: Dual approach using Plotly and Matplotlib/Seaborn
- Interactive charts with Plotly Express and Graph Objects
- Statistical visualizations with Seaborn

### Backend Architecture

**Core Utilities** (`utils/` directory):

1. **Data Processing** (`data_processor.py`)
   - Handles CSV data loading and preprocessing
   - Feature engineering from date columns (loan duration calculation)
   - Categorical encoding using LabelEncoder
   - Numerical imputation with scikit-learn SimpleImputer
   - StandardScaler for feature normalization

2. **Machine Learning Pipeline** (`ml_models.py`)
   - Model training with multiple algorithms:
     - Random Forest Classifier
     - XGBoost
     - Logistic Regression
     - Neural Networks (MLPClassifier)
     - K-Nearest Neighbors (KNN)
     - Decision Tree Classifier
   - Feature selection methods:
     - Recursive Feature Elimination (RFE)
     - K-Best with F-statistic
     - K-Best with Mutual Information
     - Random Forest feature importance
   - Class imbalance handling with SMOTE and RandomUnderSampler
   - Cross-validation using StratifiedKFold
   - Model persistence with pickle and JSON metadata
   - LIME integration for model explainability

3. **Visualization Components** (`visualizations.py`)
   - Reusable chart functions for:
     - Default rate analysis by region
     - Age distribution analysis
     - Payment type analysis
     - Correlation heatmaps
     - Risk segmentation
     - Trader/customer analysis

**Data Pipeline Flow**:
1. Raw CSV loaded → Preprocessing → Feature engineering
2. Train-test split → Optional class balancing → Model training
3. Feature selection (optional) → Model evaluation
4. Predictions → Explainability → Deployment

### Data Storage

**Primary Data Source**: CSV file (`attached_assets/FlaggingLoans_1760351927870.csv`)
- Loan application and performance data
- Key fields: federal_district_nm, age, gender, bad_flag (target), payment types, dates

**Model Storage**: 
- Pickle files for serialized models
- JSON files for metadata and performance metrics
- Location configurable (default: `models/` directory)

**Session State Storage**: In-memory storage for:
- Processed DataFrames
- Trained model objects
- Scalers and encoders
- Feature selection results
- Model performance metrics

### Machine Learning Architecture

**Model Training Strategy**:
- Multiple model comparison approach (Random Forest, XGBoost, Logistic Regression, Neural Network, KNN, Decision Tree)
- Configurable hyperparameters via sidebar with model selection filtering
- Evaluation metrics: AUC-ROC, precision, recall, F1-score, confusion matrix
- Cross-validation for robust performance estimation with proper preprocessing pipelines
- Automatic feature scaling for Neural Network, Logistic Regression, and KNN models
- SMOTE-based class balancing for improved minority class detection
- Proper preprocessing based on model requirements:
  - Tree-based models (Random Forest, XGBoost): Use original features with class_weight balancing
  - Distance-based models (KNN): Use StandardScaler with SMOTE-balanced data
  - Linear models (Logistic Regression): Use StandardScaler with SMOTE-balanced data
  - Neural Network: Use StandardScaler with SMOTE-balanced data
  - Decision Tree: Use SMOTE-balanced data with class_weight balancing

**Feature Engineering**:
- Automated date-based feature creation
- Categorical encoding with fallback for unknown values
- Handling of missing values through imputation

**Model Explainability**:
- LIME (Local Interpretable Model-agnostic Explanations)
- Individual prediction explanations
- Global feature importance tracking
- Support for all trained model types

**Deployment Pipeline**:
- Model serialization with complete evaluation artifacts (models, scaler, features, metrics)
- Export of standalone prediction scripts with automatic preprocessing
- Performance history tracking with JSON-based logging
- Historical trend visualization and baseline comparison
- Guided retraining workflow with checklist and best practices
- A/B testing capabilities for model comparison

### Key Architectural Decisions

1. **Multi-page Streamlit App**: Chosen for logical separation of concerns and improved user experience. Each workflow (exploration, training, prediction, etc.) has dedicated UI space.

2. **Session State for State Management**: Enables sharing of expensive computations (trained models, processed data) across pages without reloading, improving performance.

3. **Modular Utility Classes**: Separation of data processing, ML operations, and visualizations into distinct modules improves maintainability and testability.

4. **Multiple ML Algorithms**: Provides flexibility to compare different approaches and select the best performer for the specific fraud detection use case.

5. **LIME for Explainability**: Addresses the black-box nature of complex models, crucial for regulatory compliance and stakeholder trust in fraud detection.

6. **Class Imbalance Handling**: SMOTE and undersampling options address the typical class imbalance in fraud detection datasets.

7. **Caching Strategy**: Streamlit's caching decorators prevent redundant data loading and processing, critical for application responsiveness.

## External Dependencies

### Python Libraries
- **Web Framework**: Streamlit (multi-page app framework)
- **Data Manipulation**: pandas, numpy
- **Visualization**: 
  - plotly (express and graph_objects) for interactive charts
  - matplotlib and seaborn for statistical plots
- **Machine Learning**:
  - scikit-learn (models, preprocessing, metrics, feature selection)
  - xgboost (gradient boosting)
  - imbalanced-learn (SMOTE, undersampling)
- **Model Explainability**: LIME (lime-tabular)
- **Serialization**: pickle, json

### Data Dependencies
- CSV file as primary data source
- No external database required (file-based approach)
- Future database integration possible through DataProcessor class extension

### External Services
None currently integrated. The system operates as a standalone application without external API calls or cloud services.