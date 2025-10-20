import streamlit as st
import pandas as pd
import numpy as np
from utils.data_preprocessing import load_csv_data, preprocess_data
from utils.visualizations import create_price_chart
from utils.api_integration import fetch_bitcoin_historical_coingecko, get_live_bitcoin_metrics, update_data_with_latest_price

st.set_page_config(page_title="Data Upload", page_icon="📈", layout="wide")

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'models' not in st.session_state:
    st.session_state.models = {}
if 'predictions' not in st.session_state:
    st.session_state.predictions = {}

st.title("📈 Data Upload & Processing")
st.markdown("Upload your Bitcoin price data or use the provided sample data.")

# File upload section
st.markdown("## 📁 Data Upload")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload a CSV file with columns: Date, Open, High, Low, Close, Volume"
    )
    
    if uploaded_file is not None:
        # Load the uploaded data
        data = load_csv_data(uploaded_file)
        
        if data is not None:
            st.session_state.data = data
            st.success(f"✅ Data uploaded successfully! {len(data)} rows loaded.")
        else:
            st.error("❌ Failed to load data. Please check your CSV format.")

with col2:
    st.markdown("### Required CSV Format")
    st.code("""
    Date,Open,High,Low,Close,Volume
    2024-01-01,45000.00,46000.00,44000.00,45500.00,1000000
    2024-01-02,45500.00,47000.00,45000.00,46500.00,1200000
    ...
    """)

# Sample data and API data section
if st.session_state.data is None:
    st.markdown("## 🔄 No Data? Load Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📁 Load Sample Data")
        if st.button("Load Sample Bitcoin Data", use_container_width=True):
            # Load actual Bitcoin data from the provided CSV
            try:
                sample_data = load_csv_data("attached_assets/bitcoin_1760372614411.csv")
                if sample_data is not None:
                    st.session_state.data = sample_data
                    st.success("✅ Sample Bitcoin data loaded successfully!")
                    st.rerun()
                else:
                    st.error("Failed to load sample data")
            except Exception as e:
                st.error(f"Error loading sample data: {str(e)}")
    
    with col2:
        st.markdown("### 🌐 Fetch Live Data from API")
        st.info("📅 Fetches data from **TODAY backwards**. For example, 365 days gets you Oct 2024 - Oct 2025 (current).")
        st.warning("⚠️ **Recommended: 90+ days** for reliable model training. Less data may reduce accuracy.")
        days_to_fetch = st.selectbox("Select time period", [30, 90, 180, 365, 730], index=3)
        
        if st.button("Fetch Bitcoin Data from CoinGecko", use_container_width=True):
            with st.spinner(f"Fetching {days_to_fetch} days of Bitcoin data..."):
                try:
                    api_data = fetch_bitcoin_historical_coingecko(days=days_to_fetch)
                    if api_data is not None and len(api_data) > 0:
                        st.session_state.data = api_data
                        # Show date range clearly
                        start_date = api_data['Date'].min().strftime('%b %d, %Y')
                        end_date = api_data['Date'].max().strftime('%b %d, %Y')
                        st.success(f"✅ Fetched {len(api_data)} days of Bitcoin data!")
                        st.info(f"📅 Date range: **{start_date}** → **{end_date}** (includes current 2025 data)")
                        st.rerun()
                    else:
                        st.error("Failed to fetch data from API")
                except Exception as e:
                    st.error(f"Error fetching API data: {str(e)}")

# Data preview and processing
if st.session_state.data is not None:
    st.markdown("## 📊 Data Preview")
    
    # Basic statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(st.session_state.data))
    
    with col2:
        start_date = st.session_state.data['Date'].min().strftime('%Y-%m-%d')
        end_date = st.session_state.data['Date'].max().strftime('%Y-%m-%d')
        st.metric("Date Range", f"{start_date} to {end_date}")
    
    with col3:
        latest_date = st.session_state.data['Date'].max().strftime('%b %d, %Y')
        st.metric("Latest Price", f"${st.session_state.data['Close'].iloc[-1]:,.2f}", f"As of {latest_date}")
    
    with col4:
        price_change = st.session_state.data['Close'].iloc[-1] - st.session_state.data['Close'].iloc[-2]
        st.metric("Price Change", f"${price_change:.2f}", f"{price_change:.2f}")
    
    # Show data table
    st.markdown("### Raw Data")
    
    tab1, tab2, tab3 = st.tabs(["📅 Latest Data (Most Recent)", "📊 First 20 Rows", "📈 Last 20 Rows"])
    
    with tab1:
        st.markdown("**Most recent Bitcoin data (today's data):**")
        st.dataframe(st.session_state.data.tail(10), use_container_width=True)
    
    with tab2:
        st.markdown("**First 20 rows (oldest data):**")
        st.dataframe(st.session_state.data.head(20), use_container_width=True)
    
    with tab3:
        st.markdown("**Last 20 rows (newest data):**")
        st.dataframe(st.session_state.data.tail(20), use_container_width=True)
    
    # Data processing section
    st.markdown("## ⚙️ Data Processing")
    
    auto_retrain = st.checkbox("🔄 Automatically retrain models after processing", value=False, 
                               help="Train all models automatically after data processing")
    
    if st.button("Process Data & Calculate Technical Indicators"):
        with st.spinner("Processing data and calculating technical indicators..."):
            try:
                processed_data = preprocess_data(st.session_state.data)
                st.session_state.processed_data = processed_data
                
                st.success("✅ Data processing completed!")
                
                # Auto-retrain models if enabled
                if auto_retrain:
                    st.info("🔄 Auto-retraining models with new data...")
                    
                    # Import training utilities
                    from utils.model_training import ModelTrainer
                    from utils.data_preprocessing import create_features_target, split_data
                    
                    # Initialize model trainer
                    if 'model_trainer' not in st.session_state:
                        st.session_state.model_trainer = ModelTrainer()
                    
                    # Prepare data
                    X, y, feature_names = create_features_target(
                        processed_data, 
                        target_column='Close', 
                        forecast_days=1
                    )
                    
                    # Split data
                    X_train, X_val, X_test, y_train, y_val, y_test = split_data(
                        X, y, test_size=0.2, validation_size=0.1
                    )
                    
                    st.session_state.model_trainer.feature_names = feature_names
                    
                    # Train models
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    models_to_train = ['Linear Regression', 'Random Forest', 'XGBoost', 'LSTM', 'Prophet']
                    results = {}
                    
                    for idx, model_name in enumerate(models_to_train):
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
                                # LSTM can be skipped if insufficient data
                                if metrics is None:
                                    status_text.text(f"⏭️ {model_name} skipped (insufficient data)")
                            elif model_name == 'Prophet':
                                metrics = st.session_state.model_trainer.train_prophet(
                                    processed_data, target_column='Close'
                                )
                            
                            if metrics:
                                results[model_name] = metrics
                                status_text.text(f"✅ {model_name} trained successfully")
                        
                        except Exception as e:
                            st.warning(f"⚠️ Could not train {model_name}: {str(e)}")
                        
                        progress_bar.progress((idx + 1) / len(models_to_train))
                    
                    status_text.text("✅ Auto-retraining completed!")
                    st.session_state.training_results = results
                    st.session_state.test_data = (X_test, y_test)
                    
                    st.success(f"✅ Successfully retrained {len(results)} models!")
                    st.info("Navigate to Model Training page to view detailed results.")
                
                # Show processing results
                st.markdown("### Processing Results")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Original Features", len(st.session_state.data.columns))
                    st.metric("Processed Features", len(processed_data.columns))
                
                with col2:
                    st.metric("Records Before", len(st.session_state.data))
                    st.metric("Records After", len(processed_data))
                
                # Show new features
                st.markdown("### New Technical Indicators")
                new_features = [col for col in processed_data.columns if col not in st.session_state.data.columns]
                
                if new_features:
                    st.multiselect(
                        "Technical indicators added:",
                        new_features,
                        default=new_features[:10] if len(new_features) > 10 else new_features,
                        disabled=True
                    )
                
                # Preview processed data
                st.markdown("### Processed Data Preview")
                st.dataframe(processed_data[['Date', 'Close', 'SMA_20', 'RSI', 'MACD', 'BB_Upper', 'BB_Lower']].tail(10))
                
            except Exception as e:
                st.error(f"Error processing data: {str(e)}")
    
    # Quick visualization
    st.markdown("## 📈 Quick Visualization")
    
    if st.checkbox("Show Price Chart"):
        try:
            chart = create_price_chart(st.session_state.data, "Bitcoin Price Overview")
            st.plotly_chart(chart, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")
    
    # Data quality checks
    st.markdown("## 🔍 Data Quality Check")
    
    # Missing values
    missing_values = st.session_state.data.isnull().sum()
    if missing_values.sum() > 0:
        st.warning("⚠️ Missing values detected:")
        st.dataframe(missing_values[missing_values > 0])
    else:
        st.success("✅ No missing values found")
    
    # Data types
    with st.expander("Data Types"):
        st.dataframe(pd.DataFrame({
            'Column': st.session_state.data.columns,
            'Data Type': st.session_state.data.dtypes,
            'Non-Null Count': st.session_state.data.count()
        }))
    
    # Basic statistics
    with st.expander("Statistical Summary"):
        st.dataframe(st.session_state.data.describe())

else:
    st.info("👆 Please upload a CSV file or load sample data to get started!")
    
    # Show example CSV format
    st.markdown("## 📋 Expected CSV Format")
    example_data = pd.DataFrame({
        'Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'Open': [45000.00, 45500.00, 46000.00],
        'High': [46000.00, 47000.00, 47500.00],
        'Low': [44000.00, 45000.00, 45500.00],
        'Close': [45500.00, 46500.00, 47000.00],
        'Volume': [1000000, 1200000, 1100000]
    })
    st.dataframe(example_data)
