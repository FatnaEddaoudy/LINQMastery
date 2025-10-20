import streamlit as st
import pandas as pd
import numpy as np
from utils.visualizations import (
    create_price_chart, create_volume_chart, create_technical_indicators_chart,
    create_correlation_heatmap
)

st.set_page_config(page_title="Data Visualization", page_icon="📊", layout="wide")

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

st.title("📊 Data Visualization Dashboard")

if st.session_state.data is None:
    st.warning("⚠️ No data available. Please upload data first!")
    st.stop()

# Sidebar for visualization options
st.sidebar.header("Visualization Options")

# Date range selector
min_date = st.session_state.data['Date'].min()
max_date = st.session_state.data['Date'].max()

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Filter data based on date range
filtered_data = st.session_state.data[
    (st.session_state.data['Date'] >= pd.to_datetime(start_date)) &
    (st.session_state.data['Date'] <= pd.to_datetime(end_date))
].copy()

st.markdown(f"## 📈 Visualizing {len(filtered_data)} data points from {start_date} to {end_date}")

# Main price chart
st.markdown("### 💰 Bitcoin Price Chart")
try:
    price_chart = create_price_chart(filtered_data, f"Bitcoin Price ({start_date} to {end_date})")
    st.plotly_chart(price_chart, use_container_width=True)
except Exception as e:
    st.error(f"Error creating price chart: {str(e)}")

# Key metrics - using wider columns for better text display
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current Price", 
        f"${filtered_data['Close'].iloc[-1]:,.2f}",
        delta=f"{((filtered_data['Close'].iloc[-1] / filtered_data['Close'].iloc[0]) - 1) * 100:.2f}%"
    )

with col2:
    st.metric(
        "High", 
        f"${filtered_data['High'].max():,.2f}"
    )

with col3:
    st.metric(
        "Low", 
        f"${filtered_data['Low'].min():,.2f}"
    )

with col4:
    avg_vol = filtered_data['Volume'].mean()
    if avg_vol >= 1e9:
        vol_display = f"{avg_vol/1e9:.1f}B"
    elif avg_vol >= 1e6:
        vol_display = f"{avg_vol/1e6:.1f}M"
    else:
        vol_display = f"{avg_vol:,.0f}"
    st.metric(
        "Avg Volume", 
        vol_display
    )

# Volume chart
st.markdown("### 📊 Trading Volume")
try:
    volume_chart = create_volume_chart(filtered_data, f"Bitcoin Volume ({start_date} to {end_date})")
    st.plotly_chart(volume_chart, use_container_width=True)
except Exception as e:
    st.error(f"Error creating volume chart: {str(e)}")

# Technical indicators (if processed data is available)
if st.session_state.processed_data is not None:
    st.markdown("### 🔧 Technical Indicators")
    
    # Filter processed data
    processed_filtered = st.session_state.processed_data[
        (st.session_state.processed_data['Date'] >= pd.to_datetime(start_date)) &
        (st.session_state.processed_data['Date'] <= pd.to_datetime(end_date))
    ].copy()
    
    try:
        tech_chart = create_technical_indicators_chart(processed_filtered)
        st.plotly_chart(tech_chart, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating technical indicators chart: {str(e)}")
    
    # Technical indicators summary
    st.markdown("### 📋 Current Technical Indicators")
    if len(processed_filtered) > 0:
        latest = processed_filtered.iloc[-1]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Moving Averages**")
            if 'SMA_20' in latest:
                st.metric("SMA 20", f"${latest.get('SMA_20', 0):,.0f}")
            if 'SMA_50' in latest:
                st.metric("SMA 50", f"${latest.get('SMA_50', 0):,.0f}")
            if 'EMA_12' in latest:
                st.metric("EMA 12", f"${latest.get('EMA_12', 0):,.0f}")
        
        with col2:
            st.markdown("**Oscillators**")
            if 'RSI' in latest:
                rsi_value = latest.get('RSI', 50)
                rsi_status = "Overbought" if rsi_value > 70 else "Oversold" if rsi_value < 30 else "Neutral"
                st.metric("RSI", f"{rsi_value:.1f}", delta=rsi_status)
            
            if 'MACD' in latest:
                st.metric("MACD", f"{latest.get('MACD', 0):,.1f}")
        
        with col3:
            st.markdown("**Bollinger Bands**")
            if 'BB_Upper' in latest and 'BB_Lower' in latest:
                st.metric("BB Upper", f"${latest.get('BB_Upper', 0):,.0f}")
                st.metric("BB Lower", f"${latest.get('BB_Lower', 0):,.0f}")
                
                bb_position = latest.get('BB_Position', 0.5)
                bb_status = "Near Upper" if bb_position > 0.8 else "Near Lower" if bb_position < 0.2 else "Middle"
                st.metric("BB Position", f"{bb_position*100:.1f}%", delta=bb_status)

# Price distribution analysis
st.markdown("### 📈 Price Distribution Analysis")

col1, col2 = st.columns(2)

with col1:
    # Price returns histogram
    returns = filtered_data['Close'].pct_change().dropna() * 100
    
    import plotly.express as px
    fig_hist = px.histogram(
        x=returns,
        nbins=50,
        title="Daily Returns Distribution (%)",
        labels={'x': 'Daily Return (%)', 'y': 'Frequency'}
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    # Price vs Volume scatter
    fig_scatter = px.scatter(
        filtered_data,
        x='Volume',
        y='Close',
        title="Price vs Volume Relationship",
        labels={'Volume': 'Trading Volume', 'Close': 'Closing Price (USD)'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# Statistical summary
st.markdown("### 📊 Statistical Summary")

summary_stats = filtered_data[['Open', 'High', 'Low', 'Close', 'Volume']].describe()
st.dataframe(summary_stats)

# Volatility analysis
st.markdown("### 📊 Volatility Analysis")

col1, col2 = st.columns(2)

with col1:
    # Rolling volatility
    if len(filtered_data) > 30:
        rolling_vol = filtered_data['Close'].pct_change().rolling(window=30).std() * np.sqrt(365) * 100
        
        fig_vol = px.line(
            x=filtered_data['Date'],
            y=rolling_vol,
            title="30-Day Rolling Volatility (%)",
            labels={'x': 'Date', 'y': 'Volatility (%)'}
        )
        st.plotly_chart(fig_vol, use_container_width=True)

with col2:
    # High-Low percentage
    high_low_pct = ((filtered_data['High'] - filtered_data['Low']) / filtered_data['Close']) * 100
    
    fig_hl = px.line(
        x=filtered_data['Date'],
        y=high_low_pct,
        title="Daily High-Low Range (%)",
        labels={'x': 'Date', 'y': 'High-Low Range (%)'}
    )
    st.plotly_chart(fig_hl, use_container_width=True)

# Correlation analysis (if processed data available)
if st.session_state.processed_data is not None:
    st.markdown("### 🔗 Feature Correlation Analysis")
    
    if st.checkbox("Show Correlation Heatmap"):
        with st.spinner("Generating correlation heatmap..."):
            try:
                # Select a subset of features for correlation
                feature_cols = [col for col in processed_filtered.columns if col not in ['Date'] and processed_filtered[col].dtype in ['float64', 'int64']]
                if len(feature_cols) > 50:
                    feature_cols = feature_cols[:50]  # Limit to first 50 features
                
                correlation_data = processed_filtered[feature_cols]
                corr_fig = create_correlation_heatmap(correlation_data)
                st.plotly_chart(corr_fig, use_container_width=True)
                
                # Top correlations with Close price
                if 'Close' in correlation_data.columns:
                    close_corr = correlation_data.corr()['Close'].abs().sort_values(ascending=False)
                    st.markdown("#### Top Features Correlated with Close Price")
                    st.dataframe(close_corr.head(10).to_frame('Correlation'))
                    
            except Exception as e:
                st.error(f"Error generating correlation heatmap: {str(e)}")

# Market trend analysis
st.markdown("### 📈 Market Trend Analysis")

if len(filtered_data) > 1:
    # Calculate trend metrics
    total_return = ((filtered_data['Close'].iloc[-1] / filtered_data['Close'].iloc[0]) - 1) * 100
    volatility = filtered_data['Close'].pct_change().std() * np.sqrt(365) * 100
    
    # Bull/Bear market identification
    sma_50 = filtered_data['Close'].rolling(window=min(50, len(filtered_data)//2)).mean()
    sma_200 = filtered_data['Close'].rolling(window=min(200, len(filtered_data)//2)).mean()
    
    current_trend = "Bullish" if filtered_data['Close'].iloc[-1] > sma_50.iloc[-1] else "Bearish"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Return", f"{total_return:.2f}%")
    
    with col2:
        st.metric("Annualized Volatility", f"{volatility:.2f}%")
    
    with col3:
        st.metric("Current Trend", current_trend)

# Export options
st.markdown("### 💾 Export Options")

col1, col2 = st.columns(2)

with col1:
    if st.button("Download Filtered Data"):
        csv = filtered_data.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"bitcoin_data_{start_date}_{end_date}.csv",
            mime="text/csv"
        )

with col2:
    if st.session_state.processed_data is not None:
        if st.button("Download Processed Data"):
            csv = processed_filtered.to_csv(index=False)
            st.download_button(
                label="Download Processed CSV",
                data=csv,
                file_name=f"bitcoin_processed_{start_date}_{end_date}.csv",
                mime="text/csv"
            )
