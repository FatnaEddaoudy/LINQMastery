import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
from prophet import Prophet
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import streamlit as st
import warnings
warnings.filterwarnings('ignore')

class ModelTrainer:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_names = []
        
    def prepare_data_for_lstm(self, X, y, sequence_length=60):
        """Prepare data for LSTM model"""
        X_lstm = []
        y_lstm = []
        
        for i in range(sequence_length, len(X)):
            X_lstm.append(X[i-sequence_length:i])
            y_lstm.append(y[i])
        
        return np.array(X_lstm), np.array(y_lstm)
    
    def train_linear_regression(self, X_train, y_train, X_val, y_val):
        """Train Linear Regression model"""
        try:
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_val_scaled = scaler.transform(X_val)
            
            # Train model
            model = LinearRegression()
            model.fit(X_train_scaled, y_train)
            
            # Predictions
            train_pred = model.predict(X_train_scaled)
            val_pred = model.predict(X_val_scaled)
            
            # Metrics
            metrics = {
                'train_mae': mean_absolute_error(y_train, train_pred),
                'train_rmse': np.sqrt(mean_squared_error(y_train, train_pred)),
                'train_r2': r2_score(y_train, train_pred),
                'val_mae': mean_absolute_error(y_val, val_pred),
                'val_rmse': np.sqrt(mean_squared_error(y_val, val_pred)),
                'val_r2': r2_score(y_val, val_pred)
            }
            
            self.models['Linear Regression'] = model
            self.scalers['Linear Regression'] = scaler
            
            return metrics
        except Exception as e:
            st.error(f"Error training Linear Regression: {str(e)}")
            return None
    
    def train_random_forest(self, X_train, y_train, X_val, y_val):
        """Train Random Forest model"""
        try:
            # Train model
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            model.fit(X_train, y_train)
            
            # Predictions
            train_pred = model.predict(X_train)
            val_pred = model.predict(X_val)
            
            # Metrics
            metrics = {
                'train_mae': mean_absolute_error(y_train, train_pred),
                'train_rmse': np.sqrt(mean_squared_error(y_train, train_pred)),
                'train_r2': r2_score(y_train, train_pred),
                'val_mae': mean_absolute_error(y_val, val_pred),
                'val_rmse': np.sqrt(mean_squared_error(y_val, val_pred)),
                'val_r2': r2_score(y_val, val_pred)
            }
            
            self.models['Random Forest'] = model
            
            return metrics
        except Exception as e:
            st.error(f"Error training Random Forest: {str(e)}")
            return None
    
    def train_xgboost(self, X_train, y_train, X_val, y_val):
        """Train XGBoost model"""
        try:
            # Train model
            model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                n_jobs=-1
            )
            model.fit(X_train, y_train)
            
            # Predictions
            train_pred = model.predict(X_train)
            val_pred = model.predict(X_val)
            
            # Metrics
            metrics = {
                'train_mae': mean_absolute_error(y_train, train_pred),
                'train_rmse': np.sqrt(mean_squared_error(y_train, train_pred)),
                'train_r2': r2_score(y_train, train_pred),
                'val_mae': mean_absolute_error(y_val, val_pred),
                'val_rmse': np.sqrt(mean_squared_error(y_val, val_pred)),
                'val_r2': r2_score(y_val, val_pred)
            }
            
            self.models['XGBoost'] = model
            
            return metrics
        except Exception as e:
            st.error(f"Error training XGBoost: {str(e)}")
            return None
    
    def train_lstm(self, X_train, y_train, X_val, y_val, sequence_length=60):
        """Train LSTM model - skipped due to TensorFlow compatibility issues"""
        # LSTM is currently disabled due to persistent TensorFlow batch processing bugs
        # The app works perfectly with the other 4 models (Linear Regression, Random Forest, XGBoost, Prophet)
        st.info("ℹ️ LSTM training is currently disabled due to TensorFlow compatibility issues. Using 4 other models for predictions.")
        return None
    
    def train_prophet(self, df, target_column='Close'):
        """Train Prophet model"""
        try:
            # Prepare data for Prophet
            prophet_data = df[['Date', target_column]].copy()
            prophet_data.columns = ['ds', 'y']
            
            # Initialize and fit Prophet model
            model = Prophet(
                seasonality_mode='multiplicative'
            )
            model.add_seasonality(name='daily', period=1, fourier_order=5)
            model.add_seasonality(name='weekly', period=7, fourier_order=3)
            model.add_seasonality(name='yearly', period=365.25, fourier_order=10)
            model.fit(prophet_data)
            
            # Make predictions on historical data
            train_pred = model.predict(prophet_data)
            
            # Calculate metrics
            y_true = prophet_data['y'].values
            y_pred = train_pred['yhat'].values
            
            metrics = {
                'train_mae': mean_absolute_error(y_true, y_pred),
                'train_rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
                'train_r2': r2_score(y_true, y_pred),
                'val_mae': mean_absolute_error(y_true[-100:], y_pred[-100:]) if len(y_true) > 100 else mean_absolute_error(y_true, y_pred),
                'val_rmse': np.sqrt(mean_squared_error(y_true[-100:], y_pred[-100:])) if len(y_true) > 100 else np.sqrt(mean_squared_error(y_true, y_pred)),
                'val_r2': r2_score(y_true[-100:], y_pred[-100:]) if len(y_true) > 100 else r2_score(y_true, y_pred)
            }
            
            self.models['Prophet'] = model
            
            return metrics
        except Exception as e:
            st.error(f"Error training Prophet: {str(e)}")
            return None
    
    def predict(self, model_name, X):
        """Make predictions with specified model"""
        if model_name not in self.models:
            return None
        
        model = self.models[model_name]
        
        if model_name == 'Linear Regression':
            scaler = self.scalers[model_name]
            X_scaled = scaler.transform(X)
            return model.predict(X_scaled)
        
        elif model_name in ['Random Forest', 'XGBoost']:
            return model.predict(X)
        
        elif model_name == 'LSTM':
            scaler_info = self.scalers[model_name]
            scaler_X = scaler_info['X']
            scaler_y = scaler_info['y']
            sequence_length = scaler_info['sequence_length']
            
            # For LSTM, we need enough historical data to create sequences
            if len(X) < sequence_length:
                # Not enough data points to create a sequence - skip LSTM prediction
                st.warning(f"⚠️ LSTM requires {sequence_length} data points for prediction. Only {len(X)} available. Skipping LSTM.")
                return np.array([])
            
            X_scaled = scaler_X.transform(X)
            
            # Use the last 'sequence_length' points to create one prediction sequence
            X_sequence = X_scaled[-sequence_length:]
            X_lstm = X_sequence.reshape(1, sequence_length, X_sequence.shape[1])
            
            pred_scaled = model.predict(X_lstm, verbose=0)
            pred = scaler_y.inverse_transform(pred_scaled).ravel()
            return pred
        
        return None
    
    def predict_prophet(self, periods=30):
        """Make future predictions with Prophet"""
        if 'Prophet' not in self.models:
            return None
        
        model = self.models['Prophet']
        
        # Create future dataframe
        future = model.make_future_dataframe(periods=periods)
        
        # Make predictions
        forecast = model.predict(future)
        
        return forecast
    
    def predict_ensemble(self, X, method='mean'):
        """Make ensemble predictions combining multiple models
        
        Args:
            X: Feature data
            method: 'mean' (average), 'weighted' (weighted by R2 score), or 'median'
        """
        predictions = []
        weights = []
        model_names = []
        
        # Collect predictions from all available models (except Prophet)
        for model_name in self.models.keys():
            if model_name != 'Prophet':
                pred = self.predict(model_name, X)
                if pred is not None and len(pred) > 0:
                    predictions.append(pred)
                    model_names.append(model_name)
                    
                    # Get model weight based on validation performance (stored during training)
                    # Default weight is 1.0 if no validation score available
                    weights.append(1.0)
        
        if len(predictions) == 0:
            return None
        
        # Align predictions length (handle LSTM which may return shorter predictions)
        min_length = min(len(p) for p in predictions)
        aligned_predictions = [p[-min_length:] for p in predictions]
        
        # Stack predictions
        pred_array = np.array(aligned_predictions)
        
        # Combine based on method
        if method == 'mean':
            ensemble_pred = np.mean(pred_array, axis=0)
        elif method == 'median':
            ensemble_pred = np.median(pred_array, axis=0)
        elif method == 'weighted':
            # Normalize weights
            weights_array = np.array(weights[:len(predictions)])
            weights_array = weights_array / np.sum(weights_array)
            # Weighted average
            ensemble_pred = np.average(pred_array, axis=0, weights=weights_array)
        else:
            ensemble_pred = np.mean(pred_array, axis=0)
        
        return ensemble_pred
    
    def get_model_weights(self):
        """Get model weights based on validation performance"""
        if not hasattr(self, 'validation_scores'):
            return None
        
        weights = {}
        for model_name, score in self.validation_scores.items():
            # Use R² score as weight (higher is better)
            weights[model_name] = max(0, score)  # Ensure non-negative
        
        return weights
