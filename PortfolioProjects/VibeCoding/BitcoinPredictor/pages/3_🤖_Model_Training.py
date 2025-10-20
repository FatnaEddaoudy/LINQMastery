import streamlit as st
import pandas as pd
import numpy as np
from utils.model_training import ModelTrainer
from utils.data_preprocessing import create_features_target, split_data
from utils.visualizations import create_feature_importance_chart, create_residuals_plot
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import plotly.express as px
import time

st.set_page_config(page_title="Model Training", page_icon="🤖", layout="wide")

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'models' not in st.session_state:
    st.session_state.models = {}
if 'predictions' not in st.session_state:
    st.session_state.predictions = {}

st.title("🤖 Machine Learning Model Training")

if st.session_state.processed_data is None:
    st.warning("⚠️ No processed data available. Please upload and process data first!")
    st.stop()

# Initialize model trainer
if 'model_trainer' not in st.session_state:
    st.session_state.model_trainer = ModelTrainer()

# Model selection
st.sidebar.header("Model Configuration")

available_models = {
    'Linear Regression': '📈 Fast, interpretable linear model',
    'Random Forest': '🌳 Ensemble method, handles non-linearity',
    'XGBoost': '🚀 Gradient boosting, high performance',
    'LSTM': '🧠 Neural network for time series',
    'Prophet': '📊 Facebook\'s time series forecasting'
}

selected_models = st.sidebar.multiselect(
    "Select Models to Train",
    options=list(available_models.keys()),
    default=list(available_models.keys()),
    format_func=lambda x: f"{x}: {available_models[x]}"
)

# Training parameters
st.sidebar.subheader("Training Parameters")
test_size = st.sidebar.slider("Test Set Size", 0.1, 0.4, 0.2, 0.05)
val_size = st.sidebar.slider("Validation Set Size", 0.05, 0.2, 0.1, 0.05)
forecast_days = st.sidebar.selectbox("Forecast Horizon (days)", [1, 3, 7, 14, 30], index=0)

# Data preparation
st.markdown("## 📊 Data Preparation")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", len(st.session_state.processed_data))

with col2:
    st.metric("Features Available", len(st.session_state.processed_data.columns) - 2)  # Exclude Date and Close

with col3:
    st.metric("Forecast Horizon", f"{forecast_days} day(s)")

# Prepare features and target
with st.spinner("Preparing features and target variable..."):
    try:
        X, y, feature_names = create_features_target(
            st.session_state.processed_data, 
            target_column='Close', 
            forecast_days=forecast_days
        )
        
        # Check if data preparation failed
        if X is None or y is None or feature_names is None:
            st.error("❌ Data preparation failed due to insufficient data.")
            st.info("💡 **Solution**: Go to Data Upload and fetch at least **90 days** of data (180-365 days recommended).")
            st.stop()
        
        # Split data
        X_train, X_val, X_test, y_train, y_val, y_test = split_data(
            X, y, test_size=test_size, validation_size=val_size
        )
        
        st.session_state.model_trainer.feature_names = feature_names
        
        st.success("✅ Data preparation completed!")
        
        # Show data split information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Training Set", f"{len(X_train)} samples")
        
        with col2:
            st.metric("Validation Set", f"{len(X_val)} samples")
        
        with col3:
            st.metric("Test Set", f"{len(X_test)} samples")
            
    except Exception as e:
        st.error(f"Error preparing data: {str(e)}")
        st.info("💡 Try fetching more data (90+ days recommended) from the Data Upload page.")
        st.stop()

# Model training section
st.markdown("## 🚀 Model Training")

if st.button("🎯 Train Selected Models", type="primary"):
    results = {}
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_models = len(selected_models)
    
    for idx, model_name in enumerate(selected_models):
        status_text.text(f"Training {model_name}...")
        
        try:
            if model_name == 'Linear Regression':
                metrics = st.session_state.model_trainer.train_linear_regression(
                    X_train, y_train, X_val, y_val
                )
                
            elif model_name == 'Random Forest':
                metrics = st.session_state.model_trainer.train_random_forest(
                    X_train, y_train, X_val, y_val
                )
                
            elif model_name == 'XGBoost':
                metrics = st.session_state.model_trainer.train_xgboost(
                    X_train, y_train, X_val, y_val
                )
                
            elif model_name == 'LSTM':
                metrics = st.session_state.model_trainer.train_lstm(
                    X_train, y_train, X_val, y_val
                )
                if metrics is None:
                    # LSTM was skipped due to insufficient data
                    continue
                
            elif model_name == 'Prophet':
                metrics = st.session_state.model_trainer.train_prophet(
                    st.session_state.processed_data, target_column='Close'
                )
            
            if metrics:
                results[model_name] = metrics
                st.success(f"✅ {model_name} trained successfully!")
            else:
                st.error(f"❌ Failed to train {model_name}")
                
        except Exception as e:
            st.error(f"❌ Error training {model_name}: {str(e)}")
        
        progress_bar.progress((idx + 1) / total_models)
    
    status_text.text("Training completed!")
    
    # Store results in session state
    st.session_state.training_results = results
    st.session_state.test_data = (X_test, y_test)

# Display training results
if hasattr(st.session_state, 'training_results'):
    st.markdown("## 📊 Training Results")
    
    # Create results dataframe
    results_data = []
    for model_name, metrics in st.session_state.training_results.items():
        results_data.append({
            'Model': model_name,
            'Train MAE': metrics['train_mae'],
            'Train RMSE': metrics['train_rmse'],
            'Train R²': metrics['train_r2'],
            'Val MAE': metrics['val_mae'],
            'Val RMSE': metrics['val_rmse'],
            'Val R²': metrics['val_r2']
        })
    
    results_df = pd.DataFrame(results_data)
    
    # Display results table
    st.dataframe(results_df.round(4))
    
    # Performance comparison
    st.markdown("### 📈 Model Performance Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Validation MAE comparison
        fig_mae = px.bar(
            results_df, 
            x='Model', 
            y='Val MAE',
            title='Validation Mean Absolute Error',
            color='Val MAE',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_mae, use_container_width=True)
    
    with col2:
        # Validation R² comparison
        fig_r2 = px.bar(
            results_df, 
            x='Model', 
            y='Val R²',
            title='Validation R² Score',
            color='Val R²',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_r2, use_container_width=True)
    
    # Feature importance for tree-based models
    st.markdown("### 🔍 Feature Importance Analysis")
    
    for model_name in ['Random Forest', 'XGBoost']:
        if model_name in st.session_state.model_trainer.models:
            model = st.session_state.model_trainer.models[model_name]
            
            importance_chart = create_feature_importance_chart(
                model, 
                st.session_state.model_trainer.feature_names, 
                model_name
            )
            
            if importance_chart:
                st.plotly_chart(importance_chart, use_container_width=True)
    
    # Test set evaluation
    if hasattr(st.session_state, 'test_data'):
        st.markdown("### 🎯 Test Set Evaluation")
        
        X_test, y_test = st.session_state.test_data
        test_results = []
        
        for model_name in st.session_state.training_results.keys():
            if model_name != 'Prophet':  # Prophet handles differently
                try:
                    y_pred = st.session_state.model_trainer.predict(model_name, X_test)
                    
                    if y_pred is not None and len(y_pred) > 0:
                        # Align predictions with actual values for LSTM
                        if model_name == 'LSTM' and len(y_pred) != len(y_test):
                            y_test_aligned = y_test[-len(y_pred):]
                        else:
                            y_test_aligned = y_test
                            
                        if len(y_pred) == len(y_test_aligned):
                            test_mae = mean_absolute_error(y_test_aligned, y_pred)
                            test_rmse = np.sqrt(mean_squared_error(y_test_aligned, y_pred))
                            test_r2 = r2_score(y_test_aligned, y_pred)
                            
                            test_results.append({
                                'Model': model_name,
                                'Test MAE': test_mae,
                                'Test RMSE': test_rmse,
                                'Test R²': test_r2
                            })
                except Exception as e:
                    st.warning(f"Could not evaluate {model_name} on test set: {str(e)}")
        
        if test_results:
            test_df = pd.DataFrame(test_results)
            st.dataframe(test_df.round(4))
            
            # Best model identification
            best_model = test_df.loc[test_df['Test MAE'].idxmin(), 'Model']
            st.success(f"🏆 Best performing model: **{best_model}** (lowest Test MAE)")

# Model details section
if hasattr(st.session_state, 'training_results'):
    st.markdown("### 🔍 Model Details")
    
    selected_model = st.selectbox(
        "Select model for detailed analysis",
        options=list(st.session_state.training_results.keys())
    )
    
    if selected_model and hasattr(st.session_state, 'test_data'):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### {selected_model} Metrics")
            metrics = st.session_state.training_results[selected_model]
            
            metric_df = pd.DataFrame({
                'Metric': ['MAE', 'RMSE', 'R²'],
                'Training': [metrics['train_mae'], metrics['train_rmse'], metrics['train_r2']],
                'Validation': [metrics['val_mae'], metrics['val_rmse'], metrics['val_r2']]
            })
            
            st.dataframe(metric_df.round(4))
        
        with col2:
            # Residuals plot
            if selected_model != 'Prophet':
                try:
                    X_test, y_test = st.session_state.test_data
                    y_pred = st.session_state.model_trainer.predict(selected_model, X_test)
                    
                    if y_pred is not None and len(y_pred) > 0:
                        if selected_model == 'LSTM' and len(y_pred) != len(y_test):
                            y_test_aligned = y_test[-len(y_pred):]
                        else:
                            y_test_aligned = y_test
                            
                        if len(y_pred) == len(y_test_aligned):
                            residuals_fig = create_residuals_plot(y_test_aligned, y_pred, selected_model)
                            st.plotly_chart(residuals_fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Could not create residuals plot: {str(e)}")

# Model saving/loading section
st.markdown("## 💾 Model Management")

col1, col2 = st.columns(2)

with col1:
    if st.button("Save Trained Models"):
        st.success("✅ Models saved to session state!")
        st.info("Models are available for predictions on the next page.")

with col2:
    if st.button("Clear All Models"):
        st.session_state.model_trainer = ModelTrainer()
        if hasattr(st.session_state, 'training_results'):
            del st.session_state.training_results
        st.success("✅ All models cleared!")
        st.rerun()
