import streamlit as st
import pandas as pd
import numpy as np
from utils.visualizations import create_model_comparison_chart
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(page_title="Model Comparison", page_icon="📋", layout="wide")

# Initialize session state
if 'training_results' not in st.session_state:
    st.session_state.training_results = {}

st.title("📋 Model Comparison Dashboard")

if not hasattr(st.session_state, 'training_results') or not st.session_state.training_results:
    st.warning("⚠️ No training results available. Please train models first!")
    st.stop()

# Get training results
training_results = st.session_state.training_results
available_models = list(training_results.keys())

st.markdown(f"## 📊 Comparing {len(available_models)} Models")

# Performance Overview
st.markdown("### 🎯 Performance Overview")

# Create comprehensive comparison dataframe
comparison_data = []
for model_name, metrics in training_results.items():
    comparison_data.append({
        'Model': model_name,
        'Training MAE': metrics['train_mae'],
        'Training RMSE': metrics['train_rmse'],
        'Training R²': metrics['train_r2'],
        'Validation MAE': metrics['val_mae'],
        'Validation RMSE': metrics['val_rmse'],
        'Validation R²': metrics['val_r2']
    })

comparison_df = pd.DataFrame(comparison_data)

# Display comparison table with highlighting
st.markdown("#### 📊 Complete Performance Metrics")

# Create a styled dataframe
styled_df = comparison_df.style.format({
    'Training MAE': '{:.4f}',
    'Training RMSE': '{:.4f}',
    'Training R²': '{:.4f}',
    'Validation MAE': '{:.4f}',
    'Validation RMSE': '{:.4f}',
    'Validation R²': '{:.4f}'
}).highlight_min(
    subset=['Training MAE', 'Training RMSE', 'Validation MAE', 'Validation RMSE'],
    color='lightgreen'
).highlight_max(
    subset=['Training R²', 'Validation R²'],
    color='lightgreen'
)

st.dataframe(styled_df, use_container_width=True)

# Best model identification
best_val_mae = comparison_df.loc[comparison_df['Validation MAE'].idxmin()]
best_val_r2 = comparison_df.loc[comparison_df['Validation R²'].idxmax()]

col1, col2, col3 = st.columns(3)

with col1:
    st.success(f"🏆 **Best MAE**: {best_val_mae['Model']}")
    st.metric("Validation MAE", f"{best_val_mae['Validation MAE']:.4f}")

with col2:
    st.success(f"🏆 **Best R²**: {best_val_r2['Model']}")
    st.metric("Validation R²", f"{best_val_r2['Validation R²']:.4f}")

with col3:
    # Overall best model (considering both MAE and R²)
    # Normalize metrics and combine
    mae_normalized = 1 - ((comparison_df['Validation MAE'] - comparison_df['Validation MAE'].min()) / 
                         (comparison_df['Validation MAE'].max() - comparison_df['Validation MAE'].min()))
    r2_normalized = (comparison_df['Validation R²'] - comparison_df['Validation R²'].min()) / (comparison_df['Validation R²'].max() - comparison_df['Validation R²'].min())
    
    combined_score = (mae_normalized + r2_normalized) / 2
    best_overall_idx = combined_score.idxmax()
    best_overall = comparison_df.iloc[best_overall_idx]
    
    st.info(f"⚡ **Overall Best**: {best_overall['Model']}")
    st.metric("Combined Score", f"{combined_score.iloc[best_overall_idx]:.3f}")

# Visualizations
st.markdown("### 📊 Performance Visualizations")

# Create comparison charts
col1, col2 = st.columns(2)

with col1:
    # MAE Comparison
    fig_mae = px.bar(
        comparison_df,
        x='Model',
        y=['Training MAE', 'Validation MAE'],
        title='Mean Absolute Error Comparison',
        barmode='group',
        color_discrete_sequence=['lightblue', 'darkblue']
    )
    fig_mae.update_layout(height=400)
    st.plotly_chart(fig_mae, use_container_width=True)

with col2:
    # R² Comparison
    fig_r2 = px.bar(
        comparison_df,
        x='Model',
        y=['Training R²', 'Validation R²'],
        title='R² Score Comparison',
        barmode='group',
        color_discrete_sequence=['lightgreen', 'darkgreen']
    )
    fig_r2.update_layout(height=400)
    st.plotly_chart(fig_r2, use_container_width=True)

# RMSE Comparison
fig_rmse = px.bar(
    comparison_df,
    x='Model',
    y=['Training RMSE', 'Validation RMSE'],
    title='Root Mean Square Error Comparison',
    barmode='group',
    color_discrete_sequence=['lightyellow', 'orange']
)
fig_rmse.update_layout(height=400)
st.plotly_chart(fig_rmse, use_container_width=True)

# Overfitting Analysis
st.markdown("### 🔍 Overfitting Analysis")

# Calculate overfitting metrics
comparison_df['MAE_Gap'] = comparison_df['Validation MAE'] - comparison_df['Training MAE']
comparison_df['RMSE_Gap'] = comparison_df['Validation RMSE'] - comparison_df['Training RMSE']
comparison_df['R²_Drop'] = comparison_df['Training R²'] - comparison_df['Validation R²']

col1, col2 = st.columns(2)

with col1:
    # Overfitting visualization
    fig_overfit = px.scatter(
        comparison_df,
        x='Training MAE',
        y='Validation MAE',
        hover_data=['Model'],
        title='Overfitting Analysis: Training vs Validation MAE',
        labels={'Training MAE': 'Training MAE', 'Validation MAE': 'Validation MAE'}
    )
    
    # Add diagonal line (perfect fit)
    min_mae = min(comparison_df['Training MAE'].min(), comparison_df['Validation MAE'].min())
    max_mae = max(comparison_df['Training MAE'].max(), comparison_df['Validation MAE'].max())
    fig_overfit.add_shape(
        type='line',
        x0=min_mae, x1=max_mae,
        y0=min_mae, y1=max_mae,
        line=dict(dash='dash', color='red'),
        name='Perfect Fit'
    )
    
    # Add model labels
    for i, row in comparison_df.iterrows():
        fig_overfit.add_annotation(
            x=row['Training MAE'],
            y=row['Validation MAE'],
            text=row['Model'],
            showarrow=True,
            arrowhead=2
        )
    
    st.plotly_chart(fig_overfit, use_container_width=True)

with col2:
    # Overfitting metrics table
    overfitting_df = comparison_df[['Model', 'MAE_Gap', 'RMSE_Gap', 'R²_Drop']].copy()
    overfitting_df = overfitting_df.style.format({
        'MAE_Gap': '{:.4f}',
        'RMSE_Gap': '{:.4f}',
        'R²_Drop': '{:.4f}'
    }).highlight_max(color='lightcoral')
    
    st.markdown("#### Overfitting Metrics")
    st.markdown("*Higher values indicate more overfitting*")
    st.dataframe(overfitting_df, use_container_width=True)

# Model Characteristics
st.markdown("### 🔧 Model Characteristics")

model_characteristics = {
    'Linear Regression': {
        'Type': 'Linear Model',
        'Complexity': 'Low',
        'Training Speed': 'Very Fast',
        'Interpretability': 'High',
        'Suitable for': 'Linear relationships, baseline'
    },
    'Random Forest': {
        'Type': 'Ensemble (Trees)',
        'Complexity': 'Medium',
        'Training Speed': 'Fast',
        'Interpretability': 'Medium',
        'Suitable for': 'Non-linear patterns, feature importance'
    },
    'XGBoost': {
        'Type': 'Gradient Boosting',
        'Complexity': 'High',
        'Training Speed': 'Medium',
        'Interpretability': 'Medium',
        'Suitable for': 'Complex patterns, competitions'
    },
    'LSTM': {
        'Type': 'Deep Learning',
        'Complexity': 'Very High',
        'Training Speed': 'Slow',
        'Interpretability': 'Low',
        'Suitable for': 'Sequential patterns, time series'
    },
    'Prophet': {
        'Type': 'Time Series',
        'Complexity': 'Medium',
        'Training Speed': 'Medium',
        'Interpretability': 'High',
        'Suitable for': 'Trend & seasonality, forecasting'
    }
}

# Create characteristics table
char_data = []
for model in available_models:
    if model in model_characteristics:
        char = model_characteristics[model].copy()
        char['Model'] = model
        char_data.append(char)

if char_data:
    char_df = pd.DataFrame(char_data)
    char_df = char_df[['Model', 'Type', 'Complexity', 'Training Speed', 'Interpretability', 'Suitable for']]
    st.dataframe(char_df, use_container_width=True)

# Performance vs Complexity Analysis
st.markdown("### ⚖️ Performance vs Complexity Trade-off")

complexity_scores = {
    'Linear Regression': 1,
    'Random Forest': 3,
    'XGBoost': 4,
    'LSTM': 5,
    'Prophet': 3
}

# Create performance vs complexity scatter plot
perf_complexity_data = []
for i, row in comparison_df.iterrows():
    model = row['Model']
    if model in complexity_scores:
        perf_complexity_data.append({
            'Model': model,
            'Complexity': complexity_scores[model],
            'Performance': row['Validation R²'],
            'Error': row['Validation MAE']
        })

if perf_complexity_data:
    perf_df = pd.DataFrame(perf_complexity_data)
    
    fig_perf_complexity = px.scatter(
        perf_df,
        x='Complexity',
        y='Performance',
        size='Error',
        hover_data=['Model'],
        title='Performance vs Model Complexity',
        labels={
            'Complexity': 'Model Complexity (1=Simple, 5=Complex)',
            'Performance': 'Validation R² Score'
        }
    )
    
    # Add model labels
    for i, row in perf_df.iterrows():
        fig_perf_complexity.add_annotation(
            x=row['Complexity'],
            y=row['Performance'],
            text=row['Model'],
            showarrow=True,
            arrowhead=2
        )
    
    st.plotly_chart(fig_perf_complexity, use_container_width=True)

# Recommendations
st.markdown("### 💡 Model Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎯 For Production Use:")
    
    # Find models with good validation performance and low overfitting
    production_candidates = comparison_df[
        (comparison_df['Validation R²'] > comparison_df['Validation R²'].quantile(0.7)) &
        (comparison_df['MAE_Gap'] < comparison_df['MAE_Gap'].quantile(0.5))
    ]['Model'].tolist()
    
    if production_candidates:
        for model in production_candidates:
            st.success(f"✅ {model}")
    else:
        st.info("Consider the model with best validation R² score")

with col2:
    st.markdown("#### 🔬 For Experimentation:")
    
    # Models with unique characteristics
    experimental_models = [model for model in available_models if model in ['LSTM', 'Prophet']]
    
    for model in experimental_models:
        if model == 'LSTM':
            st.info("🧠 LSTM: Great for capturing sequential patterns")
        elif model == 'Prophet':
            st.info("📊 Prophet: Excellent for trend analysis and interpretability")

# Export comparison results
st.markdown("### 💾 Export Results")

col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Download Comparison Report"):
        # Combine all comparison data
        full_report = comparison_df.merge(
            pd.DataFrame([{'Model': k, **v} for k, v in model_characteristics.items() if k in available_models]),
            on='Model',
            how='left'
        )
        
        csv = full_report.to_csv(index=False)
        st.download_button(
            label="Download CSV Report",
            data=csv,
            file_name="model_comparison_report.csv",
            mime="text/csv"
        )

with col2:
    if st.button("📊 Generate Summary"):
        st.markdown("#### 📋 Model Comparison Summary")
        
        summary = f"""
        **Best Performing Models:**
        - Lowest Validation MAE: {best_val_mae['Model']} ({best_val_mae['Validation MAE']:.4f})
        - Highest Validation R²: {best_val_r2['Model']} ({best_val_r2['Validation R²']:.4f})
        - Overall Best: {best_overall['Model']}
        
        **Key Insights:**
        - Total models compared: {len(available_models)}
        - Performance range (R²): {comparison_df['Validation R²'].min():.3f} to {comparison_df['Validation R²'].max():.3f}
        - Best model improvement over worst: {((comparison_df['Validation R²'].max() - comparison_df['Validation R²'].min()) / comparison_df['Validation R²'].min() * 100):.1f}%
        """
        
        st.markdown(summary)

# Final insights
st.markdown("---")
st.markdown("### 🎯 Final Insights")

insights = []

# Performance insights
best_model = comparison_df.loc[comparison_df['Validation R²'].idxmax(), 'Model']
worst_model = comparison_df.loc[comparison_df['Validation R²'].idxmin(), 'Model']

insights.append(f"📈 **{best_model}** shows the best validation performance with R² of {comparison_df['Validation R²'].max():.4f}")

# Overfitting insights
most_overfit = comparison_df.loc[comparison_df['R²_Drop'].idxmax(), 'Model']
least_overfit = comparison_df.loc[comparison_df['R²_Drop'].idxmin(), 'Model']

insights.append(f"⚠️ **{most_overfit}** shows the most overfitting (R² drop: {comparison_df.loc[comparison_df['Model'] == most_overfit, 'R²_Drop'].iloc[0]:.4f})")
insights.append(f"✅ **{least_overfit}** shows the least overfitting (R² drop: {comparison_df.loc[comparison_df['Model'] == least_overfit, 'R²_Drop'].iloc[0]:.4f})")

# Display insights
for insight in insights:
    st.markdown(insight)

st.markdown("---")
st.markdown("*Model comparison completed. Use these insights to select the best model for your Bitcoin price prediction needs.*")
