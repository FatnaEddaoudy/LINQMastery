import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import streamlit as st

def create_price_chart(df, title="Bitcoin Price Chart"):
    """Create interactive price chart with candlesticks"""
    fig = go.Figure()
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="Price"
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False,
        height=600
    )
    
    return fig

def create_volume_chart(df, title="Bitcoin Volume Chart"):
    """Create volume chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['Date'],
        y=df['Volume'],
        name="Volume",
        marker_color='rgba(158,202,225,0.6)'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Volume",
        height=400
    )
    
    return fig

def create_technical_indicators_chart(df):
    """Create chart with technical indicators"""
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Price & Moving Averages', 'RSI', 'MACD'),
        vertical_spacing=0.08,
        row_heights=[0.6, 0.2, 0.2]
    )
    
    # Price and moving averages
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close Price', line=dict(color='blue')), row=1, col=1)
    
    if 'SMA_20' in df.columns:
        fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_20'], name='SMA 20', line=dict(color='red', dash='dash')), row=1, col=1)
    if 'SMA_50' in df.columns:
        fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'], name='SMA 50', line=dict(color='green', dash='dash')), row=1, col=1)
    
    # Bollinger Bands
    if 'BB_Upper' in df.columns and 'BB_Lower' in df.columns:
        fig.add_trace(go.Scatter(x=df['Date'], y=df['BB_Upper'], name='BB Upper', line=dict(color='gray', dash='dot')), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['Date'], y=df['BB_Lower'], name='BB Lower', line=dict(color='gray', dash='dot'), fill='tonexty'), row=1, col=1)
    
    # RSI
    if 'RSI' in df.columns:
        fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], name='RSI', line=dict(color='purple')), row=2, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
    
    # MACD
    if 'MACD' in df.columns and 'MACD_Signal' in df.columns:
        fig.add_trace(go.Scatter(x=df['Date'], y=df['MACD'], name='MACD', line=dict(color='blue')), row=3, col=1)
        fig.add_trace(go.Scatter(x=df['Date'], y=df['MACD_Signal'], name='MACD Signal', line=dict(color='red')), row=3, col=1)
        
        if 'MACD_Histogram' in df.columns:
            fig.add_trace(go.Bar(x=df['Date'], y=df['MACD_Histogram'], name='MACD Histogram', marker_color='gray'), row=3, col=1)
    
    fig.update_layout(height=800, title_text="Technical Indicators Analysis")
    return fig

def create_prediction_chart(dates, actual, predictions, model_names, title="Price Predictions"):
    """Create chart comparing actual vs predicted prices"""
    fig = go.Figure()
    
    # Actual prices
    fig.add_trace(go.Scatter(
        x=dates,
        y=actual,
        name='Actual Price',
        line=dict(color='black', width=2)
    ))
    
    # Model predictions
    colors = ['red', 'blue', 'green', 'purple', 'orange']
    for i, (model_name, pred) in enumerate(zip(model_names, predictions)):
        if pred is not None and len(pred) > 0:
            fig.add_trace(go.Scatter(
                x=dates[:len(pred)],
                y=pred,
                name=f'{model_name} Prediction',
                line=dict(color=colors[i % len(colors)], dash='dash')
            ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        height=600,
        legend=dict(x=0, y=1)
    )
    
    return fig

def create_forecast_chart(df, forecast_data, days_ahead=30):
    """Create forecast chart for future predictions"""
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Close'],
        name='Historical Price',
        line=dict(color='blue')
    ))
    
    # Future predictions
    last_date = df['Date'].iloc[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=days_ahead)
    
    for model_name, predictions in forecast_data.items():
        if predictions is not None and len(predictions) > 0:
            fig.add_trace(go.Scatter(
                x=future_dates[:len(predictions)],
                y=predictions,
                name=f'{model_name} Forecast',
                line=dict(dash='dash')
            ))
    
    fig.update_layout(
        title=f"Bitcoin Price Forecast - Next {days_ahead} Days",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        height=600
    )
    
    return fig

def create_model_comparison_chart(metrics_df):
    """Create model comparison chart"""
    fig = go.Figure()
    
    models = metrics_df.index
    metrics = ['MAE', 'RMSE', 'R²']
    colors = ['red', 'blue', 'green']
    
    for i, metric in enumerate(metrics):
        if metric in metrics_df.columns:
            fig.add_trace(go.Bar(
                name=metric,
                x=models,
                y=metrics_df[metric],
                marker_color=colors[i]
            ))
    
    fig.update_layout(
        title="Model Performance Comparison",
        xaxis_title="Models",
        yaxis_title="Score",
        barmode='group',
        height=500
    )
    
    return fig

def create_correlation_heatmap(df):
    """Create correlation heatmap for features"""
    # Select numeric columns only
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr_matrix = df[numeric_cols].corr()
    
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Feature Correlation Heatmap",
        color_continuous_scale="RdBu"
    )
    
    fig.update_layout(height=800)
    return fig

def create_feature_importance_chart(model, feature_names, model_name):
    """Create feature importance chart for tree-based models"""
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1][:20]  # Top 20 features
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[feature_names[i] for i in indices],
            y=[importances[i] for i in indices],
            marker_color='lightblue'
        ))
        
        fig.update_layout(
            title=f"Top 20 Feature Importances - {model_name}",
            xaxis_title="Features",
            yaxis_title="Importance",
            height=500,
            xaxis_tickangle=-45
        )
        
        return fig
    
    return None

def create_residuals_plot(y_true, y_pred, model_name):
    """Create residuals plot"""
    residuals = y_true - y_pred
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(f'{model_name} - Residuals vs Predicted', f'{model_name} - Residuals Distribution')
    )
    
    # Residuals vs Predicted
    fig.add_trace(
        go.Scatter(x=y_pred, y=residuals, mode='markers', name='Residuals'),
        row=1, col=1
    )
    fig.add_hline(y=0, line_dash="dash", line_color="red", row=1, col=1)
    
    # Residuals distribution
    fig.add_trace(
        go.Histogram(x=residuals, name='Distribution', nbinsx=30),
        row=1, col=2
    )
    
    fig.update_layout(height=400, title_text=f"Residuals Analysis - {model_name}")
    return fig
