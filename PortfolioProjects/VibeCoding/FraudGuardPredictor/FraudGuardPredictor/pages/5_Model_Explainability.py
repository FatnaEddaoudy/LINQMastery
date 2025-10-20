import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_processor import DataProcessor
from utils.ml_models import MLModels

st.set_page_config(page_title="Model Explainability", page_icon="🔍", layout="wide")

st.title("🔍 Model Explainability Dashboard")
st.markdown("### Understand How Models Make Predictions Using LIME")

data_processor = DataProcessor()
ml_models = MLModels()

if 'data' not in st.session_state:
    st.warning("⚠️ **Step 1:** Please load data from the Data Exploration page first!")
    st.info("Navigate to 'Data Exploration' in the sidebar to load your dataset.")
    st.stop()

if 'trained_models' not in st.session_state or not st.session_state.trained_models:
    st.warning("⚠️ **Step 2:** Please train models from the Model Training page first!")
    st.info("""
    You need trained models before using the explainability features. 
    
    To get started:
    1. ✅ Data is loaded (you've completed this step!)
    2. Go to 'Model Training' in the sidebar
    3. Select one or more models to train
    4. Click 'Train Models' button
    5. Return here to explain your predictions
    """)
    st.stop()

df = st.session_state.data
ml_models.models = st.session_state.trained_models
ml_models.model_results = st.session_state.get('model_results', {})
ml_models.scaler = st.session_state.get('model_scaler', None)

X = df.drop('bad_flag', axis=1)
y = df['bad_flag']

selected_features = st.session_state.get('selected_features', None)
if selected_features is not None and len(selected_features) > 0:
    X = X[selected_features]

feature_names = list(X.columns)

st.sidebar.header("🎛️ Explainability Settings")

available_models = list(ml_models.models.keys())
selected_model = st.sidebar.selectbox("Select Model to Explain", available_models)

tab1, tab2, tab3 = st.tabs(["📊 Individual Prediction", "🌍 Global Importance", "ℹ️ About LIME"])

with tab1:
    st.header("Individual Prediction Explanation")
    st.markdown("Analyze how specific features contribute to a prediction for a single loan application.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Select or Input Loan Data")
        
        input_method = st.radio("Input Method", ["Select from Dataset", "Manual Input"], horizontal=True)
        
        if input_method == "Select from Dataset":
            sample_idx = st.number_input(
                "Select Sample Index", 
                min_value=0, 
                max_value=len(X)-1, 
                value=0,
                help="Choose a loan from the dataset to explain"
            )
            instance = X.iloc[sample_idx].values
            actual_label = y.iloc[sample_idx]
            
            st.info(f"**Actual Label:** {'Default' if actual_label == 1 else 'No Default'}")
            
            with st.expander("View Selected Loan Data"):
                instance_df = pd.DataFrame([instance], columns=feature_names)
                st.dataframe(instance_df, use_container_width=True)
        
        else:
            st.markdown("Enter feature values manually:")
            instance_values = []
            
            cols = st.columns(3)
            for idx, feature in enumerate(feature_names):
                with cols[idx % 3]:
                    min_val = float(X[feature].min())
                    max_val = float(X[feature].max())
                    mean_val = float(X[feature].mean())
                    
                    value = st.number_input(
                        feature,
                        min_value=min_val,
                        max_value=max_val,
                        value=mean_val,
                        key=f"input_{feature}"
                    )
                    instance_values.append(value)
            
            instance = np.array(instance_values)
            actual_label = None
    
    with col2:
        num_features = st.slider(
            "Number of Top Features to Show",
            min_value=5,
            max_value=min(15, len(feature_names)),
            value=10
        )
        
        if st.button("🔍 Generate Explanation", type="primary"):
            with st.spinner("Generating explanation..."):
                explainer = ml_models.create_lime_explainer(X, feature_names)
                
                explanation = ml_models.explain_prediction(
                    selected_model, 
                    explainer, 
                    instance, 
                    feature_names,
                    num_features=num_features
                )
                
                st.session_state.current_explanation = explanation
    
    if 'current_explanation' in st.session_state and st.session_state.current_explanation:
        st.markdown("---")
        explanation = st.session_state.current_explanation
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Prediction",
                explanation['prediction'],
                help="Model's prediction for this loan"
            )
        
        with col2:
            st.metric(
                "Default Probability",
                f"{explanation['prediction_proba'][1]:.1%}",
                help="Probability of default"
            )
        
        with col3:
            st.metric(
                "No Default Probability",
                f"{explanation['prediction_proba'][0]:.1%}",
                help="Probability of no default"
            )
        
        st.subheader("Feature Contributions")
        fig = ml_models.plot_lime_explanation(explanation)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **How to interpret:**
        - **Green bars** push the prediction toward **Default**
        - **Red bars** push the prediction toward **No Default**
        - Longer bars indicate stronger influence on the prediction
        """)

with tab2:
    st.header("Global Feature Importance")
    st.markdown("Understand which features are most important across multiple predictions.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        num_samples = st.slider(
            "Number of Samples to Analyze",
            min_value=50,
            max_value=min(500, len(X)),
            value=100,
            help="More samples = more reliable but slower"
        )
    
    with col2:
        if st.button("📊 Calculate Global Importance", type="primary"):
            with st.spinner(f"Analyzing {num_samples} samples..."):
                explainer = ml_models.create_lime_explainer(X, feature_names)
                
                importance_df = ml_models.get_global_feature_importance(
                    selected_model,
                    explainer,
                    X.values,
                    feature_names,
                    num_samples=num_samples
                )
                
                st.session_state.global_importance = importance_df
    
    if 'global_importance' in st.session_state and st.session_state.global_importance is not None:
        importance_df = st.session_state.global_importance
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Top Features by Average Importance")
            
            top_features = importance_df.head(15)
            
            import plotly.express as px
            fig = px.bar(
                top_features,
                x='Average Importance',
                y='Feature',
                orientation='h',
                title=f'Top 15 Most Important Features ({selected_model})'
            )
            fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Importance Scores")
            st.dataframe(
                importance_df.head(15),
                use_container_width=True,
                hide_index=True
            )
        
        st.info("""
        **Global Importance** is calculated by averaging the absolute contribution of each feature 
        across many predictions. Higher values indicate features that consistently influence predictions.
        """)

with tab3:
    st.header("About LIME (Local Interpretable Model-agnostic Explanations)")
    
    st.markdown("""
    ### What is LIME?
    
    LIME is a technique that explains the predictions of any machine learning model by approximating 
    it locally with an interpretable model.
    
    ### How it Works:
    
    1. **Perturbation**: LIME creates variations of the input by changing feature values
    2. **Prediction**: Gets predictions from the black-box model for these variations
    3. **Learning**: Fits a simple, interpretable model (like linear regression) to approximate the complex model locally
    4. **Explanation**: Uses the simple model to explain which features matter most for this specific prediction
    
    ### Key Benefits:
    
    - **Model-Agnostic**: Works with any machine learning model (Random Forest, Neural Networks, XGBoost, etc.)
    - **Local Fidelity**: Provides accurate explanations for individual predictions
    - **Human-Interpretable**: Shows how each feature contributes to the prediction in an understandable way
    - **Debugging**: Helps identify when models make decisions based on spurious correlations
    
    ### Use Cases in Loan Default Prediction:
    
    - **Transparency**: Explain to loan officers why a loan was flagged as high risk
    - **Compliance**: Meet regulatory requirements for explainable AI in financial decisions
    - **Trust**: Build confidence in the model's predictions
    - **Debugging**: Identify if the model is using appropriate features
    
    ### Interpreting Results:
    
    - **Positive weights** (green): Features that increase the probability of default
    - **Negative weights** (red): Features that decrease the probability of default
    - **Magnitude**: Larger absolute values mean stronger influence
    
    ### Limitations:
    
    - Local explanations may not reflect global model behavior
    - Perturbation strategy can affect explanation quality
    - Computational cost increases with number of features
    """)
    
    st.info("💡 **Tip**: Compare LIME explanations with the feature importance from tree-based models on the Feature Selection page to validate insights.")
