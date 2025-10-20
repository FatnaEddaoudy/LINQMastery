import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processor import DataProcessor
from utils.visualizations import (
    create_overview_charts, 
    create_correlation_heatmap, 
    create_default_analysis_charts,
    create_risk_segmentation_chart,
    create_payment_analysis_charts,
    create_trader_analysis
)

st.set_page_config(
    page_title="Data Exploration - Loan Fraud Detection",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Exploration & Analysis")

# Initialize session state
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()

# Load and process data
@st.cache_data
def load_and_process_data():
    processor = DataProcessor()
    df = processor.load_data('attached_assets/FlaggingLoans_1760351927870.csv')
    if df is not None:
        df_processed = processor.preprocess_data(df)
        return df, df_processed
    return None, None

df_raw, df_processed = load_and_process_data()

if df_raw is None:
    st.error("Failed to load data. Please check the file path.")
    st.stop()

# Store processed data in session state for other pages
st.session_state.data = df_processed

# Sidebar filters
st.sidebar.header("🔍 Data Filters")

# Region filter
if 'federal_district_nm' in df_raw.columns:
    regions = ['All'] + sorted(df_raw['federal_district_nm'].dropna().unique().tolist())
    selected_region = st.sidebar.selectbox("Select Region", regions)
    
    if selected_region != 'All':
        df_filtered = df_raw[df_raw['federal_district_nm'] == selected_region]
        df_processed_filtered = df_processed[df_processed['federal_district_nm'] == selected_region]
    else:
        df_filtered = df_raw.copy()
        df_processed_filtered = df_processed.copy()
else:
    df_filtered = df_raw.copy()
    df_processed_filtered = df_processed.copy()

# Age filter
if 'age' in df_filtered.columns:
    age_min, age_max = int(df_filtered['age'].min()), int(df_filtered['age'].max())
    age_range = st.sidebar.slider("Age Range", age_min, age_max, (age_min, age_max))
    df_filtered = df_filtered[(df_filtered['age'] >= age_range[0]) & (df_filtered['age'] <= age_range[1])]
    df_processed_filtered = df_processed_filtered[(df_processed_filtered['age'] >= age_range[0]) & (df_processed_filtered['age'] <= age_range[1])]

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Overview", "🔗 Correlations", "⚠️ Default Analysis", "💳 Payment Behavior", "🏢 Trader Analysis"])

with tab1:
    st.header("Dataset Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{len(df_filtered):,}")
    
    with col2:
        if 'bad_flag' in df_filtered.columns:
            default_rate = (df_filtered['bad_flag'].sum() / len(df_filtered)) * 100
            st.metric("Default Rate", f"{default_rate:.2f}%")
    
    with col3:
        st.metric("Features", f"{len(df_filtered.columns)}")
    
    with col4:
        missing_pct = (df_filtered.isnull().sum().sum() / (len(df_filtered) * len(df_filtered.columns))) * 100
        st.metric("Missing Data", f"{missing_pct:.2f}%")
    
    # Data quality assessment
    st.subheader("🔍 Data Quality Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Missing values analysis
        missing_data = df_filtered.isnull().sum()
        missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
        
        if len(missing_data) > 0:
            fig = px.bar(
                x=missing_data.values,
                y=missing_data.index,
                orientation='h',
                title="Missing Values by Feature",
                labels={'x': 'Number of Missing Values', 'y': 'Features'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("No missing values found!")
    
    with col2:
        # Data types overview
        dtype_counts = df_filtered.dtypes.value_counts()
        fig = px.pie(
            values=dtype_counts.values,
            names=[str(dt) for dt in dtype_counts.index],
            title="Data Types Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Descriptive statistics
    st.subheader("📋 Descriptive Statistics")
    
    numerical_cols = df_filtered.select_dtypes(include=[np.number]).columns
    if len(numerical_cols) > 0:
        st.dataframe(df_filtered[numerical_cols].describe(), use_container_width=True)
    
    # Feature distribution
    st.subheader("📊 Feature Distributions")
    
    if len(numerical_cols) > 0:
        selected_feature = st.selectbox("Select feature to visualize", numerical_cols)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(
                df_filtered,
                x=selected_feature,
                title=f"Distribution of {selected_feature}",
                nbins=30
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.box(
                df_filtered,
                y=selected_feature,
                title=f"Box Plot of {selected_feature}"
            )
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("🔗 Feature Correlations")
    
    numerical_cols = df_processed_filtered.select_dtypes(include=[np.number]).columns
    
    if len(numerical_cols) > 1:
        # Correlation heatmap
        corr_fig = create_correlation_heatmap(df_processed_filtered[numerical_cols])
        st.plotly_chart(corr_fig, use_container_width=True)
        
        # Top correlations with target
        if 'bad_flag' in numerical_cols:
            target_corr = df_processed_filtered[numerical_cols].corr()['bad_flag'].abs().sort_values(ascending=False)
            target_corr = target_corr.drop('bad_flag')
            
            st.subheader("🎯 Features Most Correlated with Default")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.dataframe(target_corr.head(10), use_container_width=True)
            
            with col2:
                fig = px.bar(
                    x=target_corr.head(10).values,
                    y=target_corr.head(10).index,
                    orientation='h',
                    title="Top 10 Features Correlated with Default",
                    labels={'x': 'Absolute Correlation', 'y': 'Features'}
                )
                fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("⚠️ Default Analysis")
    
    if 'bad_flag' not in df_filtered.columns:
        st.warning("Default flag column not found in the dataset.")
    else:
        # Overall default statistics
        total_loans = len(df_filtered)
        total_defaults = df_filtered['bad_flag'].sum()
        default_rate = (total_defaults / total_loans) * 100
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Loans", f"{total_loans:,}")
        with col2:
            st.metric("Total Defaults", f"{total_defaults:,}")
        with col3:
            st.metric("Default Rate", f"{default_rate:.2f}%")
        
        # Default analysis charts
        default_charts = create_default_analysis_charts(df_filtered)
        
        for chart_name, chart in default_charts.items():
            st.plotly_chart(chart, use_container_width=True)
        
        # Risk segmentation
        st.subheader("🎯 Risk Segmentation")
        risk_chart = create_risk_segmentation_chart(df_filtered)
        if risk_chart:
            st.plotly_chart(risk_chart, use_container_width=True)
        
        # Default by categorical features
        categorical_cols = ['federal_district_nm', 'gender']
        
        for col in categorical_cols:
            if col in df_filtered.columns and df_filtered[col].notna().sum() > 0:
                st.subheader(f"Default Rate by {col.replace('_', ' ').title()}")
                
                category_defaults = df_filtered.groupby(col).agg({
                    'bad_flag': ['count', 'sum', 'mean']
                }).round(3)
                category_defaults.columns = ['Total_Loans', 'Defaults', 'Default_Rate']
                category_defaults = category_defaults.reset_index()
                category_defaults['Default_Rate_Pct'] = category_defaults['Default_Rate'] * 100
                
                fig = px.bar(
                    category_defaults.sort_values('Default_Rate_Pct', ascending=False),
                    x=col,
                    y='Default_Rate_Pct',
                    title=f'Default Rate by {col.replace("_", " ").title()}',
                    labels={'Default_Rate_Pct': 'Default Rate (%)'}
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("💳 Payment Behavior Analysis")
    
    payment_charts = create_payment_analysis_charts(df_filtered)
    
    if payment_charts:
        for chart_name, chart in payment_charts.items():
            st.plotly_chart(chart, use_container_width=True)
    else:
        st.info("Payment behavior analysis not available for this dataset.")
    
    # Payment type breakdown
    payment_cols = [col for col in df_filtered.columns if col.startswith('payment_type_')]
    
    if payment_cols:
        st.subheader("💰 Payment Type Breakdown")
        
        payment_summary = []
        for col in payment_cols:
            total_payments = df_filtered[col].sum()
            avg_per_loan = df_filtered[col].mean()
            
            if 'bad_flag' in df_filtered.columns:
                default_payments = df_filtered[df_filtered['bad_flag'] == 1][col].sum()
                default_rate = (default_payments / total_payments * 100) if total_payments > 0 else 0
            else:
                default_rate = 0
            
            payment_summary.append({
                'Payment Type': col,
                'Total Payments': total_payments,
                'Avg per Loan': round(avg_per_loan, 2),
                'Default Rate (%)': round(default_rate, 2)
            })
        
        payment_df = pd.DataFrame(payment_summary)
        st.dataframe(payment_df, use_container_width=True)

with tab5:
    st.header("🏢 Trader Performance Analysis")
    
    if 'TraderKey' in df_filtered.columns:
        trader_chart = create_trader_analysis(df_filtered)
        
        if trader_chart:
            st.plotly_chart(trader_chart, use_container_width=True)
        
        # Trader summary statistics
        st.subheader("📊 Trader Summary")
        
        trader_stats = df_filtered.groupby('TraderKey').agg({
            'bad_flag': ['count', 'sum', 'mean'] if 'bad_flag' in df_filtered.columns else ['count'],
            'age': 'mean'
        }).round(3)
        
        if 'bad_flag' in df_filtered.columns:
            trader_stats.columns = ['Total_Loans', 'Defaults', 'Default_Rate', 'Avg_Age']
            trader_stats['Default_Rate_Pct'] = trader_stats['Default_Rate'] * 100
        else:
            trader_stats.columns = ['Total_Loans', 'Avg_Age']
        
        trader_stats = trader_stats.reset_index()
        
        # Filter significant traders
        significant_traders = trader_stats[trader_stats['Total_Loans'] >= 5].sort_values('Total_Loans', ascending=False)
        
        st.dataframe(significant_traders.head(20), use_container_width=True)
        
        # Top performing traders
        if 'Default_Rate_Pct' in significant_traders.columns:
            st.subheader("🏆 Best Performing Traders (Lowest Default Rate)")
            best_traders = significant_traders.nsmallest(10, 'Default_Rate_Pct')
            st.dataframe(best_traders, use_container_width=True)
            
            st.subheader("⚠️ Worst Performing Traders (Highest Default Rate)")
            worst_traders = significant_traders.nlargest(10, 'Default_Rate_Pct')
            st.dataframe(worst_traders, use_container_width=True)
    else:
        st.info("Trader information not available in this dataset.")

# Export functionality
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Export Data")

if st.sidebar.button("Download Filtered Data"):
    csv = df_filtered.to_csv(index=False)
    st.sidebar.download_button(
        label="📄 Download CSV",
        data=csv,
        file_name=f"filtered_loan_data_{selected_region}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# Data insights
st.sidebar.markdown("---")
st.sidebar.subheader("💡 Key Insights")
if 'bad_flag' in df_filtered.columns:
    insights = [
        f"Default rate: {(df_filtered['bad_flag'].sum() / len(df_filtered)) * 100:.1f}%",
        f"Total loans analyzed: {len(df_filtered):,}",
        f"Age range: {df_filtered['age'].min():.0f} - {df_filtered['age'].max():.0f} years"
    ]
    
    for insight in insights:
        st.sidebar.info(insight)
