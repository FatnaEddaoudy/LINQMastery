import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from utils.data_processor import DataProcessor
from utils.visualizations import create_overview_charts
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Loan Fraud Detection System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Flat Design CSS
st.markdown("""
<style>
    /* Main Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 3rem;
        color: #2C3E50;
        letter-spacing: -0.5px;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 3rem;
        margin-bottom: 1.5rem;
        color: #2E86DE;
        border-left: 4px solid #2E86DE;
        padding-left: 1rem;
    }
    
    /* Cards */
    .metric-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #E1E8ED;
        margin: 1rem 0;
    }
    
    /* Clean metrics */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E1E8ED;
        padding: 1rem;
        border-radius: 8px;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 8px;
        border: none;
    }
    
    /* Remove extra spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🏦 Loan Fraud Detection System</h1>', unsafe_allow_html=True)
    
    # Initialize data processor
    if 'data_processor' not in st.session_state:
        st.session_state.data_processor = DataProcessor()
    
    # Load data
    try:
        df = st.session_state.data_processor.load_data('attached_assets/FlaggingLoans_1760351927870.csv')
        
        if df is None:
            st.error("Failed to load data. Please check the file path.")
            return
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.sidebar.markdown("---")
    
    # Main overview section
    st.markdown('<h2 class="section-header">📊 Dataset Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Loans", f"{len(df):,}")
    
    with col2:
        default_rate = (df['bad_flag'].sum() / len(df)) * 100
        st.metric("Default Rate", f"{default_rate:.2f}%")
    
    with col3:
        st.metric("Total Features", f"{len(df.columns)}")
    
    with col4:
        missing_percentage = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        st.metric("Missing Data", f"{missing_percentage:.2f}%")
    
    # Key insights
    st.markdown('<h2 class="section-header">🔍 Key Insights</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Default Rate by Region")
        region_default = df.groupby('federal_district_nm')['bad_flag'].agg(['count', 'sum']).reset_index()
        region_default['default_rate'] = (region_default['sum'] / region_default['count']) * 100
        region_default = region_default.sort_values('default_rate', ascending=False)
        
        fig = px.bar(
            region_default.head(10), 
            x='federal_district_nm', 
            y='default_rate',
            title="Default Rate by Federal District",
            labels={'default_rate': 'Default Rate (%)', 'federal_district_nm': 'Federal District'},
            color_discrete_sequence=['#2E86DE']
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='sans-serif', color='#2C3E50')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("👥 Default Rate by Age Group")
        df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 45, 55, 100], 
                                labels=['18-25', '26-35', '36-45', '46-55', '55+'])
        age_default = df.groupby('age_group')['bad_flag'].agg(['count', 'sum']).reset_index()
        age_default['default_rate'] = (age_default['sum'] / age_default['count']) * 100
        
        fig = px.bar(
            age_default, 
            x='age_group', 
            y='default_rate',
            title="Default Rate by Age Group",
            labels={'default_rate': 'Default Rate (%)', 'age_group': 'Age Group'},
            color_discrete_sequence=['#10AC84']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='sans-serif', color='#2C3E50')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Payment type analysis
    st.markdown('<h2 class="section-header">💳 Payment Type Analysis</h2>', unsafe_allow_html=True)
    
    payment_cols = ['payment_type_0', 'payment_type_1', 'payment_type_2', 'payment_type_3', 'payment_type_4', 'payment_type_5']
    payment_data = []
    
    for col in payment_cols:
        total_payments = df[col].sum()
        default_payments = df[df['bad_flag'] == 1][col].sum()
        if total_payments > 0:
            default_rate = (default_payments / total_payments) * 100
            payment_data.append({
                'Payment Type': col,
                'Total Count': total_payments,
                'Default Count': default_payments,
                'Default Rate (%)': default_rate
            })
    
    payment_df = pd.DataFrame(payment_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            payment_df, 
            x='Payment Type', 
            y='Total Count',
            title="Total Payments by Type",
            color_discrete_sequence=['#5F27CD']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='sans-serif', color='#2C3E50')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            payment_df, 
            x='Payment Type', 
            y='Default Rate (%)',
            title="Default Rate by Payment Type",
            color='Default Rate (%)',
            color_continuous_scale=['#10AC84', '#EE5A6F']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='sans-serif', color='#2C3E50')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Descriptive Analysis Section
    st.markdown('<h2 class="section-header">📋 Descriptive Analysis</h2>', unsafe_allow_html=True)
    
    with st.expander("🔍 How were loans in historical data labeled as good or risky?"):
        st.write("""
        **Loan Labeling Analysis:**
        
        Based on the dataset analysis:
        - **Good Loans**: Loans with `bad_flag = 0` representing loans that were repaid successfully
        - **Risky/Bad Loans**: Loans with `bad_flag = 1` representing loans that defaulted
        
        **Key Findings:**
        """)
        
        good_loans = len(df[df['bad_flag'] == 0])
        bad_loans = len(df[df['bad_flag'] == 1])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Good Loans", f"{good_loans:,} ({good_loans/len(df)*100:.1f}%)")
        with col2:
            st.metric("Risky Loans", f"{bad_loans:,} ({bad_loans/len(df)*100:.1f}%)")
    
    with st.expander("📊 How are loans currently categorized based on risk?"):
        st.write("""
        **Current Risk Categorization:**
        
        Loans are categorized based on multiple factors:
        """)
        
        # Risk factors analysis
        risk_factors = ['dpd_5_cnt', 'dpd_15_cnt', 'dpd_30_cnt', 'past_billings_cnt']
        
        for factor in risk_factors:
            if factor in df.columns:
                factor_analysis = df.groupby('bad_flag')[factor].agg(['mean', 'median', 'std']).round(2)
                st.write(f"**{factor}**: Higher values indicate greater risk")
                st.dataframe(factor_analysis)
    
    with st.expander("🏷️ Are there different classes or levels of flagged loans?"):
        st.write("""
        **Loan Classification Levels:**
        
        Based on the analysis, we can identify different risk levels:
        """)
        
        # Create risk levels based on multiple factors
        df_analysis = df.copy()
        
        # Calculate risk score
        risk_cols = ['dpd_5_cnt', 'dpd_15_cnt', 'dpd_30_cnt']
        df_analysis['risk_score'] = 0
        
        for col in risk_cols:
            if col in df_analysis.columns:
                df_analysis['risk_score'] += df_analysis[col].fillna(0)
        
        # Define risk levels
        df_analysis['risk_level'] = pd.cut(
            df_analysis['risk_score'], 
            bins=[-1, 0, 1, 3, np.inf], 
            labels=['Low Risk', 'Medium Risk', 'High Risk', 'Very High Risk']
        )
        
        risk_summary = df_analysis.groupby('risk_level')['bad_flag'].agg(['count', 'sum', 'mean']).round(3)
        risk_summary.columns = ['Total Loans', 'Defaults', 'Default Rate']
        st.dataframe(risk_summary)
    
    # Navigation info
    st.markdown('<h2 class="section-header">🧭 Navigation Guide</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: #FFFFFF; padding: 1.5rem; border-radius: 8px; border: 1px solid #E1E8ED; height: 100%;'>
            <h3 style='color: #2E86DE; font-size: 1.2rem; margin-bottom: 1rem;'>📊 Data Exploration</h3>
            <p style='color: #2C3E50;'>Comprehensive analysis of loan data with interactive visualizations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #FFFFFF; padding: 1.5rem; border-radius: 8px; border: 1px solid #E1E8ED; height: 100%;'>
            <h3 style='color: #10AC84; font-size: 1.2rem; margin-bottom: 1rem;'>🤖 Model Training</h3>
            <p style='color: #2C3E50;'>Build and evaluate machine learning models for fraud detection</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: #FFFFFF; padding: 1.5rem; border-radius: 8px; border: 1px solid #E1E8ED; height: 100%;'>
            <h3 style='color: #5F27CD; font-size: 1.2rem; margin-bottom: 1rem;'>🔮 Predictions</h3>
            <p style='color: #2C3E50;'>Make predictions and analyze expected default rates at different approval levels</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Dataset preview
    st.markdown('<h2 class="section-header">📄 Dataset Preview</h2>', unsafe_allow_html=True)
    st.dataframe(df.head(100), use_container_width=True)

if __name__ == "__main__":
    main()
