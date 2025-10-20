import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_processor import DataProcessor
from utils.ml_models import MLModels

st.set_page_config(page_title="Model Deployment", page_icon="🚀", layout="wide")

st.title("🚀 Model Deployment & Persistence")
st.markdown("### Save, Load, and Export Models for Production Use")

ml_models = MLModels()

if 'trained_models' not in st.session_state or not st.session_state.trained_models:
    st.warning("⚠️ Please train models from the Model Training page first!")
    st.stop()

ml_models.models = st.session_state.trained_models
ml_models.model_results = st.session_state.get('model_results', {})
ml_models.scaler = st.session_state.get('model_scaler', None)
ml_models.selected_features = st.session_state.get('selected_features', None)

tab1, tab2, tab3, tab4 = st.tabs(["💾 Save Models", "📂 Load Models", "📦 Export Scripts", "📊 Deployment Info"])

with tab1:
    st.header("Save Trained Models")
    st.markdown("Save your trained models to disk for later use or deployment.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        save_path = st.text_input(
            "Save Location",
            value="models/saved_models.pkl",
            help="Path where the model package will be saved"
        )
        
        save_metadata = st.checkbox(
            "Save Metadata (JSON)",
            value=True,
            help="Save model performance metrics and configuration as JSON"
        )
        
        st.markdown("**Models to be saved:**")
        for name in ml_models.models.keys():
            result = ml_models.model_results.get(name, {})
            auc = result.get('auc_score', 0)
            st.markdown(f"- **{name}** (AUC: {auc:.3f})")
    
    with col2:
        st.markdown("**Package Contents:**")
        st.info(f"""
        - Models: {len(ml_models.models)}
        - Scaler: {'✅ Yes' if ml_models.scaler else '❌ No'}
        - Features: {len(ml_models.selected_features) if ml_models.selected_features else 'All'}
        - Metadata: {'✅ Yes' if save_metadata else '❌ No'}
        """)
    
    if st.button("💾 Save Models", type="primary"):
        try:
            with st.spinner("Saving models..."):
                filepath = ml_models.save_models(save_path, save_metadata)
                
                st.success(f"✅ Models saved successfully to: `{filepath}`")
                
                if save_metadata:
                    metadata_path = filepath.replace('.pkl', '_metadata.json')
                    st.success(f"✅ Metadata saved to: `{metadata_path}`")
                
                # Show file info
                file_size = os.path.getsize(filepath) / (1024 * 1024)  # Convert to MB
                st.info(f"📁 Model file size: {file_size:.2f} MB")
                
        except Exception as e:
            st.error(f"❌ Error saving models: {str(e)}")

with tab2:
    st.header("Load Saved Models")
    st.markdown("Load previously saved models from disk.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        load_path = st.text_input(
            "Load Location",
            value="models/saved_models.pkl",
            help="Path to the saved model package",
            key="load_path"
        )
        
        # Check if file exists
        if os.path.exists(load_path):
            st.success(f"✅ File found: `{load_path}`")
            
            # Try to load metadata if available
            metadata_path = load_path.replace('.pkl', '_metadata.json')
            if os.path.exists(metadata_path):
                import json
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                
                st.markdown("**Model Package Info:**")
                st.json(metadata)
        else:
            st.warning(f"⚠️ File not found: `{load_path}`")
    
    with col2:
        if st.button("📂 Load Models", type="primary"):
            try:
                with st.spinner("Loading models..."):
                    model_package = ml_models.load_models(load_path)
                    
                    # Update session state
                    st.session_state.trained_models = ml_models.models
                    st.session_state.model_scaler = ml_models.scaler
                    st.session_state.selected_features = ml_models.selected_features
                    
                    st.success(f"✅ Loaded {len(ml_models.models)} model(s)")
                    
                    for name in ml_models.models.keys():
                        st.markdown(f"- {name}")
                    
                    st.info("💡 Models loaded into session. You can now use them for predictions!")
                    
            except Exception as e:
                st.error(f"❌ Error loading models: {str(e)}")

with tab3:
    st.header("Export Prediction Scripts")
    st.markdown("Generate standalone Python scripts for deployment and batch predictions.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_model = st.selectbox(
            "Select Model to Export",
            list(ml_models.models.keys()),
            help="Choose which model to create a deployment script for"
        )
        
        export_path = st.text_input(
            "Export Location",
            value=f"deployment/predict_{selected_model.lower().replace(' ', '_')}.py" if selected_model else "deployment/predict_model.py",
            help="Path where the prediction script will be saved"
        )
        
        st.markdown("""
        **The exported script will include:**
        - Model loading functionality
        - Single prediction function
        - Batch prediction from CSV
        - Command-line interface
        - Automatic feature selection and scaling
        """)
    
    with col2:
        st.markdown("**Usage:**")
        st.code("""
# Single prediction
from predict import predict
result = predict(data_dict)

# Batch prediction
python predict.py input.csv output.csv
        """, language="python")
    
    if st.button("📦 Export Script", type="primary"):
        try:
            with st.spinner("Generating prediction script..."):
                script_path = ml_models.export_prediction_script(selected_model, export_path)
                
                st.success(f"✅ Prediction script exported to: `{script_path}`")
                
                # Read and display the generated script
                with open(script_path, 'r') as f:
                    script_content = f.read()
                
                with st.expander("📄 View Generated Script"):
                    st.code(script_content, language="python")
                
                st.info("""
                **Next Steps:**
                1. Ensure models are saved using the "Save Models" tab
                2. Copy the deployment folder to your production environment
                3. Install required dependencies: `pip install pandas numpy scikit-learn xgboost`
                4. Run predictions: `python predict.py your_data.csv`
                """)
                
        except Exception as e:
            st.error(f"❌ Error exporting script: {str(e)}")

with tab4:
    st.header("Deployment Information")
    st.markdown("### Understanding Model Deployment")
    
    st.markdown("""
    ## 📋 Deployment Workflow
    
    ### 1. Save Models
    - Serializes all trained models, scaler, and feature selection settings
    - Creates a portable `.pkl` file containing the complete model package
    - Optionally saves metadata in JSON format for documentation
    
    ### 2. Export Prediction Script
    - Generates a standalone Python script for your selected model
    - Includes all necessary code for loading models and making predictions
    - Supports both single predictions and batch processing
    - Handles feature scaling and selection automatically
    
    ### 3. Deploy to Production
    
    #### Option A: Batch Processing
    ```bash
    # Process a CSV file with new loan applications
    python predict.py new_loans.csv predictions.csv
    ```
    
    #### Option B: API Integration
    ```python
    # Import in your application
    from predict import predict
    
    loan_data = {
        'feature1': value1,
        'feature2': value2,
        # ... other features
    }
    
    result = predict(loan_data)
    print(result['default_probability'])
    ```
    
    #### Option C: Streamlit App (Current)
    - Use the Predictions page for interactive predictions
    - Suitable for business users and exploratory analysis
    
    ## 🔧 System Requirements
    
    **Python Dependencies:**
    ```
    pandas
    numpy
    scikit-learn
    xgboost
    ```
    
    **For Neural Network or Logistic Regression:**
    - Scaler must be included in the model package
    - Automatic scaling is handled by the prediction script
    
    ## 📊 Model Performance Tracking
    
    """)
    
    if ml_models.model_results:
        st.markdown("### Current Model Performance")
        
        comparison_df = ml_models.get_model_comparison()
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    st.markdown("""
    ## 🔒 Best Practices
    
    1. **Version Control**
       - Save models with timestamps or version numbers
       - Track model metadata (features, performance, date)
       - Document any data preprocessing steps
    
    2. **Model Monitoring**
       - Regularly evaluate model performance on new data
       - Track prediction distributions
       - Watch for data drift or concept drift
    
    3. **Security**
       - Validate input data before predictions
       - Handle errors gracefully
       - Log predictions for audit trails
    
    4. **Scalability**
       - Consider model size for deployment environment
       - Optimize prediction speed if needed
       - Implement caching for repeated predictions
    
    ## 🚨 Important Notes
    
    - **Feature Consistency**: New data must have the same features used during training
    - **Data Format**: Input data should match the training data distribution
    - **Model Refresh**: Retrain models periodically with new data
    - **Backup**: Always keep backups of production models
    """)
