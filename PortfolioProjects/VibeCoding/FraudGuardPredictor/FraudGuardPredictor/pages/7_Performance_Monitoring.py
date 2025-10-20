import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_processor import DataProcessor
from utils.ml_models import MLModels

st.set_page_config(page_title="Performance Monitoring", page_icon="📈", layout="wide")

st.title("📈 Performance Monitoring & Model Retraining")
st.markdown("### Track Model Performance Over Time and Manage Retraining")

ml_models = MLModels()

if 'trained_models' not in st.session_state or not st.session_state.trained_models:
    st.warning("⚠️ Please train models from the Model Training page first!")
    st.stop()

ml_models.models = st.session_state.trained_models
ml_models.model_results = st.session_state.get('model_results', {})
ml_models.scaler = st.session_state.get('model_scaler', None)
ml_models.selected_features = st.session_state.get('selected_features', None)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Current Performance", "📈 Historical Trends", "🔄 Model Comparison", "🔁 Retraining Workflow"])

with tab1:
    st.header("Current Model Performance")
    st.markdown("Overview of all trained models and their current performance metrics.")
    
    if ml_models.model_results:
        comparison_df = ml_models.get_model_comparison()
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Performance Summary")
            
            best_auc_model = max(ml_models.model_results.items(), 
                                key=lambda x: x[1]['auc_score'])
            best_precision_model = max(ml_models.model_results.items(), 
                                      key=lambda x: x[1]['classification_report']['1']['precision'])
            
            st.metric("Best AUC Score", 
                     f"{best_auc_model[1]['auc_score']:.3f}",
                     f"{best_auc_model[0]}")
            st.metric("Best Precision", 
                     f"{best_precision_model[1]['classification_report']['1']['precision']:.3f}",
                     f"{best_precision_model[0]}")
        
        with col2:
            st.subheader("Save Performance Snapshot")
            
            if st.button("💾 Save Current Performance to History", type="primary"):
                try:
                    with st.spinner("Saving performance metrics..."):
                        filepath = ml_models.save_performance_history()
                        st.success(f"✅ Performance metrics saved to: `{filepath}`")
                        st.info("This snapshot can be used to track model performance over time and compare with future retraining runs.")
                except Exception as e:
                    st.error(f"❌ Error saving performance: {str(e)}")
    else:
        st.warning("No model performance data available. Please train models first.")

with tab2:
    st.header("Historical Performance Trends")
    st.markdown("Visualize how model performance has changed over time.")
    
    history_path = st.text_input(
        "Performance History File",
        value="models/performance_history.json",
        help="Path to the performance history JSON file"
    )
    
    if os.path.exists(history_path):
        history = ml_models.load_performance_history(history_path)
        
        if history.get('records'):
            st.success(f"📊 Loaded {len(history['records'])} performance records")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                metric_to_plot = st.selectbox(
                    "Select Metric to Visualize",
                    ['auc_score', 'avg_precision', 'precision', 'recall', 'f1_score', 'cv_mean'],
                    format_func=lambda x: {
                        'auc_score': 'AUC Score',
                        'avg_precision': 'Average Precision',
                        'precision': 'Precision',
                        'recall': 'Recall',
                        'f1_score': 'F1 Score',
                        'cv_mean': 'Cross-Validation Mean'
                    }.get(x, x)
                )
            
            with col2:
                st.markdown("**Records Timeline:**")
                for i, record in enumerate(history['records'][-5:], 1):
                    timestamp = datetime.fromisoformat(record['timestamp'])
                    st.caption(f"{i}. {timestamp.strftime('%Y-%m-%d %H:%M')}")
            
            fig = ml_models.plot_performance_trends(history, metric_to_plot)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            st.subheader("Performance Records Details")
            
            records_data = []
            for record in history['records']:
                for model_name, metrics in record['models'].items():
                    records_data.append({
                        'Timestamp': record['timestamp'],
                        'Model': model_name,
                        'AUC': metrics.get('auc_score', 0),
                        'Precision': metrics.get('precision', 0),
                        'Recall': metrics.get('recall', 0),
                        'F1 Score': metrics.get('f1_score', 0)
                    })
            
            records_df = pd.DataFrame(records_data)
            st.dataframe(records_df, use_container_width=True, hide_index=True)
            
        else:
            st.info("No performance records found. Save current performance to start tracking.")
    else:
        st.info(f"Performance history file not found at: `{history_path}`")
        st.markdown("Save current performance from the 'Current Performance' tab to create the history file.")

with tab3:
    st.header("Model Comparison & A/B Testing")
    st.markdown("Compare current models with a baseline to evaluate improvements.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Select Baseline")
        
        baseline_source = st.radio(
            "Baseline Source",
            ["Load from File", "Use Historical Record"],
            horizontal=True
        )
        
        if baseline_source == "Load from File":
            baseline_path = st.text_input(
                "Baseline Model File",
                value="models/saved_models.pkl",
                help="Path to saved baseline model package"
            )
            
            if os.path.exists(baseline_path):
                if st.button("📂 Load Baseline Models"):
                    try:
                        baseline_ml = MLModels()
                        baseline_package = baseline_ml.load_models(baseline_path)
                        st.session_state.baseline_results = baseline_ml.model_results
                        st.success(f"✅ Loaded baseline with {len(baseline_ml.models)} model(s)")
                    except Exception as e:
                        st.error(f"❌ Error loading baseline: {str(e)}")
            else:
                st.warning(f"File not found: `{baseline_path}`")
        
        else:
            history_path_comp = st.text_input(
                "Performance History File",
                value="models/performance_history.json",
                key="history_comparison"
            )
            
            if os.path.exists(history_path_comp):
                history = ml_models.load_performance_history(history_path_comp)
                
                if history.get('records'):
                    record_options = [
                        f"{i+1}. {datetime.fromisoformat(r['timestamp']).strftime('%Y-%m-%d %H:%M')}"
                        for i, r in enumerate(history['records'])
                    ]
                    
                    selected_record = st.selectbox(
                        "Select Historical Record",
                        range(len(record_options)),
                        format_func=lambda x: record_options[x]
                    )
                    
                    if st.button("📊 Use This Record as Baseline"):
                        baseline_record = history['records'][selected_record]
                        
                        # Convert historical record to model_results format
                        baseline_results = {}
                        for model_name, metrics in baseline_record['models'].items():
                            baseline_results[model_name] = {
                                'auc_score': metrics['auc_score'],
                                'classification_report': {
                                    '1': {
                                        'precision': metrics.get('precision', 0),
                                        'recall': metrics.get('recall', 0),
                                        'f1-score': metrics.get('f1_score', 0)
                                    }
                                }
                            }
                        
                        st.session_state.baseline_results = baseline_results
                        st.success(f"✅ Using historical record as baseline")
    
    with col2:
        st.subheader("Comparison Results")
        
        if 'baseline_results' in st.session_state:
            comparison_df = ml_models.compare_with_baseline(st.session_state.baseline_results)
            
            if comparison_df is not None:
                st.dataframe(comparison_df, use_container_width=True, hide_index=True)
                
                improved_count = len(comparison_df[comparison_df['Status'].str.contains('Improved')])
                declined_count = len(comparison_df[comparison_df['Status'].str.contains('Declined')])
                
                st.markdown(f"""
                **Summary:**
                - 📈 Improved: {improved_count}
                - 📉 Declined: {declined_count}
                - ➡️ Same: {len(comparison_df) - improved_count - declined_count}
                """)
            else:
                st.warning("Unable to compare models. Ensure baseline has matching models.")
        else:
            st.info("Load a baseline to compare with current models.")

with tab4:
    st.header("Model Retraining Workflow")
    st.markdown("Best practices and workflow for retraining models with new data.")
    
    st.markdown("""
    ## 🔄 Retraining Process
    
    ### When to Retrain Models
    
    1. **Performance Degradation**
       - AUC score drops by >5%
       - Precision or recall significantly declines
       - Increased false positive/negative rates
    
    2. **New Data Available**
       - Substantial new loan data collected
       - Data distribution has changed
       - New fraud patterns identified
    
    3. **Regular Schedule**
       - Monthly or quarterly retraining
       - After major business changes
       - Regulatory compliance requirements
    
    ### Retraining Steps
    
    1. **Data Preparation**
       - Load new data from Data Exploration page
       - Verify data quality and completeness
       - Check for data drift or anomalies
    
    2. **Feature Selection** (Optional)
       - Re-run feature selection if needed
       - Compare with previous feature sets
       - Update feature list if beneficial
    
    3. **Model Training**
       - Train models with same configuration
       - Use Model Training page
       - Ensure consistent preprocessing
    
    4. **Performance Evaluation**
       - Compare with baseline (previous models)
       - Check all key metrics
       - Validate on holdout set
    
    5. **Decision**
       - Deploy if improved or stable
       - Investigate if degraded
       - A/B test if uncertain
    
    6. **Deployment**
       - Save new models
       - Update performance history
       - Export deployment scripts
       - Document changes
    
    ### Workflow Checklist
    """)
    
    st.markdown("**Pre-Training:**")
    pre_training = [
        st.checkbox("✅ New data loaded and validated", key="check1"),
        st.checkbox("✅ Data quality checked (no missing values, correct types)", key="check2"),
        st.checkbox("✅ Feature selection reviewed", key="check3"),
        st.checkbox("✅ Baseline performance recorded", key="check4")
    ]
    
    st.markdown("**Training:**")
    training = [
        st.checkbox("✅ Models trained with appropriate parameters", key="check5"),
        st.checkbox("✅ Cross-validation results reviewed", key="check6"),
        st.checkbox("✅ Feature importance analyzed", key="check7")
    ]
    
    st.markdown("**Post-Training:**")
    post_training = [
        st.checkbox("✅ Performance compared with baseline", key="check8"),
        st.checkbox("✅ All metrics reviewed and acceptable", key="check9"),
        st.checkbox("✅ Models saved and performance recorded", key="check10"),
        st.checkbox("✅ Deployment scripts exported", key="check11"),
        st.checkbox("✅ Documentation updated", key="check12")
    ]
    
    total_checks = len(pre_training) + len(training) + len(post_training)
    completed_checks = sum(pre_training + training + post_training)
    
    progress = completed_checks / total_checks if total_checks > 0 else 0
    st.progress(progress)
    st.caption(f"Progress: {completed_checks}/{total_checks} steps completed")
    
    if progress == 1.0:
        st.success("🎉 All retraining steps completed! Models are ready for deployment.")
    
    st.markdown("""
    ---
    
    ## 📊 Monitoring Best Practices
    
    1. **Track Key Metrics**
       - AUC, Precision, Recall, F1-Score
       - Confusion matrix patterns
       - Prediction distribution
    
    2. **Data Drift Detection**
       - Monitor input feature distributions
       - Track prediction probability distributions
       - Alert on significant changes
    
    3. **Business Metrics**
       - Default rates vs predictions
       - Financial impact (ROI)
       - False positive/negative costs
    
    4. **Documentation**
       - Record all retraining decisions
       - Document model versions
       - Track deployment history
    
    ## 🚨 Alert Thresholds
    
    Consider retraining or investigation when:
    - AUC drops >5% from baseline
    - Precision or Recall drops >10%
    - Prediction distribution shifts significantly
    - Business metrics deteriorate
    - Major data or process changes occur
    """)
