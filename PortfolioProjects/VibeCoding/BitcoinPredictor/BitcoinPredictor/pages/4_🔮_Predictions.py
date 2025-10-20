import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.visualizations import create_prediction_chart, create_forecast_chart
from utils.data_preprocessing import create_features_target
from utils.pdf_generator import create_prediction_pdf, create_forecast_pdf
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

st.set_page_config(page_title="Predictions", page_icon="🔮", layout="wide")

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'model_trainer' not in st.session_state:
    from utils.model_training import ModelTrainer
    st.session_state.model_trainer = ModelTrainer()

st.title("🔮 Bitcoin Price Predictions")

if not hasattr(st.session_state, 'model_trainer') or not st.session_state.model_trainer.models:
    st.warning("⚠️ No trained models available. Please train models first!")
    st.stop()

if st.session_state.processed_data is None:
    st.warning("⚠️ No processed data available. Please upload and process data first!")
    st.stop()

# Sidebar for prediction options
st.sidebar.header("Prediction Settings")

available_models = list(st.session_state.model_trainer.models.keys())
selected_models = st.sidebar.multiselect(
    "Select Models for Prediction",
    options=available_models,
    default=available_models
)

use_ensemble = st.sidebar.checkbox("Use Ensemble Prediction", value=True, help="Combine predictions from all models")
if use_ensemble:
    ensemble_method = st.sidebar.selectbox(
        "Ensemble Method",
        options=['mean', 'median', 'weighted'],
        format_func=lambda x: {'mean': 'Average', 'median': 'Median', 'weighted': 'Weighted Average'}[x]
    )

prediction_type = st.sidebar.radio(
    "Prediction Type",
    ["Next Day Prediction", "Multi-Day Forecast", "Historical Backtest"]
)

# Main content based on prediction type
if prediction_type == "Next Day Prediction":
    st.markdown("## 📅 Next Day Price Prediction")
    
    if st.button("🎯 Generate Next Day Predictions", type="primary"):
        with st.spinner("Generating predictions..."):
            try:
                # Prepare the most recent data for prediction
                X, y, feature_names = create_features_target(
                    st.session_state.processed_data, 
                    target_column='Close', 
                    forecast_days=1
                )
                
                # Use the last available data point for prediction
                last_features = X[-1:] if len(X) > 0 else None
                current_price = st.session_state.processed_data['Close'].iloc[-1]
                
                predictions = {}
                
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    st.markdown("### 🔮 Model Predictions")
                    
                    results = []
                    
                    for model_name in selected_models:
                        if model_name == 'Prophet':
                            # Prophet prediction
                            forecast = st.session_state.model_trainer.predict_prophet(periods=1)
                            if forecast is not None:
                                pred_price = forecast['yhat'].iloc[-1]
                                predictions[model_name] = pred_price
                                
                                price_change = pred_price - current_price
                                price_change_pct = (price_change / current_price) * 100
                                
                                results.append({
                                    'Model': model_name,
                                    'Predicted Price': f"${pred_price:.2f}",
                                    'Price Change': f"${price_change:+.2f}",
                                    'Change %': f"{price_change_pct:+.2f}%",
                                    'Trend': '📈 Up' if price_change > 0 else '📉 Down' if price_change < 0 else '➡️ Stable'
                                })
                        
                        else:
                            # Other models
                            if last_features is not None:
                                pred_price = st.session_state.model_trainer.predict(model_name, last_features)
                                
                                if pred_price is not None and len(pred_price) > 0:
                                    pred_price = pred_price[0]
                                    predictions[model_name] = pred_price
                                    
                                    price_change = pred_price - current_price
                                    price_change_pct = (price_change / current_price) * 100
                                    
                                    results.append({
                                        'Model': model_name,
                                        'Predicted Price': f"${pred_price:.2f}",
                                        'Price Change': f"${price_change:+.2f}",
                                        'Change %': f"{price_change_pct:+.2f}%",
                                        'Trend': '📈 Up' if price_change > 0 else '📉 Down' if price_change < 0 else '➡️ Stable'
                                    })
                    
                    if results:
                        results_df = pd.DataFrame(results)
                        st.dataframe(
                            results_df, 
                            use_container_width=True, 
                            height=400,
                            column_config={
                                "Model": st.column_config.TextColumn("Model", width="medium"),
                                "Predicted Price": st.column_config.TextColumn("Predicted Price", width="large"),
                                "Price Change": st.column_config.TextColumn("Price Change", width="medium"),
                                "Change %": st.column_config.TextColumn("Change %", width="medium"),
                                "Trend": st.column_config.TextColumn("Trend", width="small")
                            }
                        )
                        
                        # Ensemble prediction
                        if use_ensemble and len(predictions) > 1 and last_features is not None:
                            ensemble_pred = st.session_state.model_trainer.predict_ensemble(
                                last_features, method=ensemble_method
                            )
                            
                            if ensemble_pred is not None and len(ensemble_pred) > 0:
                                ensemble_price = ensemble_pred[0]
                                ensemble_change = ensemble_price - current_price
                                ensemble_change_pct = (ensemble_change / current_price) * 100
                                
                                st.markdown("### 🎯 Ensemble Prediction")
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.metric(
                                        f"Ensemble ({ensemble_method.capitalize()})",
                                        f"${ensemble_price:.2f}",
                                        f"{ensemble_change_pct:+.2f}%"
                                    )
                                
                                with col2:
                                    st.metric(
                                        "Models Used",
                                        len([m for m in selected_models if m != 'Prophet'])
                                    )
                                
                                with col3:
                                    trend = '📈 Bullish' if ensemble_change > 0 else '📉 Bearish' if ensemble_change < 0 else '➡️ Neutral'
                                    st.metric("Trend", trend)
                                
                                # Add ensemble to predictions for visualization
                                predictions['Ensemble'] = ensemble_price
                        
                        # Consensus prediction (if not using ensemble)
                        elif len(predictions) > 1:
                            avg_prediction = np.mean(list(predictions.values()))
                            avg_change = avg_prediction - current_price
                            avg_change_pct = (avg_change / current_price) * 100
                            
                            st.markdown("### 🎯 Consensus Prediction")
                            st.metric(
                                "Average Predicted Price",
                                f"${avg_prediction:.2f}",
                                f"{avg_change_pct:+.2f}%"
                            )
                
                with col2:
                    st.markdown("### 📊 Current Market Status")
                    st.metric("Current Price", f"${current_price:.2f}")
                    st.metric("Date", st.session_state.processed_data['Date'].iloc[-1].strftime('%Y-%m-%d'))
                    
                    if len(predictions) > 0:
                        pred_range = max(predictions.values()) - min(predictions.values())
                        st.metric("Prediction Range", f"${pred_range:.2f}")
                        
                        # Model agreement
                        up_votes = sum(1 for p in predictions.values() if p > current_price)
                        down_votes = len(predictions) - up_votes
                        
                        st.markdown("#### Model Consensus")
                        st.write(f"📈 Bullish: {up_votes} models")
                        st.write(f"📉 Bearish: {down_votes} models")
                
                # Trading Recommendation
                if len(predictions) > 0:
                    st.markdown("---")
                    st.markdown("## 💡 Trading Recommendation")
                    
                    # Calculate recommendation based on predictions
                    avg_pred = np.mean(list(predictions.values()))
                    price_change_pct = ((avg_pred - current_price) / current_price) * 100
                    
                    # Calculate confidence based on model agreement
                    bullish_pct = (up_votes / len(predictions)) * 100
                    confidence = abs(bullish_pct - 50) * 2  # 0-100% scale
                    
                    # Determine recommendation
                    if price_change_pct > 2:
                        recommendation = "🟢 STRONG BUY"
                        explanation = f"Models predict a significant price increase of {price_change_pct:.2f}%. This suggests a strong buying opportunity."
                        color = "green"
                    elif price_change_pct > 0.5:
                        recommendation = "🟢 BUY"
                        explanation = f"Models predict a moderate price increase of {price_change_pct:.2f}%. Consider buying if aligned with your strategy."
                        color = "green"
                    elif price_change_pct > -0.5:
                        recommendation = "🟡 HOLD"
                        explanation = f"Models predict minimal price change ({price_change_pct:+.2f}%). Current position holding is recommended."
                        color = "orange"
                    elif price_change_pct > -2:
                        recommendation = "🔴 SELL"
                        explanation = f"Models predict a moderate price decrease of {price_change_pct:.2f}%. Consider reducing exposure."
                        color = "red"
                    else:
                        recommendation = "🔴 STRONG SELL"
                        explanation = f"Models predict a significant price decrease of {price_change_pct:.2f}%. Consider exiting positions."
                        color = "red"
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.markdown(f"### {recommendation}")
                        st.info(explanation)
                    
                    with col2:
                        st.metric("Confidence", f"{confidence:.0f}%")
                        st.caption(f"Based on {len(predictions)} models")
                    
                    with col3:
                        st.metric("Expected Return", f"{price_change_pct:+.2f}%")
                        st.caption("Next 24 hours")
                    
                    # Risk assessment
                    st.markdown("#### ⚠️ Risk Assessment")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Model Agreement:**")
                        if confidence > 70:
                            st.success(f"✅ High ({confidence:.0f}%) - Models strongly agree")
                        elif confidence > 40:
                            st.warning(f"⚠️ Medium ({confidence:.0f}%) - Some disagreement among models")
                        else:
                            st.error(f"❌ Low ({confidence:.0f}%) - Models significantly disagree")
                    
                    with col2:
                        st.markdown("**Volatility Risk:**")
                        if pred_range / current_price > 0.05:
                            st.error("❌ High - Wide prediction range indicates uncertainty")
                        elif pred_range / current_price > 0.02:
                            st.warning("⚠️ Medium - Moderate prediction variance")
                        else:
                            st.success("✅ Low - Narrow prediction range")
                    
                    st.caption("⚠️ This recommendation is based on ML predictions and should not be considered financial advice. Always do your own research and invest responsibly.")
                
                # Visualization
                if len(predictions) > 0:
                    st.markdown("### 📊 Prediction Visualization")
                    
                    fig = go.Figure()
                    
                    # Historical prices (last 30 days)
                    recent_data = st.session_state.processed_data.tail(30)
                    fig.add_trace(go.Scatter(
                        x=recent_data['Date'],
                        y=recent_data['Close'],
                        name='Historical Price',
                        line=dict(color='blue')
                    ))
                    
                    # Predictions
                    tomorrow = st.session_state.processed_data['Date'].iloc[-1] + timedelta(days=1)
                    
                    colors = ['red', 'green', 'purple', 'orange', 'brown']
                    for i, (model_name, pred_price) in enumerate(predictions.items()):
                        fig.add_trace(go.Scatter(
                            x=[st.session_state.processed_data['Date'].iloc[-1], tomorrow],
                            y=[current_price, pred_price],
                            name=f'{model_name} Prediction',
                            line=dict(color=colors[i % len(colors)], dash='dash'),
                            mode='lines+markers'
                        ))
                    
                    fig.update_layout(
                        title="Next Day Price Predictions",
                        xaxis_title="Date",
                        yaxis_title="Price (USD)",
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Download predictions report
                if len(predictions) > 0:
                    st.markdown("### 💾 Download Predictions Report")
                    
                    # Create report data
                    report_data = {
                        'Date': [tomorrow.strftime('%Y-%m-%d')],
                        'Current_Price': [current_price]
                    }
                    
                    for model_name, pred_price in predictions.items():
                        report_data[f'{model_name}_Prediction'] = [pred_price]
                        report_data[f'{model_name}_Change'] = [pred_price - current_price]
                        report_data[f'{model_name}_Change_Pct'] = [(pred_price - current_price) / current_price * 100]
                    
                    report_df = pd.DataFrame(report_data)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv = report_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV Report",
                            data=csv,
                            file_name=f"bitcoin_prediction_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                    with col2:
                        # Generate PDF report
                        pdf_buffer = create_prediction_pdf(predictions, current_price, "Next Day Prediction")
                        st.download_button(
                            label="📄 Download PDF Report",
                            data=pdf_buffer,
                            file_name=f"bitcoin_prediction_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                
            except Exception as e:
                st.error(f"Error generating predictions: {str(e)}")

elif prediction_type == "Multi-Day Forecast":
    st.markdown("## 📊 Multi-Day Price Forecast")
    
    forecast_mode = st.sidebar.radio("Forecast Mode", ["Preset Days", "Custom Date Range"])
    
    if forecast_mode == "Preset Days":
        forecast_days = st.sidebar.slider("Forecast Days", 7, 90, 30)
    else:
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now().date())
        with col2:
            end_date = st.date_input("End Date", value=(datetime.now() + timedelta(days=30)).date())
        
        forecast_days = (end_date - start_date).days
        
        if forecast_days <= 0:
            st.sidebar.error("End date must be after start date")
            st.stop()
        
        st.sidebar.info(f"Forecasting {forecast_days} days")
    
    if st.button("🔮 Generate Forecast", type="primary"):
        with st.spinner(f"Generating {forecast_days}-day forecast..."):
            try:
                forecasts = {}
                current_price = st.session_state.processed_data['Close'].iloc[-1]
                
                # Prophet forecast
                if 'Prophet' in selected_models:
                    forecast = st.session_state.model_trainer.predict_prophet(periods=forecast_days)
                    if forecast is not None:
                        forecasts['Prophet'] = forecast['yhat'].tail(forecast_days).values
                
                # Other models (simplified approach - using last known features)
                X, y, feature_names = create_features_target(
                    st.session_state.processed_data, 
                    target_column='Close', 
                    forecast_days=1
                )
                
                if len(X) > 0:
                    last_features = X[-1:]
                    
                    for model_name in selected_models:
                        if model_name != 'Prophet':
                            # Simple iterative prediction (not ideal for long horizons)
                            model_forecast = []
                            current_features = last_features.copy()
                            
                            for day in range(min(forecast_days, 7)):  # Limit to 7 days for non-Prophet models
                                pred = st.session_state.model_trainer.predict(model_name, current_features)
                                if pred is not None and len(pred) > 0:
                                    model_forecast.append(pred[0])
                                    # This is a simplified approach - in practice, you'd update features
                                else:
                                    break
                            
                            if len(model_forecast) > 0:
                                forecasts[model_name] = model_forecast
                
                if forecasts:
                    # Display forecast results
                    st.markdown("### 📊 Forecast Results")
                    
                    # Create forecast chart
                    forecast_fig = create_forecast_chart(
                        st.session_state.processed_data.tail(60), 
                        forecasts, 
                        forecast_days
                    )
                    st.plotly_chart(forecast_fig, use_container_width=True)
                    
                    # Forecast statistics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### Forecast Summary")
                        for model_name, forecast_values in forecasts.items():
                            if len(forecast_values) > 0:
                                final_price = forecast_values[-1]
                                total_change = ((final_price / current_price) - 1) * 100
                                st.metric(
                                    f"{model_name} ({len(forecast_values)} days)",
                                    f"${final_price:.2f}",
                                    f"{total_change:+.2f}%"
                                )
                    
                    with col2:
                        st.markdown("#### Price Targets")
                        if len(forecasts) > 1:
                            all_values = []
                            for values in forecasts.values():
                                all_values.extend(values)
                            
                            if all_values:
                                st.metric("Highest Target", f"${max(all_values):.2f}")
                                st.metric("Lowest Target", f"${min(all_values):.2f}")
                                st.metric("Average Target", f"${np.mean(all_values):.2f}")
                    
                    with col3:
                        st.markdown("#### Risk Metrics")
                        if len(forecasts) > 1:
                            final_predictions = [f[-1] for f in forecasts.values() if len(f) > 0]
                            if len(final_predictions) > 1:
                                prediction_std = np.std(final_predictions)
                                prediction_range = max(final_predictions) - min(final_predictions)
                                
                                st.metric("Prediction Std Dev", f"${prediction_std:.2f}")
                                st.metric("Prediction Range", f"${prediction_range:.2f}")
                                st.metric("Uncertainty", f"{(prediction_std/current_price)*100:.1f}%")
                    
                    # Download forecast report
                    st.markdown("### 💾 Download Forecast Report")
                    
                    # Create forecast report
                    last_date = st.session_state.processed_data['Date'].iloc[-1]
                    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=forecast_days)
                    
                    forecast_report_data = {'Date': future_dates.strftime('%Y-%m-%d')}
                    
                    for model_name, forecast_values in forecasts.items():
                        if len(forecast_values) > 0:
                            # Pad with None if forecast is shorter
                            padded_forecast = list(forecast_values) + [None] * (forecast_days - len(forecast_values))
                            forecast_report_data[f'{model_name}_Forecast'] = padded_forecast[:forecast_days]
                    
                    forecast_report_df = pd.DataFrame(forecast_report_data)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv = forecast_report_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Forecast CSV",
                            data=csv,
                            file_name=f"bitcoin_forecast_{forecast_days}days_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                    with col2:
                        # Generate PDF forecast report
                        pdf_buffer = create_forecast_pdf(forecasts, current_price, forecast_days)
                        st.download_button(
                            label="📄 Download Forecast PDF",
                            data=pdf_buffer,
                            file_name=f"bitcoin_forecast_{forecast_days}days_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                
                else:
                    st.warning("No forecast data generated. Please check your models.")
                
            except Exception as e:
                st.error(f"Error generating forecast: {str(e)}")

elif prediction_type == "Historical Backtest":
    st.markdown("## 📈 Historical Backtest Analysis")
    
    backtest_days = st.sidebar.slider("Backtest Period (days)", 30, 200, 60)
    
    if st.button("🔄 Run Backtest", type="primary"):
        with st.spinner("Running historical backtest..."):
            try:
                # Prepare data for backtesting
                X, y, feature_names = create_features_target(
                    st.session_state.processed_data, 
                    target_column='Close', 
                    forecast_days=1
                )
                
                if len(X) < backtest_days:
                    st.warning(f"Not enough data for {backtest_days}-day backtest. Using {len(X)} days.")
                    backtest_days = len(X)
                
                # Use last backtest_days for backtesting
                X_backtest = X[-backtest_days:]
                y_backtest = y[-backtest_days:]
                dates_backtest = st.session_state.processed_data['Date'].iloc[-(backtest_days+1):-1]
                
                backtest_results = {}
                
                for model_name in selected_models:
                    if model_name != 'Prophet':  # Prophet needs different handling
                        predictions = st.session_state.model_trainer.predict(model_name, X_backtest)
                        
                        if predictions is not None and len(predictions) > 0:
                            # Handle LSTM predictions alignment
                            if model_name == 'LSTM' and len(predictions) != len(y_backtest):
                                y_aligned = y_backtest[-len(predictions):]
                                dates_aligned = dates_backtest[-len(predictions):]
                            else:
                                y_aligned = y_backtest
                                dates_aligned = dates_backtest
                                
                            if len(predictions) == len(y_aligned):
                                backtest_results[model_name] = {
                                    'predictions': predictions,
                                    'actual': y_aligned,
                                    'dates': dates_aligned
                                }
                
                if backtest_results:
                    # Display backtest results
                    st.markdown("### 📊 Backtest Performance")
                    
                    # Performance metrics
                    performance_data = []
                    
                    for model_name, results in backtest_results.items():
                        y_true = results['actual']
                        y_pred = results['predictions']
                        
                        mae = mean_absolute_error(y_true, y_pred)
                        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
                        r2 = r2_score(y_true, y_pred)
                        
                        # Calculate directional accuracy
                        actual_direction = np.diff(y_true) > 0
                        pred_direction = np.diff(y_pred) > 0
                        directional_accuracy = np.mean(actual_direction == pred_direction) * 100
                        
                        performance_data.append({
                            'Model': model_name,
                            'MAE': mae,
                            'RMSE': rmse,
                            'R² Score': r2,
                            'Directional Accuracy': f"{directional_accuracy:.1f}%"
                        })
                    
                    performance_df = pd.DataFrame(performance_data)
                    st.dataframe(performance_df.round(4))
                    
                    # Visualization
                    st.markdown("### 📊 Backtest Visualization")
                    
                    fig = go.Figure()
                    
                    # Plot results for each model
                    colors = ['red', 'blue', 'green', 'purple', 'orange']
                    
                    for i, (model_name, results) in enumerate(backtest_results.items()):
                        # Actual prices
                        if i == 0:  # Only plot actual once
                            fig.add_trace(go.Scatter(
                                x=results['dates'],
                                y=results['actual'],
                                name='Actual Price',
                                line=dict(color='black', width=2)
                            ))
                        
                        # Predicted prices
                        fig.add_trace(go.Scatter(
                            x=results['dates'],
                            y=results['predictions'],
                            name=f'{model_name} Predictions',
                            line=dict(color=colors[i % len(colors)], dash='dash')
                        ))
                    
                    fig.update_layout(
                        title=f"Historical Backtest - Last {backtest_days} Days",
                        xaxis_title="Date",
                        yaxis_title="Price (USD)",
                        height=600,
                        legend=dict(x=0, y=1)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Error analysis
                    st.markdown("### 🔍 Error Analysis")
                    
                    selected_model_analysis = st.selectbox(
                        "Select model for detailed error analysis",
                        options=list(backtest_results.keys())
                    )
                    
                    if selected_model_analysis:
                        results = backtest_results[selected_model_analysis]
                        errors = results['actual'] - results['predictions']
                        error_pct = (errors / results['actual']) * 100
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Error distribution
                            fig_error = px.histogram(
                                x=error_pct,
                                nbins=30,
                                title=f"{selected_model_analysis} - Error Distribution (%)",
                                labels={'x': 'Percentage Error', 'y': 'Frequency'}
                            )
                            st.plotly_chart(fig_error, use_container_width=True)
                        
                        with col2:
                            # Error over time
                            fig_error_time = px.line(
                                x=results['dates'],
                                y=error_pct,
                                title=f"{selected_model_analysis} - Error Over Time",
                                labels={'x': 'Date', 'y': 'Percentage Error (%)'}
                            )
                            st.plotly_chart(fig_error_time, use_container_width=True)
                        
                        # Error statistics
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Mean Error", f"{np.mean(errors):.2f}")
                        
                        with col2:
                            st.metric("Mean Abs Error", f"{np.mean(np.abs(errors)):.2f}")
                        
                        with col3:
                            st.metric("Error Std Dev", f"{np.std(errors):.2f}")
                        
                        with col4:
                            st.metric("Max Error", f"{np.max(np.abs(errors)):.2f}")
                    
                    # Download backtest report
                    st.markdown("### 💾 Download Backtest Report")
                    
                    # Create comprehensive backtest report
                    backtest_report_data = []
                    
                    for model_name, results in backtest_results.items():
                        for i, (date, actual, pred) in enumerate(zip(results['dates'], results['actual'], results['predictions'])):
                            backtest_report_data.append({
                                'Date': date.strftime('%Y-%m-%d'),
                                'Model': model_name,
                                'Actual_Price': actual,
                                'Predicted_Price': pred,
                                'Error': actual - pred,
                                'Error_Pct': ((actual - pred) / actual) * 100
                            })
                    
                    backtest_report_df = pd.DataFrame(backtest_report_data)
                    
                    csv = backtest_report_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Backtest CSV",
                        data=csv,
                        file_name=f"bitcoin_backtest_{backtest_days}days_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                
                else:
                    st.warning("No backtest results generated. Please check your models.")
                
            except Exception as e:
                st.error(f"Error running backtest: {str(e)}")

# Trading strategy simulation (bonus feature)
st.markdown("## 💰 Simple Trading Strategy Simulation")

if st.checkbox("Run Trading Strategy Simulation"):
    st.markdown("### 📊 Strategy: Buy when predicted price > current price")
    
    if hasattr(st.session_state, 'training_results'):
        strategy_model = st.selectbox(
            "Select model for strategy",
            options=available_models
        )
        
        initial_capital = st.number_input("Initial Capital ($)", value=10000, min_value=1000)
        
        if st.button("🚀 Run Strategy Simulation"):
            try:
                # Simple buy/hold strategy based on predictions
                st.info("This is a simplified simulation for educational purposes only!")
                
                # Use backtest data if available
                if 'backtest_results' in locals() and strategy_model in backtest_results:
                    results = backtest_results[strategy_model]
                    
                    # Simple strategy: buy when predicted price > current, sell when < current
                    capital = initial_capital
                    position = 0  # BTC position
                    trades = []
                    
                    for i in range(1, len(results['predictions'])):
                        current_price = results['actual'][i-1]
                        predicted_price = results['predictions'][i]
                        actual_next_price = results['actual'][i]
                        
                        if predicted_price > current_price and position == 0:
                            # Buy signal
                            position = capital / current_price
                            capital = 0
                            trades.append(('BUY', current_price, results['dates'][i-1]))
                        
                        elif predicted_price < current_price and position > 0:
                            # Sell signal
                            capital = position * current_price
                            position = 0
                            trades.append(('SELL', current_price, results['dates'][i-1]))
                    
                    # Close position at end
                    if position > 0:
                        final_price = results['actual'][-1]
                        capital = position * final_price
                        position = 0
                        trades.append(('SELL', final_price, results['dates'][-1]))
                    
                    # Calculate returns
                    total_return = ((capital / initial_capital) - 1) * 100
                    
                    # Buy and hold comparison
                    buy_hold_return = ((results['actual'][-1] / results['actual'][0]) - 1) * 100
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Strategy Return", f"{total_return:.2f}%")
                    
                    with col2:
                        st.metric("Buy & Hold Return", f"{buy_hold_return:.2f}%")
                    
                    with col3:
                        st.metric("Number of Trades", len(trades))
                    
                    # Show trades
                    if trades:
                        st.markdown("### 📋 Trade History")
                        trades_df = pd.DataFrame(trades, columns=['Action', 'Price', 'Date'])
                        st.dataframe(trades_df)
                
            except Exception as e:
                st.error(f"Error running strategy simulation: {str(e)}")
