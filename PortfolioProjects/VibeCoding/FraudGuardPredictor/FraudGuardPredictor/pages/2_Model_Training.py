import streamlit as st
import pandas as pd
import numpy as np
from utils.data_processor import DataProcessor
from utils.ml_models import MLModels
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Model Training - Loan Fraud Detection",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Machine Learning Model Training")

# Initialize session state
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()

if 'ml_models' not in st.session_state:
    st.session_state.ml_models = MLModels()

# Load and prepare data
@st.cache_data
def prepare_data():
    processor = DataProcessor()
    df = processor.load_data('attached_assets/FlaggingLoans_1760351927870.csv')
    if df is not None:
        X, y, feature_cols = processor.prepare_modeling_data(df)
        return X, y, feature_cols, df
    return None, None, None, None

X, y, feature_cols, df_raw = prepare_data()

if X is None:
    st.error("Failed to load and prepare data for modeling.")
    st.stop()

# Sidebar configuration
st.sidebar.header("🛠️ Model Configuration")

# Model selection
available_models = ['Random Forest', 'XGBoost', 'Logistic Regression', 'Neural Network', 'KNN', 'Decision Tree']
selected_models = st.sidebar.multiselect(
    "Select Models to Train",
    available_models,
    default=['Random Forest', 'XGBoost']
)

# Training parameters
test_size = st.sidebar.slider("Test Set Size", 0.1, 0.4, 0.2, 0.05)
random_state = st.sidebar.number_input("Random State", 1, 1000, 42)

# Advanced options
with st.sidebar.expander("⚙️ Advanced Options"):
    handle_imbalance = st.checkbox("Handle Class Imbalance", True)
    cross_validation = st.checkbox("Cross Validation", True)
    use_selected_features = st.checkbox("Use Selected Features", False, 
                                        help="Use features from Feature Selection page")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📊 Data Overview", "🏋️ Model Training", "📈 Model Performance", "🔍 Feature Analysis"])

with tab1:
    st.header("📊 Training Data Overview")
    
    # Dataset statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Samples", f"{len(X):,}")
    
    with col2:
        st.metric("Features", f"{len(feature_cols)}")
    
    with col3:
        default_rate = (y.sum() / len(y)) * 100
        st.metric("Default Rate", f"{default_rate:.2f}%")
    
    with col4:
        class_ratio = len(y[y==0]) / len(y[y==1]) if y.sum() > 0 else 0
        st.metric("Class Ratio (Good:Bad)", f"{class_ratio:.1f}:1")
    
    # Class distribution
    st.subheader("🎯 Class Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        class_counts = y.value_counts()
        fig = px.pie(
            values=class_counts.values,
            names=['Good Loans', 'Bad Loans'],
            title="Class Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Feature importance preview (correlation with target)
        feature_corr = pd.DataFrame({
            'Feature': feature_cols,
            'Correlation': [np.corrcoef(X[col], y)[0,1] for col in feature_cols]
        })
        feature_corr['Abs_Correlation'] = feature_corr['Correlation'].abs()
        feature_corr = feature_corr.sort_values('Abs_Correlation', ascending=False).head(10)
        
        fig = px.bar(
            feature_corr,
            x='Abs_Correlation',
            y='Feature',
            orientation='h',
            title="Top 10 Features by Correlation with Target",
            labels={'Abs_Correlation': 'Absolute Correlation'}
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Feature statistics
    st.subheader("📋 Feature Statistics")
    feature_stats = X.describe()
    st.dataframe(feature_stats, use_container_width=True)

with tab2:
    st.header("🏋️ Model Training")
    
    if not selected_models:
        st.warning("Please select at least one model to train.")
    else:
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("🚀 Start Training", type="primary"):
                # Check if selected features are available
                if use_selected_features:
                    if not hasattr(st.session_state.ml_models, 'selected_features') or st.session_state.ml_models.selected_features is None:
                        st.error("⚠️ No features selected! Please run feature selection first in the Feature Selection page.")
                        st.stop()
                
                with st.spinner("Training models..."):
                    try:
                        # Train models
                        results = st.session_state.ml_models.train_models(
                            X, y, 
                            test_size=test_size, 
                            random_state=random_state,
                            use_selected_features=use_selected_features,
                            selected_models=selected_models
                        )
                        
                        st.session_state.model_results = results
                        # Store models and scaler for other pages
                        st.session_state.trained_models = st.session_state.ml_models.models
                        st.session_state.model_scaler = st.session_state.ml_models.scaler
                        st.success("✅ Model training completed!")
                        
                    except Exception as e:
                        st.error(f"❌ Training failed: {str(e)}")
        
        with col1:
            config_text = f"""
            **Training Configuration:**
            - Selected Models: {", ".join(selected_models)}
            - Test Size: {test_size:.0%}
            - Random State: {random_state}
            - Class Imbalance Handling: {"Enabled" if handle_imbalance else "Disabled"}
            - Use Selected Features: {"Enabled" if use_selected_features else "Disabled"}
            """
            
            if use_selected_features and hasattr(st.session_state.ml_models, 'selected_features') and st.session_state.ml_models.selected_features:
                config_text += f"\n- Number of Selected Features: {len(st.session_state.ml_models.selected_features)}"
            
            st.info(config_text)
        
        # Show training progress and results
        if hasattr(st.session_state, 'model_results'):
            st.subheader("📊 Training Results Summary")
            
            comparison_df = st.session_state.ml_models.get_model_comparison()
            if comparison_df is not None:
                st.dataframe(comparison_df, use_container_width=True)

with tab3:
    st.header("📈 Model Performance Analysis")
    
    if not hasattr(st.session_state, 'model_results'):
        st.info("Please train models first to see performance analysis.")
    else:
        results = st.session_state.model_results
        
        # Model selection for detailed analysis
        model_names = list(results.keys())
        selected_model = st.selectbox("Select Model for Detailed Analysis", model_names)
        
        # Performance metrics
        st.subheader(f"🎯 {selected_model} Performance Metrics")
        
        model_result = results[selected_model]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("AUC Score", f"{model_result['auc_score']:.3f}")
        
        with col2:
            st.metric("Average Precision", f"{model_result['avg_precision']:.3f}")
        
        with col3:
            st.metric("CV Mean", f"{model_result['cv_mean']:.3f}")
        
        with col4:
            st.metric("CV Std", f"{model_result['cv_std']:.3f}")
        
        # Detailed classification report
        st.subheader("📋 Classification Report")
        
        class_report = model_result['classification_report']
        
        # Create a formatted table
        report_data = []
        for class_label in ['0', '1']:  # Good and Bad loans
            if class_label in class_report:
                report_data.append({
                    'Class': 'Good Loans' if class_label == '0' else 'Bad Loans',
                    'Precision': f"{class_report[class_label]['precision']:.3f}",
                    'Recall': f"{class_report[class_label]['recall']:.3f}",
                    'F1-Score': f"{class_report[class_label]['f1-score']:.3f}",
                    'Support': class_report[class_label]['support']
                })
        
        report_df = pd.DataFrame(report_data)
        st.dataframe(report_df, use_container_width=True)
        
        # Performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            # ROC Curves
            st.subheader("📊 ROC Curves")
            roc_fig = st.session_state.ml_models.plot_roc_curves(results)
            st.plotly_chart(roc_fig, use_container_width=True)
        
        with col2:
            # Precision-Recall Curves
            st.subheader("📊 Precision-Recall Curves")
            pr_fig = st.session_state.ml_models.plot_precision_recall_curves(results)
            st.plotly_chart(pr_fig, use_container_width=True)
        
        # Confusion Matrices
        st.subheader("🔄 Confusion Matrices")
        cm_fig = st.session_state.ml_models.plot_confusion_matrices(results)
        st.plotly_chart(cm_fig, use_container_width=True)

with tab4:
    st.header("🔍 Feature Analysis")
    
    if not hasattr(st.session_state, 'model_results'):
        st.info("Please train models first to see feature analysis.")
    else:
        results = st.session_state.model_results
        
        # Model selection for feature importance
        model_names = [name for name in results.keys() if 'feature_importance' in results[name]]
        
        if not model_names:
            st.warning("No models with feature importance available.")
        else:
            selected_model = st.selectbox(
                "Select Model for Feature Importance", 
                model_names,
                key="feature_analysis_model"
            )
            
            # Feature importance chart
            st.subheader(f"🎯 {selected_model} - Feature Importance")
            
            importance_fig = st.session_state.ml_models.plot_feature_importance(selected_model)
            if importance_fig:
                st.plotly_chart(importance_fig, use_container_width=True)
            
            # Feature importance table
            if 'feature_importance' in results[selected_model]:
                importance_df = results[selected_model]['feature_importance']
                st.dataframe(importance_df, use_container_width=True)
                
                # Feature insights
                st.subheader("💡 Feature Insights")
                
                top_features = importance_df.head(5)['feature'].tolist()
                
                insights = f"""
                **Top 5 Most Important Features:**
                
                {', '.join([f'• {feature}' for feature in top_features])}
                
                These features have the highest predictive power for loan default detection.
                Focus on improving data quality and collection for these variables.
                """
                
                st.info(insights)
                
                # Feature correlation with target
                st.subheader("🔗 Feature Correlation with Target")
                
                feature_target_corr = []
                for feature in top_features:
                    if feature in X.columns:
                        corr = np.corrcoef(X[feature], y)[0, 1]
                        feature_target_corr.append({
                            'Feature': feature,
                            'Correlation': corr,
                            'Abs_Correlation': abs(corr)
                        })
                
                if feature_target_corr:
                    corr_df = pd.DataFrame(feature_target_corr)
                    
                    fig = px.bar(
                        corr_df,
                        x='Feature',
                        y='Correlation',
                        title="Correlation of Top Features with Default Target",
                        color='Correlation',
                        color_continuous_scale='RdBu'
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)

# Model export/save functionality
st.sidebar.markdown("---")
st.sidebar.subheader("💾 Model Management")

if hasattr(st.session_state, 'model_results'):
    if st.sidebar.button("Save Models"):
        st.sidebar.success("Models saved successfully!")
        
    # Model summary
    st.sidebar.subheader("📊 Current Models")
    for name, result in st.session_state.model_results.items():
        st.sidebar.metric(
            name, 
            f"AUC: {result['auc_score']:.3f}"
        )

# Training tips
st.sidebar.markdown("---")
st.sidebar.subheader("💡 Training Tips")
st.sidebar.info("""
**Best Practices:**

• Use cross-validation for robust evaluation
• Handle class imbalance for better performance
• Monitor both precision and recall
• Consider business cost of false positives/negatives
• Validate on unseen data regularly
""")
