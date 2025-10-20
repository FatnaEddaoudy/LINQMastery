import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from utils.data_preprocessing import preprocess_data, calculate_technical_indicators
from utils.visualizations import create_price_chart, create_volume_chart
from utils.api_integration import get_live_bitcoin_metrics, update_data_with_latest_price

# Configure page
st.set_page_config(
    page_title="Bitcoin Price Prediction",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'models' not in st.session_state:
    st.session_state.models = {}
if 'predictions' not in st.session_state:
    st.session_state.predictions = {}

# Main page
st.title("₿ Bitcoin Price Prediction using Machine Learning")
st.markdown("### Welcome to the comprehensive Bitcoin price prediction platform")

# Live Bitcoin Price Display
st.markdown("---")
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("## 📊 Live Bitcoin Price")

with col2:
    if st.button("🔄 Refresh Price"):
        st.rerun()

live_metrics = get_live_bitcoin_metrics()
if live_metrics:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Price", 
            f"${live_metrics['current_price']:,.2f}",
            delta=f"{live_metrics['change_24h']:.2f}%" if live_metrics['change_24h'] else None
        )
    
    with col2:
        st.metric(
            "24h Volume",
            f"${live_metrics['volume_24h']:,.0f}"
        )
    
    with col3:
        change_value = (live_metrics['current_price'] * live_metrics['change_24h'] / 100) if live_metrics['change_24h'] else 0
        st.metric(
            "24h Change",
            f"${abs(change_value):,.2f}",
            delta=f"{live_metrics['change_24h']:.2f}%" if live_metrics['change_24h'] else None
        )
    
    with col4:
        st.metric(
            "Last Updated",
            live_metrics['last_updated'].split(' ')[1]
        )

st.markdown("---")

# Display app overview
col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **📈 Data Analysis**
    - Upload Bitcoin price data
    - Automated data preprocessing
    - Technical indicators calculation
    """)

with col2:
    st.success("""
    **🤖 ML Models**
    - Linear Regression
    - Random Forest
    - LSTM Neural Network
    - XGBoost
    - Prophet (Time Series)
    """)

with col3:
    st.warning("""
    **🔮 Predictions**
    - Next-day price prediction
    - Multi-day forecasting
    - Trend analysis
    - Model comparison
    """)

# Navigation instructions
st.markdown("---")
st.markdown("## 🚀 Getting Started")
st.markdown("""
1. **📈 Data Upload**: Upload your Bitcoin price CSV file or use the sample data
2. **📊 Data Visualization**: Explore your data with interactive charts
3. **🤖 Model Training**: Train multiple ML models on your data
4. **🔮 Predictions**: Generate predictions and forecasts
5. **📋 Model Comparison**: Compare model performance and accuracy
""")

# Show data status
if st.session_state.data is not None:
    st.success(f"✅ Data loaded successfully! {len(st.session_state.data)} rows available")
    
    # Quick data preview
    st.markdown("### Quick Data Preview")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(st.session_state.data.tail(10))
    
    with col2:
        st.metric("Latest Close Price", f"${st.session_state.data['Close'].iloc[-1]:.2f}")
        st.metric("Data Range", f"{len(st.session_state.data)} days")
        st.metric("Date Range", f"{st.session_state.data['Date'].iloc[0].strftime('%Y-%m-%d')} to {st.session_state.data['Date'].iloc[-1].strftime('%Y-%m-%d')}")

else:
    st.info("👈 Please upload data using the **Data Upload** page in the sidebar to get started!")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit • Machine Learning for Bitcoin Price Prediction")
