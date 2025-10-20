import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

def create_overview_charts(df):
    """Create overview charts for the dataset"""
    
    charts = {}
    
    # Default rate by region
    if 'federal_district_nm' in df.columns and 'bad_flag' in df.columns:
        region_stats = df.groupby('federal_district_nm').agg({
            'bad_flag': ['count', 'sum', 'mean']
        }).round(3)
        region_stats.columns = ['Total_Loans', 'Defaults', 'Default_Rate']
        region_stats = region_stats.reset_index()
        region_stats['Default_Rate_Pct'] = region_stats['Default_Rate'] * 100
        
        charts['region_default'] = px.bar(
            region_stats.sort_values('Default_Rate_Pct', ascending=False),
            x='federal_district_nm',
            y='Default_Rate_Pct',
            title='Default Rate by Federal District',
            labels={'Default_Rate_Pct': 'Default Rate (%)', 'federal_district_nm': 'Federal District'}
        )
        charts['region_default'].update_layout(xaxis_tickangle=-45)
    
    # Age distribution
    if 'age' in df.columns:
        charts['age_dist'] = px.histogram(
            df,
            x='age',
            nbins=30,
            title='Age Distribution of Loan Applicants',
            labels={'age': 'Age', 'count': 'Number of Loans'}
        )
    
    # Payment type analysis
    payment_cols = [col for col in df.columns if col.startswith('payment_type_')]
    if payment_cols:
        payment_data = []
        for col in payment_cols:
            payment_data.append({
                'Payment_Type': col,
                'Total_Count': df[col].sum(),
                'Avg_per_Loan': df[col].mean()
            })
        
        payment_df = pd.DataFrame(payment_data)
        charts['payment_types'] = px.bar(
            payment_df,
            x='Payment_Type',
            y='Total_Count',
            title='Distribution of Payment Types'
        )
    
    return charts

def create_correlation_heatmap(df, figsize=(12, 10)):
    """Create correlation heatmap"""
    # Select numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    corr_matrix = df[numerical_cols].corr()
    
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Correlation Matrix of Numerical Features",
        color_continuous_scale='RdBu'
    )
    
    return fig

def create_default_analysis_charts(df):
    """Create charts for default analysis"""
    charts = {}
    
    if 'bad_flag' not in df.columns:
        return charts
    
    # Default rate over time
    if 'rep_loan_date' in df.columns:
        df['loan_month'] = pd.to_datetime(df['rep_loan_date']).dt.to_period('M')
        monthly_defaults = df.groupby('loan_month').agg({
            'bad_flag': ['count', 'sum', 'mean']
        }).round(3)
        monthly_defaults.columns = ['Total_Loans', 'Defaults', 'Default_Rate']
        monthly_defaults = monthly_defaults.reset_index()
        monthly_defaults['loan_month'] = monthly_defaults['loan_month'].astype(str)
        monthly_defaults['Default_Rate_Pct'] = monthly_defaults['Default_Rate'] * 100
        
        charts['monthly_defaults'] = px.line(
            monthly_defaults,
            x='loan_month',
            y='Default_Rate_Pct',
            title='Default Rate Trend Over Time',
            labels={'Default_Rate_Pct': 'Default Rate (%)', 'loan_month': 'Month'}
        )
        charts['monthly_defaults'].update_layout(xaxis_tickangle=-45)
    
    # Default by gender
    if 'gender' in df.columns:
        gender_defaults = df.groupby('gender').agg({
            'bad_flag': ['count', 'sum', 'mean']
        }).round(3)
        gender_defaults.columns = ['Total_Loans', 'Defaults', 'Default_Rate']
        gender_defaults = gender_defaults.reset_index()
        gender_defaults['Default_Rate_Pct'] = gender_defaults['Default_Rate'] * 100
        
        charts['gender_defaults'] = px.bar(
            gender_defaults,
            x='gender',
            y='Default_Rate_Pct',
            title='Default Rate by Gender',
            labels={'Default_Rate_Pct': 'Default Rate (%)', 'gender': 'Gender'}
        )
    
    # Score distribution by default status
    score_cols = [col for col in df.columns if col.startswith('score_')]
    if score_cols:
        for score_col in score_cols:
            if df[score_col].notna().sum() > 0:
                charts[f'{score_col}_dist'] = px.histogram(
                    df,
                    x=score_col,
                    color='bad_flag',
                    title=f'{score_col} Distribution by Default Status',
                    barmode='overlay',
                    opacity=0.7
                )
    
    return charts

def create_risk_segmentation_chart(df):
    """Create risk segmentation analysis"""
    if 'bad_flag' not in df.columns:
        return None
    
    # Create risk score
    risk_cols = ['dpd_5_cnt', 'dpd_15_cnt', 'dpd_30_cnt']
    existing_risk_cols = [col for col in risk_cols if col in df.columns]
    
    if not existing_risk_cols:
        return None
    
    df_risk = df.copy()
    df_risk['risk_score'] = df_risk[existing_risk_cols].fillna(0).sum(axis=1)
    
    # Create risk segments
    df_risk['risk_segment'] = pd.cut(
        df_risk['risk_score'],
        bins=[-1, 0, 1, 3, np.inf],
        labels=['Low Risk', 'Medium Risk', 'High Risk', 'Very High Risk']
    )
    
    # Calculate default rates by risk segment
    risk_analysis = df_risk.groupby('risk_segment').agg({
        'bad_flag': ['count', 'sum', 'mean']
    }).round(3)
    risk_analysis.columns = ['Total_Loans', 'Defaults', 'Default_Rate']
    risk_analysis = risk_analysis.reset_index()
    risk_analysis['Default_Rate_Pct'] = risk_analysis['Default_Rate'] * 100
    
    fig = px.bar(
        risk_analysis,
        x='risk_segment',
        y='Default_Rate_Pct',
        title='Default Rate by Risk Segment',
        labels={'Default_Rate_Pct': 'Default Rate (%)', 'risk_segment': 'Risk Segment'},
        color='Default_Rate_Pct',
        color_continuous_scale='Reds'
    )
    
    return fig

def create_payment_analysis_charts(df):
    """Create payment behavior analysis charts"""
    charts = {}
    
    payment_cols = [col for col in df.columns if col.startswith('payment_type_')]
    
    if not payment_cols or 'bad_flag' not in df.columns:
        return charts
    
    # Payment diversity analysis
    df_payment = df.copy()
    df_payment['payment_diversity'] = (df_payment[payment_cols] > 0).sum(axis=1)
    df_payment['total_payments'] = df_payment[payment_cols].sum(axis=1)
    
    # Default rate by payment diversity
    diversity_analysis = df_payment.groupby('payment_diversity').agg({
        'bad_flag': ['count', 'sum', 'mean']
    }).round(3)
    diversity_analysis.columns = ['Total_Loans', 'Defaults', 'Default_Rate']
    diversity_analysis = diversity_analysis.reset_index()
    diversity_analysis['Default_Rate_Pct'] = diversity_analysis['Default_Rate'] * 100
    
    charts['payment_diversity'] = px.bar(
        diversity_analysis,
        x='payment_diversity',
        y='Default_Rate_Pct',
        title='Default Rate by Payment Diversity',
        labels={'Default_Rate_Pct': 'Default Rate (%)', 'payment_diversity': 'Number of Payment Types Used'}
    )
    
    # Payment volume vs default
    if df_payment['total_payments'].max() > 0:
        charts['payment_volume'] = px.scatter(
            df_payment.sample(min(1000, len(df_payment))),  # Sample for performance
            x='total_payments',
            y='bad_flag',
            title='Payment Volume vs Default Status',
            labels={'total_payments': 'Total Payments', 'bad_flag': 'Default Status'},
            opacity=0.6
        )
    
    return charts

def create_trader_analysis(df):
    """Analyze trader performance"""
    if 'TraderKey' not in df.columns or 'bad_flag' not in df.columns:
        return None
    
    trader_analysis = df.groupby('TraderKey').agg({
        'bad_flag': ['count', 'sum', 'mean']
    }).round(3)
    trader_analysis.columns = ['Total_Loans', 'Defaults', 'Default_Rate']
    trader_analysis = trader_analysis.reset_index()
    trader_analysis['Default_Rate_Pct'] = trader_analysis['Default_Rate'] * 100
    
    # Filter traders with significant volume
    significant_traders = trader_analysis[trader_analysis['Total_Loans'] >= 10]
    
    if len(significant_traders) == 0:
        return None
    
    fig = px.scatter(
        significant_traders,
        x='Total_Loans',
        y='Default_Rate_Pct',
        size='Defaults',
        hover_data=['TraderKey'],
        title='Trader Performance: Loan Volume vs Default Rate',
        labels={'Total_Loans': 'Total Loans', 'Default_Rate_Pct': 'Default Rate (%)'}
    )
    
    return fig
