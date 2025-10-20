# 🪙 Bitcoin Predictor

A powerful Streamlit web application for Bitcoin price prediction using advanced machine learning models. This application provides comprehensive data analysis, visualization, and forecasting capabilities for Bitcoin price movements.

## 🌟 Features

- **📈 Data Upload & Management**: Upload and manage Bitcoin price datasets
- **📊 Interactive Visualizations**: Comprehensive data visualization with charts and graphs
- **🤖 Machine Learning Models**: Multiple ML algorithms for price prediction
- **🔮 Price Predictions**: Real-time Bitcoin price forecasting
- **📋 Model Comparison**: Compare different models' performance
- **📄 PDF Reports**: Generate detailed analysis reports

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or uv package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/FatnaEddaoudy/vibe-coding.git
cd vibe-coding/BitcoinPredictor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
# or if using uv:
uv sync
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## 📱 Application Pages

### 1. 📈 Data Upload
- Upload Bitcoin price datasets (CSV format)
- Data validation and preprocessing
- Historical data management

### 2. 📊 Data Visualization
- Interactive price charts
- Technical indicators
- Statistical analysis
- Trend visualization

### 3. 🤖 Model Training
- Multiple machine learning algorithms
- Feature engineering
- Model hyperparameter tuning
- Training progress monitoring

### 4. 🔮 Predictions
- Real-time price predictions
- Confidence intervals
- Prediction accuracy metrics
- Future price forecasting

### 5. 📋 Model Comparison
- Side-by-side model performance
- Accuracy metrics comparison
- Best model selection
- Performance visualization

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Machine Learning**: Scikit-learn, TensorFlow/Keras
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Plotly, Seaborn
- **APIs**: Real-time data integration

## 📊 Supported Data Formats

- CSV files with Bitcoin price data
- Required columns: Date, Open, High, Low, Close, Volume
- Automatic data validation and cleaning

## 🤖 Machine Learning Models

The application supports various ML algorithms:

- Linear Regression
- Random Forest
- Support Vector Machines (SVM)
- Neural Networks
- LSTM (Long Short-Term Memory)
- ARIMA models

## 📈 Performance Metrics

- Mean Absolute Error (MAE)
- Root Mean Square Error (RMSE)
- Mean Absolute Percentage Error (MAPE)
- R-squared Score
- Directional Accuracy

## 🔧 Configuration

The application uses configuration files for:
- Model parameters (`pyproject.toml`)
- Streamlit settings (`.streamlit/config.toml`)
- Environment variables

## 📁 Project Structure

```
BitcoinPredictor/
├── app.py                      # Main Streamlit application
├── pages/                      # Multi-page application
│   ├── 1_📈_Data_Upload.py
│   ├── 2_📊_Data_Visualization.py
│   ├── 3_🤖_Model_Training.py
│   ├── 4_🔮_Predictions.py
│   └── 5_📋_Model_Comparison.py
├── utils/                      # Utility modules
│   ├── data_preprocessing.py
│   ├── model_training.py
│   ├── visualizations.py
│   ├── api_integration.py
│   └── pdf_generator.py
├── attached_assets/            # Data and assets
└── .streamlit/                # Streamlit configuration
```

## 🚀 Deployment

The application can be deployed on various platforms:

- **Streamlit Cloud**: Direct deployment from GitHub
- **Heroku**: Using the included configuration
- **Docker**: Containerized deployment
- **Replit**: Ready-to-run environment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Bitcoin price data providers
- Streamlit community
- Machine learning libraries contributors

## 📞 Contact

For questions or support, please open an issue on GitHub or contact the project maintainer.

---

**⚠️ Disclaimer**: This application is for educational and research purposes only. Cryptocurrency trading involves significant risk, and predictions should not be used as the sole basis for financial decisions.