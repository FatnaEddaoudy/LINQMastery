# Bitcoin Price Prediction Platform

## Overview

This is a comprehensive Bitcoin price prediction platform built with Streamlit that enables users to analyze historical Bitcoin data, train multiple machine learning models, and generate price forecasts. The application provides an interactive dashboard for data visualization, model training, performance comparison, and prediction generation with PDF report capabilities.

The platform supports multiple prediction models including Linear Regression, Random Forest, XGBoost, LSTM neural networks, and Facebook's Prophet. It integrates with the CoinGecko API for live Bitcoin price data and historical market information.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework**: Streamlit multipage application
- **Rationale**: Streamlit provides rapid development of data science applications with minimal frontend code, allowing focus on ML functionality rather than UI implementation
- **Structure**: Modular page-based navigation with 5 main sections:
  - Main dashboard with live price display
  - Data upload and processing
  - Interactive data visualization
  - Model training interface
  - Predictions and forecasting
  - Model performance comparison
- **State Management**: Streamlit session state for maintaining data, trained models, and predictions across page navigation
- **Pros**: Fast prototyping, automatic reactivity, built-in caching
- **Cons**: Limited customization compared to traditional web frameworks

### Backend Architecture

**Pattern**: Utility module architecture with functional decomposition
- **Rationale**: Separates concerns into specialized modules for maintainability and testability
- **Core Modules**:
  - `data_preprocessing.py`: Data loading, validation, technical indicator calculation
  - `model_training.py`: ML model training with ModelTrainer class encapsulating training logic
  - `visualizations.py`: Plotly-based interactive charts and graphs
  - `api_integration.py`: External API communication for live and historical data
  - `pdf_generator.py`: Report generation using ReportLab

**Machine Learning Pipeline**:
- Feature engineering with technical indicators (SMA, EMA, MACD, RSI, Bollinger Bands)
- Multiple model support through unified ModelTrainer interface
- Train/validation/test split for robust evaluation
- Ensemble prediction capability (mean, median, weighted average)
- **Technology Choices**:
  - scikit-learn: Traditional ML models (Linear Regression, Random Forest)
  - XGBoost: Gradient boosting for high performance
  - TensorFlow/Keras: LSTM neural networks for time series
  - Prophet: Time series forecasting with trend detection
- **Pros**: Flexibility to compare multiple approaches, ensemble reduces individual model bias
- **Cons**: Higher computational requirements, model complexity varies significantly

### Data Flow

**Data Pipeline**:
1. Data acquisition (CSV upload or API fetch)
2. Preprocessing and validation (date parsing, missing value handling)
3. Feature engineering (technical indicators calculation)
4. Train/validation/test splitting
5. Model training with cross-validation
6. Prediction generation and visualization
7. PDF report export

**State Persistence**: Session-based storage without database
- **Rationale**: Simplifies deployment and suitable for single-user analysis sessions
- **Limitations**: Data lost on session refresh, not suitable for multi-user persistence

### Visualization Strategy

**Library**: Plotly for interactive charts
- **Rationale**: Superior interactivity compared to Matplotlib, integrates seamlessly with Streamlit
- **Chart Types**:
  - Candlestick charts for OHLC data
  - Volume bar charts
  - Technical indicator overlays
  - Prediction vs actual comparison plots
  - Feature importance visualizations
  - Correlation heatmaps
  - Model performance comparisons
- **Pros**: Interactive tooltips, zoom/pan, responsive design
- **Cons**: Larger file sizes than static charts

## External Dependencies

### Third-Party APIs

**CoinGecko API** (Public cryptocurrency data)
- **Purpose**: Fetch live Bitcoin prices and historical market data
- **Integration Points**:
  - `fetch_bitcoin_price_coingecko()`: Real-time price with 24h change and volume
  - `fetch_bitcoin_historical_coingecko()`: Historical daily OHLCV data
  - `get_live_bitcoin_metrics()`: Comprehensive current market metrics
- **Rate Limiting**: Free tier with reasonable limits for development
- **Error Handling**: Timeout handling, graceful fallback on API failures

### Python Libraries

**Core Dependencies**:
- **streamlit**: Web application framework
- **pandas**: Data manipulation and time series handling
- **numpy**: Numerical computations
- **plotly**: Interactive visualizations
- **scikit-learn**: Traditional ML algorithms and preprocessing
- **xgboost**: Gradient boosting models
- **tensorflow/keras**: Deep learning (LSTM networks)
- **prophet**: Facebook's time series forecasting
- **reportlab**: PDF report generation
- **requests**: HTTP client for API integration

**Data Science Stack**:
- StandardScaler/MinMaxScaler for feature normalization
- Technical indicators computed using rolling windows and exponential moving averages
- Train/test splitting with configurable ratios
- Multiple evaluation metrics (MAE, RMSE, R²)

### Data Storage

**Current Implementation**: In-memory session state
- **Rationale**: Streamlit apps are stateless by default; session state provides temporary persistence
- **Data Stored**:
  - Raw uploaded/fetched data
  - Processed data with technical indicators
  - Trained model objects
  - Prediction results
  - Training performance metrics

**Future Considerations**: Application could be extended with:
- Database integration (PostgreSQL/MongoDB) for historical storage
- Model serialization for reusability across sessions
- User authentication for personalized dashboards

### Report Generation

**ReportLab Library**:
- **Purpose**: Generate professional PDF reports of predictions and model performance
- **Features**: Tables, charts (via matplotlib conversion), styled text, multi-page layouts
- **Output**: In-memory buffer for Streamlit download functionality