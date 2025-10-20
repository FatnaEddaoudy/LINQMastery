import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

def load_csv_data(uploaded_file):
    """Load and validate CSV data"""
    try:
        df = pd.read_csv(uploaded_file)
        
        # Check required columns
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Missing required columns: {missing_columns}")
            return None
        
        # Convert Date column
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Sort by date
        df = df.sort_values('Date').reset_index(drop=True)
        
        return df
    
    except Exception as e:
        st.error(f"Error loading CSV: {str(e)}")
        return None

def calculate_technical_indicators(df):
    """Calculate technical indicators for the dataset"""
    df = df.copy()
    
    # Determine maximum window size based on available data
    n_rows = len(df)
    max_window = min(50, n_rows // 3)  # Use at most 1/3 of data for rolling windows
    
    # Simple Moving Averages (adjust windows based on available data)
    df['SMA_5'] = df['Close'].rolling(window=min(5, max_window)).mean()
    df['SMA_10'] = df['Close'].rolling(window=min(10, max_window)).mean()
    df['SMA_20'] = df['Close'].rolling(window=min(20, max_window)).mean()
    if n_rows >= 50:
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
    else:
        df['SMA_50'] = df['Close'].rolling(window=max_window).mean()
    
    # Exponential Moving Averages
    df['EMA_12'] = df['Close'].ewm(span=12).mean()
    df['EMA_26'] = df['Close'].ewm(span=26).mean()
    
    # MACD
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
    df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    df['BB_Middle'] = df['Close'].rolling(window=20).mean()
    bb_std = df['Close'].rolling(window=20).std()
    df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
    df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
    df['BB_Width'] = df['BB_Upper'] - df['BB_Lower']
    df['BB_Position'] = (df['Close'] - df['BB_Lower']) / (df['BB_Upper'] - df['BB_Lower'])
    
    # Price change features
    df['Price_Change'] = df['Close'].diff()
    df['Price_Change_Pct'] = df['Close'].pct_change() * 100
    df['High_Low_Pct'] = ((df['High'] - df['Low']) / df['Close']) * 100
    df['Open_Close_Pct'] = ((df['Close'] - df['Open']) / df['Open']) * 100
    
    # Volume features
    df['Volume_SMA'] = df['Volume'].rolling(window=20).mean()
    df['Volume_Ratio'] = df['Volume'] / df['Volume_SMA']
    
    # Volatility
    df['Volatility'] = df['Close'].rolling(window=20).std()
    
    # Price position within day's range
    df['Price_Position'] = (df['Close'] - df['Low']) / (df['High'] - df['Low'])
    
    # Lag features
    for lag in [1, 2, 3, 5, 7]:
        df[f'Close_Lag_{lag}'] = df['Close'].shift(lag)
        df[f'Volume_Lag_{lag}'] = df['Volume'].shift(lag)
    
    # Rolling statistics
    for window in [5, 10, 20]:
        df[f'Close_Rolling_Mean_{window}'] = df['Close'].rolling(window=window).mean()
        df[f'Close_Rolling_Std_{window}'] = df['Close'].rolling(window=window).std()
        df[f'Volume_Rolling_Mean_{window}'] = df['Volume'].rolling(window=window).mean()
    
    return df

def preprocess_data(df):
    """Preprocess data for machine learning"""
    df = df.copy()
    
    # Calculate technical indicators
    df = calculate_technical_indicators(df)
    
    # Handle missing values
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    # Forward fill first, then backward fill for any remaining NaNs
    df[numeric_columns] = df[numeric_columns].fillna(method='ffill').fillna(method='bfill')
    
    # Remove any remaining rows with NaN values
    df = df.dropna()
    
    return df

def create_features_target(df, target_column='Close', forecast_days=1):
    """Create feature matrix and target variable for ML models"""
    # Check minimum data requirements
    if len(df) < 50:
        st.warning(f"⚠️ Warning: Only {len(df)} rows of data. Recommended minimum: 100 rows for reliable training.")
    
    # Feature columns (excluding date and target)
    feature_columns = [col for col in df.columns if col not in ['Date', target_column]]
    
    # Create features
    X = df[feature_columns].values
    
    # Create target (next day's closing price)
    y = df[target_column].shift(-forecast_days).values
    
    # Remove last rows where target is NaN
    valid_indices = ~np.isnan(y)
    X = X[valid_indices]
    y = y[valid_indices]
    
    # Final check for empty data
    if len(X) == 0:
        st.error("❌ Error: Not enough data after preprocessing. Please fetch at least 90 days of data.")
        return None, None, None
    
    if len(X) < 30:
        st.warning(f"⚠️ Warning: Only {len(X)} valid samples after preprocessing. Model accuracy may be poor. Try fetching more data (90+ days recommended).")
    
    return X, y, feature_columns

def split_data(X, y, test_size=0.2, validation_size=0.1):
    """Split data into train, validation, and test sets"""
    n_samples = len(X)
    
    # Calculate split indices
    test_start = int(n_samples * (1 - test_size))
    val_start = int(test_start * (1 - validation_size))
    
    # Split the data
    X_train = X[:val_start]
    y_train = y[:val_start]
    
    X_val = X[val_start:test_start]
    y_val = y[val_start:test_start]
    
    X_test = X[test_start:]
    y_test = y[test_start:]
    
    return X_train, X_val, X_test, y_train, y_val, y_test
