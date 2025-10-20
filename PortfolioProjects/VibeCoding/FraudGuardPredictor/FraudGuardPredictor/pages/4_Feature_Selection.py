import streamlit as st
import pandas as pd
import numpy as np
from utils.data_processor import DataProcessor
from utils.ml_models import MLModels

st.set_page_config(
    page_title="Feature Selection - Loan Fraud Detection",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Advanced Feature Selection")

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
        return X, y, feature_cols
    return None, None, None

X, y, feature_cols = prepare_data()

if X is None:
    st.error("Failed to load and prepare data for feature selection.")
    st.stop()

# Sidebar configuration
st.sidebar.header("🛠️ Feature Selection Configuration")

# Method selection
selection_method = st.sidebar.selectbox(
    "Select Feature Selection Method",
    ["RFE (Recursive Feature Elimination)", 
     "K-Best F-Statistic", 
     "K-Best Mutual Information", 
     "Random Forest Importance"],
    help="Choose the method for selecting the most important features"
)

# Map display names to method codes
method_map = {
    "RFE (Recursive Feature Elimination)": "rfe",
    "K-Best F-Statistic": "kbest_f",
    "K-Best Mutual Information": "kbest_mi",
    "Random Forest Importance": "importance"
}

selected_method = method_map[selection_method]

# Number of features to select
n_features = st.sidebar.slider(
    "Number of Features to Select",
    min_value=5,
    max_value=min(20, len(feature_cols)),
    value=10,
    help="Select how many top features to keep"
)

# Random state
random_state = st.sidebar.number_input("Random State", 1, 1000, 42)

# Main content
tab1, tab2, tab3 = st.tabs(["📊 Feature Selection Results", "📈 Comparison", "💡 Recommendations"])

with tab1:
    st.header("Feature Selection Analysis")
    
    st.info(f"""
    **Method**: {selection_method}
    
    Feature selection helps identify the most relevant features for predicting loan defaults,
    reducing model complexity and potentially improving performance.
    """)
    
    # Run feature selection button
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🚀 Run Feature Selection", type="primary"):
            with st.spinner(f"Performing {selection_method}..."):
                try:
                    result = st.session_state.ml_models.perform_feature_selection(
                        X, y, method=selected_method, n_features=n_features, random_state=random_state
                    )
                    st.session_state.feature_selection_result = result
                    st.success(f"✅ Feature selection completed! {len(result['selected_features'])} features selected.")
                except Exception as e:
                    st.error(f"❌ Feature selection failed: {str(e)}")
    
    with col1:
        st.write(f"**Current Dataset**: {len(X)} samples, {len(feature_cols)} features")
        st.write(f"**Target**: Loan Default Prediction (bad_flag)")
    
    # Display results if available
    if hasattr(st.session_state, 'feature_selection_result'):
        result = st.session_state.feature_selection_result
        
        st.subheader("🎯 Selected Features")
        
        # Display selected features
        selected_df = result['results'][result['results']['selected'] == True].copy()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.dataframe(selected_df, use_container_width=True)
        
        with col2:
            # Summary metrics
            st.metric("Selected Features", len(result['selected_features']))
            st.metric("Total Features", len(feature_cols))
            reduction_pct = (1 - len(result['selected_features']) / len(feature_cols)) * 100
            st.metric("Dimensionality Reduction", f"{reduction_pct:.1f}%")
        
        # Visualization
        st.subheader("📊 Feature Selection Visualization")
        
        fig = st.session_state.ml_models.plot_feature_selection_results(selected_method)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Full results table
        st.subheader("📋 All Features Ranked")
        st.dataframe(result['results'], use_container_width=True)

with tab2:
    st.header("📈 Method Comparison")
    
    st.info("Compare different feature selection methods to find the best approach for your data.")
    
    if st.button("🔄 Run All Methods", type="primary"):
        comparison_results = {}
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        methods = ["rfe", "kbest_f", "kbest_mi", "importance"]
        method_names = {
            "rfe": "RFE",
            "kbest_f": "K-Best F-Stat",
            "kbest_mi": "K-Best MI",
            "importance": "RF Importance"
        }
        
        for idx, method in enumerate(methods):
            status_text.text(f"Running {method_names[method]}...")
            
            try:
                result = st.session_state.ml_models.perform_feature_selection(
                    X, y, method=method, n_features=n_features, random_state=random_state
                )
                comparison_results[method] = result
            except Exception as e:
                st.warning(f"Failed to run {method_names[method]}: {str(e)}")
            
            progress_bar.progress((idx + 1) / len(methods))
        
        status_text.text("Comparison complete!")
        st.session_state.comparison_results = comparison_results
    
    # Display comparison if available
    if hasattr(st.session_state, 'comparison_results'):
        st.subheader("🎯 Selected Features by Method")
        
        # Create comparison table
        all_features = set()
        for method, result in st.session_state.comparison_results.items():
            all_features.update(result['selected_features'])
        
        comparison_df = pd.DataFrame(index=sorted(all_features))
        
        for method, result in st.session_state.comparison_results.items():
            method_name = {
                "rfe": "RFE",
                "kbest_f": "K-Best F",
                "kbest_mi": "K-Best MI",
                "importance": "RF Importance"
            }[method]
            
            comparison_df[method_name] = comparison_df.index.isin(result['selected_features'])
        
        # Add count column
        comparison_df['Selection Count'] = comparison_df.sum(axis=1)
        comparison_df = comparison_df.sort_values('Selection Count', ascending=False)
        
        # Display
        st.dataframe(comparison_df, use_container_width=True)
        
        # Consensus features
        st.subheader("🏆 Consensus Features")
        
        consensus_threshold = st.slider("Minimum methods agreeing", 1, 4, 3)
        consensus_features = comparison_df[comparison_df['Selection Count'] >= consensus_threshold].index.tolist()
        
        st.write(f"**{len(consensus_features)} features** selected by at least {consensus_threshold} methods:")
        st.write(", ".join(consensus_features))

with tab3:
    st.header("💡 Feature Selection Recommendations")
    
    st.markdown("""
    ### When to Use Each Method
    
    #### 🔄 RFE (Recursive Feature Elimination)
    - **Best for**: Finding the optimal subset of features
    - **Advantages**: Considers feature interactions, model-based
    - **Disadvantages**: Computationally expensive
    - **Use when**: You have time and want thorough feature selection
    
    #### 📊 K-Best F-Statistic
    - **Best for**: Quick feature selection with linear relationships
    - **Advantages**: Fast, interpretable, works well for linear models
    - **Disadvantages**: Assumes linear relationships
    - **Use when**: Features have linear relationships with target
    
    #### 🔗 K-Best Mutual Information
    - **Best for**: Capturing non-linear relationships
    - **Advantages**: Detects any relationship type, robust
    - **Disadvantages**: Slower than F-statistic
    - **Use when**: Relationships are complex or non-linear
    
    #### 🌲 Random Forest Importance
    - **Best for**: Tree-based models
    - **Advantages**: Handles non-linearity, considers interactions
    - **Disadvantages**: Can be biased toward high-cardinality features
    - **Use when**: Using tree-based models (RF, XGBoost)
    
    ### Best Practices
    
    1. **Try Multiple Methods**: Compare results across methods
    2. **Use Consensus**: Select features chosen by multiple methods
    3. **Consider Domain Knowledge**: Don't ignore important business features
    4. **Validate Performance**: Test model performance with selected features
    5. **Balance Complexity**: More features ≠ better model
    """)
    
    # Feature importance from current results
    if hasattr(st.session_state, 'feature_selection_result'):
        st.subheader("📈 Current Selection Impact")
        
        result = st.session_state.feature_selection_result
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Original Features", len(feature_cols))
        
        with col2:
            st.metric("Selected Features", len(result['selected_features']))
        
        with col3:
            reduction = (1 - len(result['selected_features']) / len(feature_cols)) * 100
            st.metric("Complexity Reduction", f"{reduction:.0f}%")
        
        st.info("""
        **Next Steps**:
        1. Go to the Model Training page
        2. Enable "Use Selected Features" option
        3. Train models with the selected features
        4. Compare performance with full feature set
        """)

# Export selected features
st.sidebar.markdown("---")
st.sidebar.subheader("💾 Export Selected Features")

if hasattr(st.session_state, 'feature_selection_result'):
    result = st.session_state.feature_selection_result
    
    if st.sidebar.button("📥 Download Selected Features"):
        features_df = pd.DataFrame({
            'Selected Features': result['selected_features']
        })
        
        csv = features_df.to_csv(index=False)
        st.sidebar.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name=f"selected_features_{selected_method}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# Information
st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ Information")
st.sidebar.info(f"""
**Dataset**: {len(X)} samples
**Features**: {len(feature_cols)} total
**Target**: Loan default prediction
""")
