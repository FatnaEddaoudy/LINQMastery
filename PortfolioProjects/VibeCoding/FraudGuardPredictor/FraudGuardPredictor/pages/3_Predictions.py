import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_processor import DataProcessor
from utils.ml_models import MLModels

st.set_page_config(
    page_title="Predictions - Loan Fraud Detection",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Loan Default Predictions & Risk Assessment")

# Initialize session state
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()

if 'ml_models' not in st.session_state:
    st.session_state.ml_models = MLModels()

# Check if models are trained
if not hasattr(st.session_state, 'model_results'):
    st.error("⚠️ No trained models found. Please train models first in the Model Training page.")
    st.stop()

# Load data for predictions
@st.cache_data
def load_prediction_data():
    processor = DataProcessor()
    df = processor.load_data('attached_assets/FlaggingLoans_1760351927870.csv')
    if df is not None:
        X, y, feature_cols = processor.prepare_modeling_data(df)
        return X, y, feature_cols, df
    return None, None, None, None

X, y, feature_cols, df_raw = load_prediction_data()

if X is None:
    st.error("Failed to load prediction data.")
    st.stop()

# Sidebar configuration
st.sidebar.header("🎛️ Prediction Settings")

# Model selection
available_models = list(st.session_state.model_results.keys())
selected_model = st.sidebar.selectbox("Select Model for Predictions", available_models)

# Prediction mode
prediction_mode = st.sidebar.radio(
    "Prediction Mode",
    ["✨ Simple Prediction", "📊 Approval Level Analysis", "🔍 Individual Prediction", "📈 Batch Analysis"]
)

# Main content based on prediction mode
if prediction_mode == "✨ Simple Prediction":
    st.header("✨ Simple Loan Prediction")
    
    st.info("📝 Enter all loan features below and click the button to get an instant Good/Bad loan prediction.")
    
    # Add note about score fields
    with st.expander("ℹ️ About Score Fields (score_1 and score_2)", expanded=False):
        st.markdown("""
        **Score fields can be unknown/null for many loans:**
        - **Score_1**: Unknown in 15% of historical loans
        - **Score_2**: Unknown in 94% of historical loans
        
        **How to handle unknown scores:**
        - ✅ **Check the "Unknown/Null" checkbox** if you don't have the score
        - The system will automatically use median values: Score_1 = 588.53, Score_2 = 556.76
        - OR enter any value you have (including 0 or negative values)
        - This matches the approach used when training the models
        """)
    
    # Get unique values for categorical fields from raw data
    gender_options = ['Male', 'Female', 'Unknown']
    region_options = ['Unknown'] + sorted([r for r in df_raw['federal_district_nm'].unique() if pd.notna(r)])
    
    # Create input form with all features
    with st.form("simple_prediction_form"):
        st.subheader("Loan Features")
        
        # Organize features into columns
        num_cols = 3
        cols = st.columns(num_cols)
        
        input_data = {}
        score_unknown = {}
        categorical_selections = {}
        
        # Create input for each feature
        for idx, feature in enumerate(feature_cols):
            col_idx = idx % num_cols
            
            with cols[col_idx]:
                if feature in X.columns:
                    # Clean feature name for display
                    display_name = feature.replace('_', ' ').title()
                    
                    # Special handling for categorical encoded fields
                    if feature == 'gender_encoded':
                        categorical_selections['gender'] = st.selectbox(
                            "Gender",
                            options=gender_options,
                            index=2,  # Default to Unknown
                            key=f"simple_gender",
                            help="Select gender or leave as Unknown if not available"
                        )
                        # Will encode later
                        continue
                    
                    elif feature == 'federal_district_nm_encoded':
                        categorical_selections['federal_district_nm'] = st.selectbox(
                            "Federal District",
                            options=region_options,
                            index=0,  # Default to Unknown
                            key=f"simple_federal_district",
                            help="Select region (e.g., region_1, region_6) or leave as Unknown"
                        )
                        # Will encode later
                        continue
                    
                    # Numerical features
                    min_val = float(X[feature].min())
                    max_val = float(X[feature].max())
                    mean_val = float(X[feature].mean())
                    
                    # Special handling for score fields - allow null/unknown
                    if feature in ['score_1', 'score_2']:
                        median_val = float(df_raw[feature].median())
                        
                        # Checkbox to mark score as unknown
                        score_unknown[feature] = st.checkbox(
                            f"⬜ {display_name} is Unknown/Null",
                            value=False,
                            key=f"simple_{feature}_unknown",
                            help="Check this if the score is not available"
                        )
                        
                        # Input field (disabled if unknown)
                        if score_unknown[feature]:
                            # Show median value when unknown
                            st.info(f"Using median value: {median_val:.2f}")
                            input_data[feature] = median_val
                        else:
                            # Allow any value (no min constraint)
                            input_data[feature] = st.number_input(
                                display_name,
                                value=median_val,
                                key=f"simple_{feature}",
                                help=f"Typical range: {min_val:.2f} - {max_val:.2f}"
                            )
                    else:
                        help_text = f"Range: {min_val:.2f} - {max_val:.2f}"
                        default_val = mean_val
                        
                        input_data[feature] = st.number_input(
                            display_name,
                            min_value=min_val,
                            max_value=max_val,
                            value=default_val,
                            key=f"simple_{feature}",
                            help=help_text
                        )
        
        # Submit button
        submitted = st.form_submit_button("🎯 Predict Loan Status", type="primary", use_container_width=True)
        
        if submitted:
            # Encode categorical selections
            if 'gender' in categorical_selections:
                gender_value = categorical_selections['gender']
                # Map user-friendly values to actual data values
                gender_mapping = {'Male': False, 'Female': True, 'Unknown': 'Unknown'}
                actual_gender = gender_mapping.get(gender_value, 'Unknown')
                
                # Encode using the data processor's label encoder
                if 'gender' in st.session_state.data_processor.label_encoders:
                    encoder = st.session_state.data_processor.label_encoders['gender']
                    
                    # Check if Unknown is in the encoder classes
                    if 'Unknown' not in encoder.classes_:
                        st.error(f"⚠️ 'Unknown' is not a valid option. The model was trained without Unknown gender values. Please select Male or Female.")
                        st.stop()
                    
                    try:
                        # Encode the actual value
                        if actual_gender == 'Unknown':
                            encoded_val = encoder.transform(['Unknown'])[0]
                        else:
                            # Check if the value exists in encoder
                            if actual_gender not in encoder.classes_:
                                st.error(f"⚠️ Gender value '{actual_gender}' not recognized. Using 'Unknown' instead.")
                                encoded_val = encoder.transform(['Unknown'])[0]
                            else:
                                encoded_val = encoder.transform([actual_gender])[0]
                        input_data['gender_encoded'] = float(encoded_val)
                    except Exception as e:
                        st.error(f"Error encoding gender: {str(e)}")
                        st.stop()
            
            if 'federal_district_nm' in categorical_selections:
                district_value = categorical_selections['federal_district_nm']
                
                # Encode using the data processor's label encoder
                if 'federal_district_nm' in st.session_state.data_processor.label_encoders:
                    encoder = st.session_state.data_processor.label_encoders['federal_district_nm']
                    
                    # Check if Unknown is in the encoder classes
                    if district_value == 'Unknown' and 'Unknown' not in encoder.classes_:
                        st.error(f"⚠️ 'Unknown' is not a valid option. The model was trained without Unknown district values. Please select a specific region.")
                        st.stop()
                    
                    try:
                        # Check if the value exists in encoder
                        if district_value not in encoder.classes_:
                            st.error(f"⚠️ District '{district_value}' not recognized by the model. Available options: {list(encoder.classes_)}")
                            st.stop()
                        
                        encoded_val = encoder.transform([district_value])[0]
                        input_data['federal_district_nm_encoded'] = float(encoded_val)
                    except Exception as e:
                        st.error(f"Error encoding federal district: {str(e)}")
                        st.stop()
            
            # Create prediction dataframe
            pred_df = pd.DataFrame([input_data])
            
            # Add any missing columns with default values
            for col in feature_cols:
                if col not in pred_df.columns:
                    pred_df[col] = 0.0
            
            # Ensure correct column order
            pred_df = pred_df[feature_cols]
            
            # Make prediction
            probability = st.session_state.ml_models.predict_default_probability(
                selected_model, pred_df
            )
            
            if probability is not None:
                prob_pct = probability[0] * 100
                
                # Display result prominently
                st.markdown("---")
                st.subheader("🎯 Prediction Result")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col2:
                    # Determine loan status
                    if prob_pct < 50:
                        loan_status = "✅ GOOD LOAN"
                        status_color = "green"
                        status_emoji = "✅"
                        explanation = "This loan has a low probability of default and is recommended for approval."
                    else:
                        loan_status = "❌ BAD LOAN"
                        status_color = "red"
                        status_emoji = "❌"
                        explanation = "This loan has a high probability of default and is NOT recommended for approval."
                    
                    # Display with large, prominent styling
                    st.markdown(f"<h1 style='text-align: center; color: {status_color};'>{status_emoji} {loan_status}</h1>", 
                               unsafe_allow_html=True)
                    
                    st.metric("Default Probability", f"{prob_pct:.2f}%", 
                             delta=f"{prob_pct - 50:.2f}% from threshold" if prob_pct != 50 else None,
                             delta_color="inverse")
                    
                    st.info(explanation)
                    
                    # Additional risk breakdown
                    with st.expander("📊 Risk Breakdown"):
                        if prob_pct < 10:
                            risk_level = "Very Low Risk"
                            risk_bar_color = "darkgreen"
                        elif prob_pct < 25:
                            risk_level = "Low Risk"
                            risk_bar_color = "green"
                        elif prob_pct < 50:
                            risk_level = "Moderate Risk"
                            risk_bar_color = "orange"
                        elif prob_pct < 75:
                            risk_level = "High Risk"
                            risk_bar_color = "red"
                        else:
                            risk_level = "Very High Risk"
                            risk_bar_color = "darkred"
                        
                        st.write(f"**Risk Level:** {risk_level}")
                        
                        # Visual risk gauge
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=prob_pct,
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': "Default Risk Gauge"},
                            gauge={
                                'axis': {'range': [0, 100]},
                                'bar': {'color': risk_bar_color},
                                'steps': [
                                    {'range': [0, 25], 'color': "lightgreen"},
                                    {'range': [25, 50], 'color': "lightyellow"},
                                    {'range': [50, 75], 'color': "lightsalmon"},
                                    {'range': [75, 100], 'color': "lightcoral"}
                                ],
                                'threshold': {
                                    'line': {'color': "black", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 50
                                }
                            }
                        ))
                        
                        fig.update_layout(height=300)
                        st.plotly_chart(fig, use_container_width=True)

elif prediction_mode == "📊 Approval Level Analysis":
    st.header("📊 Expected Default Rates at Different Approval Levels")
    
    st.info("""
    This analysis shows how the expected default rate changes based on different approval thresholds.
    Lower thresholds mean stricter approval criteria (approving only loans with very low predicted default probability).
    """)
    
    # Approval level configuration
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("🎛️ Configuration")
        
        # Threshold settings
        min_threshold = st.slider("Minimum Threshold", 0.0, 0.5, 0.05, 0.01)
        max_threshold = st.slider("Maximum Threshold", 0.1, 1.0, 0.8, 0.05)
        step_size = st.slider("Step Size", 0.01, 0.1, 0.05, 0.01)
        
        # Generate thresholds
        thresholds = np.arange(min_threshold, max_threshold + step_size, step_size)
        
        # Business parameters
        st.subheader("💼 Business Parameters")
        revenue_per_loan = st.number_input("Revenue per Loan ($)", 500, 5000, 1000)
        loss_per_default = st.number_input("Loss per Default ($)", 1000, 20000, 5000)
    
    with col1:
        # Calculate approval analysis
        with st.spinner("Analyzing approval levels..."):
            approval_analysis = st.session_state.ml_models.analyze_approval_levels(
                selected_model, X, y, thresholds.tolist()
            )
        
        if approval_analysis is not None:
            # Update business calculations
            approval_analysis['expected_revenue'] = approval_analysis['approved_loans'] * revenue_per_loan
            approval_analysis['expected_loss'] = approval_analysis['expected_defaults'] * loss_per_default
            approval_analysis['net_expected_value'] = approval_analysis['expected_revenue'] - approval_analysis['expected_loss']
            approval_analysis['roi'] = (approval_analysis['net_expected_value'] / approval_analysis['expected_revenue']) * 100
            
            # Key metrics
            st.subheader("📈 Key Insights")
            
            # Find optimal threshold
            optimal_idx = approval_analysis['net_expected_value'].idxmax()
            optimal_threshold = approval_analysis.loc[optimal_idx, 'threshold']
            optimal_roi = approval_analysis.loc[optimal_idx, 'roi']
            optimal_approval_rate = approval_analysis.loc[optimal_idx, 'approval_rate']
            optimal_default_rate = approval_analysis.loc[optimal_idx, 'actual_default_rate']
            
            col_a, col_b, col_c, col_d = st.columns(4)
            
            with col_a:
                st.metric("Optimal Threshold", f"{optimal_threshold:.2f}")
            with col_b:
                st.metric("Optimal ROI", f"{optimal_roi:.1f}%")
            with col_c:
                st.metric("Approval Rate", f"{optimal_approval_rate:.1f}%")
            with col_d:
                st.metric("Default Rate", f"{optimal_default_rate:.1f}%")
    
    # Visualizations
    if approval_analysis is not None:
        st.subheader("📊 Analysis Visualizations")
        
        # Create subplot figure
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Approval Rate vs Threshold', 'Default Rate vs Threshold', 
                          'ROI vs Threshold', 'Net Expected Value vs Threshold'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Approval Rate
        fig.add_trace(
            go.Scatter(x=approval_analysis['threshold'], y=approval_analysis['approval_rate'],
                      mode='lines+markers', name='Approval Rate (%)', line=dict(color='blue')),
            row=1, col=1
        )
        
        # Default Rate
        fig.add_trace(
            go.Scatter(x=approval_analysis['threshold'], y=approval_analysis['actual_default_rate'],
                      mode='lines+markers', name='Default Rate (%)', line=dict(color='red')),
            row=1, col=2
        )
        
        # ROI
        fig.add_trace(
            go.Scatter(x=approval_analysis['threshold'], y=approval_analysis['roi'],
                      mode='lines+markers', name='ROI (%)', line=dict(color='green')),
            row=2, col=1
        )
        
        # Net Expected Value
        fig.add_trace(
            go.Scatter(x=approval_analysis['threshold'], y=approval_analysis['net_expected_value'],
                      mode='lines+markers', name='Net Expected Value ($)', line=dict(color='purple')),
            row=2, col=2
        )
        
        # Add optimal threshold line
        fig.add_vline(x=optimal_threshold, line_dash="dash", line_color="orange", 
                     annotation_text="Optimal Threshold")
        
        fig.update_layout(
            height=700,
            showlegend=False,
            title_text=f"Approval Level Analysis - {selected_model}"
        )
        
        fig.update_xaxes(title_text="Threshold", row=2, col=1)
        fig.update_xaxes(title_text="Threshold", row=2, col=2)
        fig.update_yaxes(title_text="Approval Rate (%)", row=1, col=1)
        fig.update_yaxes(title_text="Default Rate (%)", row=1, col=2)
        fig.update_yaxes(title_text="ROI (%)", row=2, col=1)
        fig.update_yaxes(title_text="Net Expected Value ($)", row=2, col=2)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.subheader("📋 Detailed Analysis Table")
        
        # Format the dataframe for display
        display_df = approval_analysis.copy()
        display_df['threshold'] = display_df['threshold'].round(3)
        display_df['approval_rate'] = display_df['approval_rate'].round(1)
        display_df['actual_default_rate'] = display_df['actual_default_rate'].round(2)
        display_df['roi'] = display_df['roi'].round(1)
        display_df['net_expected_value'] = display_df['net_expected_value'].astype(int)
        
        # Rename columns for display
        display_columns = {
            'threshold': 'Threshold',
            'approval_rate': 'Approval Rate (%)',
            'approved_loans': 'Approved Loans',
            'actual_default_rate': 'Default Rate (%)',
            'expected_defaults': 'Expected Defaults',
            'net_expected_value': 'Net Value ($)',
            'roi': 'ROI (%)'
        }
        
        display_df = display_df.rename(columns=display_columns)
        selected_cols = list(display_columns.values())
        
        st.dataframe(
            display_df[selected_cols],
            use_container_width=True,
            hide_index=True
        )

elif prediction_mode == "🔍 Individual Prediction":
    st.header("🔍 Individual Loan Prediction")
    
    st.info("Enter loan characteristics below to get a default probability prediction.")
    
    # Create input form
    with st.form("individual_prediction"):
        st.subheader("📝 Loan Information")
        
        col1, col2, col3 = st.columns(3)
        
        # Get feature ranges for input validation
        feature_ranges = {}
        for feature in feature_cols:
            if feature in X.columns:
                feature_ranges[feature] = {
                    'min': float(X[feature].min()),
                    'max': float(X[feature].max()),
                    'mean': float(X[feature].mean())
                }
        
        # Create input fields
        input_data = {}
        
        with col1:
            st.write("**Demographic Information**")
            if 'age' in feature_ranges:
                input_data['age'] = st.slider(
                    "Age", 
                    int(feature_ranges['age']['min']), 
                    int(feature_ranges['age']['max']), 
                    int(feature_ranges['age']['mean'])
                )
            
            if 'federal_district_nm_encoded' in feature_ranges:
                input_data['federal_district_nm_encoded'] = st.slider(
                    "Federal District (encoded)", 
                    int(feature_ranges['federal_district_nm_encoded']['min']), 
                    int(feature_ranges['federal_district_nm_encoded']['max']), 
                    int(feature_ranges['federal_district_nm_encoded']['mean'])
                )
        
        with col2:
            st.write("**Payment Information**")
            payment_features = [f for f in feature_cols if f.startswith('payment_type_')]
            for feature in payment_features[:3]:  # Limit to first 3 payment types
                if feature in feature_ranges:
                    input_data[feature] = st.number_input(
                        feature.replace('_', ' ').title(),
                        min_value=feature_ranges[feature]['min'],
                        max_value=feature_ranges[feature]['max'],
                        value=feature_ranges[feature]['mean'],
                        key=feature
                    )
        
        with col3:
            st.write("**Risk Indicators**")
            risk_features = ['dpd_5_cnt', 'dpd_15_cnt', 'dpd_30_cnt', 'past_billings_cnt']
            for feature in risk_features:
                if feature in feature_ranges:
                    input_data[feature] = st.number_input(
                        feature.replace('_', ' ').title(),
                        min_value=feature_ranges[feature]['min'],
                        max_value=feature_ranges[feature]['max'],
                        value=0.0,
                        key=feature
                    )
        
        submitted = st.form_submit_button("🔮 Predict Default Probability", type="primary")
        
        if submitted:
            # Create prediction dataframe
            pred_df = pd.DataFrame([input_data])
            
            # Add missing features with default values
            for feature in feature_cols:
                if feature not in pred_df.columns:
                    if feature in X.columns:
                        pred_df[feature] = X[feature].mean()
                    else:
                        pred_df[feature] = 0
            
            # Ensure correct column order
            pred_df = pred_df[feature_cols]
            
            # Make prediction
            probability = st.session_state.ml_models.predict_default_probability(
                selected_model, pred_df
            )
            
            if probability is not None:
                prob_pct = probability[0] * 100
                
                # Display result
                col1, col2, col3 = st.columns(3)
                
                with col2:
                    st.metric("Default Probability", f"{prob_pct:.2f}%")
                    
                    # Risk level classification
                    if prob_pct < 10:
                        risk_level = "🟢 Low Risk"
                        risk_color = "green"
                    elif prob_pct < 25:
                        risk_level = "🟡 Medium Risk"
                        risk_color = "orange"
                    elif prob_pct < 50:
                        risk_level = "🟠 High Risk"
                        risk_color = "red"
                    else:
                        risk_level = "🔴 Very High Risk"
                        risk_color = "darkred"
                    
                    st.markdown(f"**Risk Level:** {risk_level}")
                    
                    # Recommendation
                    if prob_pct < 20:
                        recommendation = "✅ **APPROVE** - Low default risk"
                    elif prob_pct < 40:
                        recommendation = "⚠️ **REVIEW** - Requires additional assessment"
                    else:
                        recommendation = "❌ **REJECT** - High default risk"
                    
                    st.markdown(f"**Recommendation:** {recommendation}")

elif prediction_mode == "📈 Batch Analysis":
    st.header("📈 Batch Loan Analysis")
    
    st.info("Analyze default probabilities for multiple loans in the dataset.")
    
    # Sample selection
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("🎛️ Settings")
        
        sample_size = st.slider("Sample Size", 100, min(2000, len(X)), 500)
        random_seed = st.number_input("Random Seed", 1, 1000, 42)
        
        analysis_type = st.radio(
            "Analysis Type",
            ["Random Sample", "High Risk Cases", "Low Risk Cases"]
        )
    
    with col1:
        # Get predictions for sample
        if analysis_type == "Random Sample":
            sample_indices = np.random.RandomState(random_seed).choice(len(X), sample_size, replace=False)
            sample_X = X.iloc[sample_indices]
            sample_y = y.iloc[sample_indices]
            title_suffix = "Random Sample"
        elif analysis_type == "High Risk Cases":
            # Select cases with higher actual default rate features
            risk_score = X[['dpd_5_cnt', 'dpd_15_cnt', 'dpd_30_cnt']].fillna(0).sum(axis=1)
            high_risk_indices = risk_score.nlargest(sample_size).index
            sample_X = X.loc[high_risk_indices]
            sample_y = y.loc[high_risk_indices]
            title_suffix = "High Risk Cases"
        else:  # Low Risk Cases
            risk_score = X[['dpd_5_cnt', 'dpd_15_cnt', 'dpd_30_cnt']].fillna(0).sum(axis=1)
            low_risk_indices = risk_score.nsmallest(sample_size).index
            sample_X = X.loc[low_risk_indices]
            sample_y = y.loc[low_risk_indices]
            title_suffix = "Low Risk Cases"
        
        # Make predictions
        with st.spinner("Making batch predictions..."):
            probabilities = st.session_state.ml_models.predict_default_probability(
                selected_model, sample_X
            )
        
        if probabilities is not None:
            # Create results dataframe
            results_df = pd.DataFrame({
                'Loan_Index': sample_X.index,
                'Predicted_Probability': probabilities,
                'Actual_Default': sample_y.values,
                'Risk_Level': pd.cut(
                    probabilities, 
                    bins=[0, 0.1, 0.25, 0.5, 1.0], 
                    labels=['Low', 'Medium', 'High', 'Very High']
                )
            })
            
            # Summary statistics
            st.subheader(f"📊 {title_suffix} Analysis Summary")
            
            col_a, col_b, col_c, col_d = st.columns(4)
            
            with col_a:
                st.metric("Sample Size", f"{len(results_df):,}")
            with col_b:
                avg_prob = results_df['Predicted_Probability'].mean() * 100
                st.metric("Avg Predicted Risk", f"{avg_prob:.1f}%")
            with col_c:
                actual_default_rate = results_df['Actual_Default'].mean() * 100
                st.metric("Actual Default Rate", f"{actual_default_rate:.1f}%")
            with col_d:
                # Model accuracy on this sample
                predictions_binary = (probabilities > 0.5).astype(int)
                accuracy = (predictions_binary == sample_y.values).mean() * 100
                st.metric("Model Accuracy", f"{accuracy:.1f}%")
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Probability distribution
                fig = px.histogram(
                    results_df,
                    x='Predicted_Probability',
                    nbins=30,
                    title=f"Predicted Probability Distribution - {title_suffix}",
                    labels={'Predicted_Probability': 'Default Probability'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Risk level distribution
                risk_counts = results_df['Risk_Level'].value_counts()
                fig = px.pie(
                    values=risk_counts.values,
                    names=risk_counts.index,
                    title=f"Risk Level Distribution - {title_suffix}"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed results table
            st.subheader("📋 Detailed Results")
            
            # Add percentile ranks
            results_df['Risk_Percentile'] = results_df['Predicted_Probability'].rank(pct=True) * 100
            
            # Format for display
            display_df = results_df.copy()
            display_df['Predicted_Probability'] = (display_df['Predicted_Probability'] * 100).round(2)
            display_df['Risk_Percentile'] = display_df['Risk_Percentile'].round(1)
            
            # Sort by predicted probability (highest risk first)
            display_df = display_df.sort_values('Predicted_Probability', ascending=False)
            
            # Show top risky loans
            st.write("**Top 20 Highest Risk Loans:**")
            st.dataframe(
                display_df.head(20)[['Loan_Index', 'Predicted_Probability', 'Actual_Default', 'Risk_Level', 'Risk_Percentile']],
                use_container_width=True,
                hide_index=True
            )

# Export predictions
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Export Predictions")

if st.sidebar.button("Generate Full Dataset Predictions"):
    with st.spinner("Generating predictions for full dataset..."):
        full_predictions = st.session_state.ml_models.predict_default_probability(
            selected_model, X
        )
        
        if full_predictions is not None:
            # Create export dataframe
            export_df = df_raw.copy()
            export_df['Predicted_Default_Probability'] = full_predictions
            export_df['Risk_Level'] = pd.cut(
                full_predictions,
                bins=[0, 0.1, 0.25, 0.5, 1.0],
                labels=['Low', 'Medium', 'High', 'Very High']
            )
            
            csv = export_df.to_csv(index=False)
            st.sidebar.download_button(
                label="📄 Download Predictions CSV",
                data=csv,
                file_name=f"loan_predictions_{selected_model}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            st.sidebar.success("Predictions generated successfully!")

# Model performance on current data
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Current Model Performance")

current_result = st.session_state.model_results[selected_model]
st.sidebar.metric("AUC Score", f"{current_result['auc_score']:.3f}")
st.sidebar.metric("Average Precision", f"{current_result['avg_precision']:.3f}")
st.sidebar.metric("CV Mean", f"{current_result['cv_mean']:.3f}")
