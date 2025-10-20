import pandas as pd
import numpy as np
import pickle
import json
import os
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.metrics import precision_recall_curve, average_precision_score
from sklearn.feature_selection import RFE, SelectKBest, f_classif, mutual_info_classif
import xgboost as xgb
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from lime.lime_tabular import LimeTabularExplainer

class MLModels:
    def __init__(self):
        self.models = {}
        self.model_results = {}
        self.feature_importance = {}
        self.selected_features = None
        self.feature_selection_results = {}
        self.scaler = None
        
    def perform_feature_selection(self, X, y, method='rfe', n_features=10, random_state=42):
        """
        Perform feature selection using various methods
        
        Parameters:
        -----------
        X : DataFrame
            Feature matrix
        y : Series
            Target variable
        method : str
            Feature selection method ('rfe', 'kbest_f', 'kbest_mi', 'importance')
        n_features : int
            Number of features to select
        random_state : int
            Random state for reproducibility
        """
        
        if method == 'rfe':
            # Recursive Feature Elimination
            estimator = RandomForestClassifier(n_estimators=50, random_state=random_state, n_jobs=-1)
            selector = RFE(estimator, n_features_to_select=n_features, step=1)
            selector.fit(X, y)
            
            selected_mask = selector.support_
            feature_ranking = selector.ranking_
            
            results_df = pd.DataFrame({
                'feature': X.columns,
                'selected': selected_mask,
                'ranking': feature_ranking
            }).sort_values('ranking')
            
            self.feature_selection_results[method] = {
                'selector': selector,
                'results': results_df,
                'selected_features': X.columns[selected_mask].tolist()
            }
            
        elif method == 'kbest_f':
            # SelectKBest with F-statistic
            selector = SelectKBest(f_classif, k=n_features)
            selector.fit(X, y)
            
            selected_mask = selector.get_support()
            scores = selector.scores_
            
            results_df = pd.DataFrame({
                'feature': X.columns,
                'selected': selected_mask,
                'score': scores
            }).sort_values('score', ascending=False)
            
            self.feature_selection_results[method] = {
                'selector': selector,
                'results': results_df,
                'selected_features': X.columns[selected_mask].tolist()
            }
            
        elif method == 'kbest_mi':
            # SelectKBest with Mutual Information
            selector = SelectKBest(mutual_info_classif, k=n_features)
            selector.fit(X, y)
            
            selected_mask = selector.get_support()
            scores = selector.scores_
            
            results_df = pd.DataFrame({
                'feature': X.columns,
                'selected': selected_mask,
                'score': scores
            }).sort_values('score', ascending=False)
            
            self.feature_selection_results[method] = {
                'selector': selector,
                'results': results_df,
                'selected_features': X.columns[selected_mask].tolist()
            }
            
        elif method == 'importance':
            # Feature importance from Random Forest
            rf = RandomForestClassifier(n_estimators=100, random_state=random_state, n_jobs=-1)
            rf.fit(X, y)
            
            importance_df = pd.DataFrame({
                'feature': X.columns,
                'importance': rf.feature_importances_
            }).sort_values('importance', ascending=False)
            
            selected_features = importance_df.head(n_features)['feature'].tolist()
            selected_mask = X.columns.isin(selected_features)
            
            importance_df['selected'] = importance_df['feature'].isin(selected_features)
            
            self.feature_selection_results[method] = {
                'selector': rf,
                'results': importance_df,
                'selected_features': selected_features
            }
        
        # Store the selected features
        self.selected_features = self.feature_selection_results[method]['selected_features']
        
        return self.feature_selection_results[method]
    
    def plot_feature_selection_results(self, method):
        """Plot feature selection results"""
        if method not in self.feature_selection_results:
            return None
        
        results = self.feature_selection_results[method]['results']
        
        if method == 'rfe':
            # Plot RFE ranking
            fig = px.bar(
                results.head(20),
                x='ranking',
                y='feature',
                orientation='h',
                title=f'Feature Ranking (RFE) - Top 20',
                labels={'ranking': 'Rank', 'feature': 'Features'},
                color='selected',
                color_discrete_map={True: 'green', False: 'lightgray'}
            )
        else:
            # Plot scores for KBest methods
            score_col = 'score' if 'score' in results.columns else 'importance'
            fig = px.bar(
                results.head(20),
                x=score_col,
                y='feature',
                orientation='h',
                title=f'Feature Scores ({method}) - Top 20',
                labels={score_col: 'Score', 'feature': 'Features'},
                color='selected',
                color_discrete_map={True: 'green', False: 'lightgray'}
            )
        
        fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
        return fig
        
    def train_models(self, X, y, test_size=0.2, random_state=42, use_selected_features=False, selected_models=None):
        """Train multiple ML models"""
        
        # Use selected features if available and requested
        if use_selected_features and self.selected_features is not None:
            X_filtered = X[self.selected_features]
            st.info(f"Using {len(self.selected_features)} selected features for training")
        else:
            X_filtered = X
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X_filtered, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Handle class imbalance with SMOTE
        smote = SMOTE(random_state=random_state)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
        
        # Scale data for neural network
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        X_train_balanced_scaled = scaler.transform(X_train_balanced)
        
        # Initialize models
        models = {
            'Random Forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=random_state,
                n_jobs=-1
            ),
            'XGBoost': xgb.XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=random_state,
                eval_metric='logloss'
            ),
            'Logistic Regression': LogisticRegression(
                random_state=random_state,
                max_iter=1000
            ),
            'Neural Network': MLPClassifier(
                hidden_layer_sizes=(100, 50),
                activation='relu',
                solver='adam',
                alpha=0.0001,
                batch_size='auto',
                learning_rate='adaptive',
                learning_rate_init=0.001,
                max_iter=300,
                random_state=random_state,
                early_stopping=True,
                validation_fraction=0.1,
                n_iter_no_change=10
            ),
            'KNN': KNeighborsClassifier(
                n_neighbors=5,
                weights='uniform',
                algorithm='auto',
                leaf_size=30,
                p=2,
                metric='minkowski',
                n_jobs=-1
            ),
            'Decision Tree': DecisionTreeClassifier(
                criterion='gini',
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=random_state,
                class_weight='balanced'
            )
        }
        
        # Train and evaluate models
        results = {}
        
        # Filter models based on selection
        models_to_train = {k: v for k, v in models.items() if selected_models is None or k in selected_models}
        
        for name, model in models_to_train.items():
            st.info(f"Training {name}...")
            
            # Train model with appropriate data
            if name in ['Neural Network', 'Logistic Regression', 'KNN']:
                # These models need scaled data and balanced classes
                model.fit(X_train_balanced_scaled, y_train_balanced)
                y_pred = model.predict(X_test_scaled)
                y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
            elif name == 'Decision Tree':
                # Decision Tree with balanced classes (already has class_weight='balanced')
                model.fit(X_train_balanced, y_train_balanced)
                y_pred = model.predict(X_test)
                y_pred_proba = model.predict_proba(X_test)[:, 1]
            else:
                # Tree-based models (RF, XGBoost) use original data with class_weight
                if hasattr(model, 'class_weight'):
                    model.set_params(class_weight='balanced')
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            # Calculate metrics
            auc_score = roc_auc_score(y_test, y_pred_proba)
            avg_precision = average_precision_score(y_test, y_pred_proba)
            
            # Cross-validation score with proper preprocessing
            if name in ['Neural Network', 'Logistic Regression', 'KNN']:
                # Create pipeline with scaler for models that need scaling
                cv_pipeline = Pipeline([
                    ('scaler', StandardScaler()),
                    ('model', model)
                ])
                # Use balanced data for CV
                cv_scores = cross_val_score(
                    cv_pipeline, X_train_balanced, y_train_balanced, 
                    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state),
                    scoring='roc_auc'
                )
            elif name == 'Decision Tree':
                # Decision Tree with balanced data but no scaling
                cv_scores = cross_val_score(
                    model, X_train_balanced, y_train_balanced, 
                    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state),
                    scoring='roc_auc'
                )
            else:
                # Tree-based models (RF, XGBoost) don't need scaling
                cv_scores = cross_val_score(
                    model, X_train, y_train, 
                    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state),
                    scoring='roc_auc'
                )
            
            results[name] = {
                'model': model,
                'auc_score': auc_score,
                'avg_precision': avg_precision,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'y_test': y_test,
                'y_pred': y_pred,
                'y_pred_proba': y_pred_proba,
                'classification_report': classification_report(y_test, y_pred, output_dict=True)
            }
            
            # Feature importance
            if hasattr(model, 'feature_importances_'):
                importance_df = pd.DataFrame({
                    'feature': X_filtered.columns,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False)
                results[name]['feature_importance'] = importance_df
            
            st.success(f"{name} training completed! AUC: {auc_score:.3f}")
        
        self.models = {name: result['model'] for name, result in results.items()}
        self.model_results = results
        self.scaler = scaler  # Store scaler for predictions
        
        return results
    
    def plot_roc_curves(self, results):
        """Plot ROC curves for all models"""
        fig = go.Figure()
        
        for name, result in results.items():
            fpr, tpr, _ = roc_curve(result['y_test'], result['y_pred_proba'])
            
            fig.add_trace(go.Scatter(
                x=fpr, y=tpr,
                mode='lines',
                name=f'{name} (AUC = {result["auc_score"]:.3f})',
                line=dict(width=2)
            ))
        
        # Add diagonal line
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1],
            mode='lines',
            name='Random Classifier',
            line=dict(dash='dash', color='gray')
        ))
        
        fig.update_layout(
            title='ROC Curves Comparison',
            xaxis_title='False Positive Rate',
            yaxis_title='True Positive Rate',
            width=800,
            height=600
        )
        
        return fig
    
    def plot_precision_recall_curves(self, results):
        """Plot Precision-Recall curves for all models"""
        fig = go.Figure()
        
        for name, result in results.items():
            precision, recall, _ = precision_recall_curve(result['y_test'], result['y_pred_proba'])
            
            fig.add_trace(go.Scatter(
                x=recall, y=precision,
                mode='lines',
                name=f'{name} (AP = {result["avg_precision"]:.3f})',
                line=dict(width=2)
            ))
        
        fig.update_layout(
            title='Precision-Recall Curves Comparison',
            xaxis_title='Recall',
            yaxis_title='Precision',
            width=800,
            height=600
        )
        
        return fig
    
    def plot_confusion_matrices(self, results):
        """Plot confusion matrices for all models"""
        n_models = len(results)
        cols = min(3, n_models)
        rows = (n_models + cols - 1) // cols
        
        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=list(results.keys()),
            specs=[[{'type': 'heatmap'} for _ in range(cols)] for _ in range(rows)]
        )
        
        for idx, (name, result) in enumerate(results.items()):
            row = idx // cols + 1
            col = idx % cols + 1
            
            cm = confusion_matrix(result['y_test'], result['y_pred'])
            
            fig.add_trace(
                go.Heatmap(
                    z=cm,
                    x=['Predicted 0', 'Predicted 1'],
                    y=['Actual 0', 'Actual 1'],
                    colorscale='Blues',
                    showscale=False,
                    text=cm,
                    texttemplate="%{text}",
                    textfont={"size": 12}
                ),
                row=row, col=col
            )
        
        fig.update_layout(
            title='Confusion Matrices Comparison',
            height=300 * rows
        )
        
        return fig
    
    def plot_feature_importance(self, model_name):
        """Plot feature importance for a specific model"""
        if model_name not in self.model_results:
            return None
        
        if 'feature_importance' not in self.model_results[model_name]:
            return None
        
        importance_df = self.model_results[model_name]['feature_importance'].head(15)
        
        fig = px.bar(
            importance_df,
            x='importance',
            y='feature',
            orientation='h',
            title=f'Feature Importance - {model_name}',
            labels={'importance': 'Importance Score', 'feature': 'Features'}
        )
        
        fig.update_layout(
            height=500,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def predict_default_probability(self, model_name, X):
        """Predict default probability for new data"""
        if model_name not in self.models:
            return None
        
        model = self.models[model_name]
        
        # Scale data for Neural Network and Logistic Regression
        if model_name in ['Neural Network', 'Logistic Regression'] and self.scaler is not None:
            X_processed = self.scaler.transform(X)
        else:
            X_processed = X
        
        probabilities = model.predict_proba(X_processed)[:, 1]
        
        return probabilities
    
    def analyze_approval_levels(self, model_name, X, y, approval_thresholds=[0.1, 0.2, 0.3, 0.4, 0.5]):
        """Analyze expected default rates at different approval levels"""
        if model_name not in self.models:
            return None
        
        model = self.models[model_name]
        
        # Scale data for Neural Network and Logistic Regression
        if model_name in ['Neural Network', 'Logistic Regression'] and self.scaler is not None:
            X_processed = self.scaler.transform(X)
        else:
            X_processed = X
        
        probabilities = model.predict_proba(X_processed)[:, 1]
        
        results = []
        
        for threshold in approval_thresholds:
            # Loans that would be approved (low predicted probability)
            approved_mask = probabilities <= threshold
            
            if approved_mask.sum() == 0:
                continue
            
            approved_loans = approved_mask.sum()
            total_loans = len(X)
            approval_rate = (approved_loans / total_loans) * 100
            
            # Actual default rate among approved loans
            actual_defaults = y[approved_mask].sum()
            actual_default_rate = (actual_defaults / approved_loans) * 100 if approved_loans > 0 else 0
            
            # Expected revenue/loss calculation (simplified)
            expected_revenue = approved_loans * 1000  # Assume $1000 revenue per loan
            expected_loss = actual_defaults * 5000     # Assume $5000 loss per default
            net_expected_value = expected_revenue - expected_loss
            
            results.append({
                'threshold': threshold,
                'approval_rate': approval_rate,
                'approved_loans': approved_loans,
                'actual_default_rate': actual_default_rate,
                'expected_defaults': actual_defaults,
                'expected_revenue': expected_revenue,
                'expected_loss': expected_loss,
                'net_expected_value': net_expected_value,
                'roi': (net_expected_value / expected_revenue) * 100 if expected_revenue > 0 else 0
            })
        
        return pd.DataFrame(results)
    
    def get_model_comparison(self):
        """Get comparison table of all models"""
        if not self.model_results:
            return None
        
        comparison_data = []
        
        for name, result in self.model_results.items():
            comparison_data.append({
                'Model': name,
                'AUC Score': f"{result['auc_score']:.3f}",
                'Average Precision': f"{result['avg_precision']:.3f}",
                'CV Mean': f"{result['cv_mean']:.3f}",
                'CV Std': f"{result['cv_std']:.3f}",
                'Precision': f"{result['classification_report']['1']['precision']:.3f}",
                'Recall': f"{result['classification_report']['1']['recall']:.3f}",
                'F1-Score': f"{result['classification_report']['1']['f1-score']:.3f}"
            })
        
        return pd.DataFrame(comparison_data)
    
    def create_lime_explainer(self, X_train, feature_names, class_names=['No Default', 'Default']):
        """Create a LIME explainer for the training data"""
        explainer = LimeTabularExplainer(
            X_train.values if isinstance(X_train, pd.DataFrame) else X_train,
            feature_names=feature_names,
            class_names=class_names,
            mode='classification',
            random_state=42
        )
        return explainer
    
    def explain_prediction(self, model_name, explainer, instance, feature_names, num_features=10):
        """
        Generate LIME explanation for a single prediction
        
        Parameters:
        -----------
        model_name : str
            Name of the model to explain
        explainer : LimeTabularExplainer
            LIME explainer object
        instance : array-like
            Single instance to explain
        feature_names : list
            List of feature names
        num_features : int
            Number of top features to show
        
        Returns:
        --------
        dict with explanation data
        """
        if model_name not in self.models:
            return None
        
        model = self.models[model_name]
        
        # Create prediction function that handles scaling
        def predict_fn(X):
            if model_name in ['Neural Network', 'Logistic Regression'] and self.scaler is not None:
                X_scaled = self.scaler.transform(X)
                return model.predict_proba(X_scaled)
            return model.predict_proba(X)
        
        # Get explanation
        exp = explainer.explain_instance(
            instance.flatten() if len(instance.shape) > 1 else instance,
            predict_fn,
            num_features=num_features
        )
        
        # Extract feature contributions
        feature_weights = exp.as_list()
        
        # Get prediction probabilities
        if model_name in ['Neural Network', 'Logistic Regression'] and self.scaler is not None:
            instance_scaled = self.scaler.transform(instance.reshape(1, -1))
            proba = model.predict_proba(instance_scaled)[0]
        else:
            proba = model.predict_proba(instance.reshape(1, -1))[0]
        
        return {
            'feature_weights': feature_weights,
            'prediction_proba': proba,
            'prediction': 'Default' if proba[1] > 0.5 else 'No Default',
            'explanation_object': exp
        }
    
    def plot_lime_explanation(self, explanation_data):
        """Create a plotly visualization of LIME explanation"""
        if explanation_data is None:
            return None
        
        # Extract features and weights
        features = [item[0] for item in explanation_data['feature_weights']]
        weights = [item[1] for item in explanation_data['feature_weights']]
        
        # Create color based on positive/negative contribution
        colors = ['green' if w > 0 else 'red' for w in weights]
        
        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=weights,
                y=features,
                orientation='h',
                marker_color=colors,
                text=[f'{w:.3f}' for w in weights],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Feature Contributions to Prediction (LIME)',
            xaxis_title='Contribution to Default Prediction',
            yaxis_title='Features',
            height=400,
            showlegend=False
        )
        
        return fig
    
    def get_global_feature_importance(self, model_name, explainer, X_sample, feature_names, num_samples=100):
        """
        Get global feature importance by averaging LIME explanations across multiple samples
        
        Parameters:
        -----------
        model_name : str
            Name of the model
        explainer : LimeTabularExplainer
            LIME explainer object
        X_sample : array-like
            Sample of instances to explain
        feature_names : list
            List of feature names
        num_samples : int
            Number of samples to use for global importance
        
        Returns:
        --------
        DataFrame with global feature importance
        """
        if model_name not in self.models:
            return None
        
        # Sample random instances
        n_instances = min(num_samples, len(X_sample))
        indices = np.random.choice(len(X_sample), n_instances, replace=False)
        
        # Collect feature importances
        feature_importances = {feature: [] for feature in feature_names}
        
        for idx in indices:
            instance = X_sample[idx]
            exp_data = self.explain_prediction(model_name, explainer, instance, feature_names)
            
            if exp_data is not None:
                for feature, weight in exp_data['feature_weights']:
                    # Extract just the feature name if it contains conditions
                    base_feature = feature.split('<=')[0].split('>')[0].strip()
                    if base_feature in feature_importances:
                        feature_importances[base_feature].append(abs(weight))
        
        # Calculate average absolute importance
        avg_importance = {
            feature: np.mean(weights) if weights else 0
            for feature, weights in feature_importances.items()
        }
        
        # Create DataFrame and sort
        importance_df = pd.DataFrame({
            'Feature': list(avg_importance.keys()),
            'Average Importance': list(avg_importance.values())
        }).sort_values('Average Importance', ascending=False)
        
        return importance_df
    
    def save_models(self, filepath='models/saved_models.pkl', save_metadata=True):
        """
        Save trained models, scaler, and metadata to disk
        
        Parameters:
        -----------
        filepath : str
            Path to save the models
        save_metadata : bool
            Whether to save metadata alongside models
        """
        import os
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_package = {
            'models': self.models,
            'scaler': self.scaler,
            'selected_features': self.selected_features,
            'model_results': {
                name: {
                    'auc_score': result['auc_score'],
                    'avg_precision': result['avg_precision'],
                    'cv_mean': result['cv_mean'],
                    'cv_std': result['cv_std'],
                    'y_test': result.get('y_test'),
                    'y_pred': result.get('y_pred'),
                    'y_pred_proba': result.get('y_pred_proba'),
                    'classification_report': result.get('classification_report'),
                    'feature_importance': result.get('feature_importance')
                } for name, result in self.model_results.items()
            } if self.model_results else {},
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_package, f)
        
        if save_metadata:
            metadata = {
                'models': list(self.models.keys()),
                'features': self.selected_features if self.selected_features else 'all',
                'num_features': len(self.selected_features) if self.selected_features else 0,
                'scaler_used': self.scaler is not None,
                'timestamp': datetime.now().isoformat(),
                'performance': {
                    name: {
                        'auc': float(result['auc_score']),
                        'avg_precision': float(result['avg_precision']),
                        'cv_mean': float(result['cv_mean']),
                        'cv_std': float(result['cv_std'])
                    } for name, result in self.model_results.items()
                } if self.model_results else {}
            }
            
            metadata_path = filepath.replace('.pkl', '_metadata.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
        
        return filepath
    
    def load_models(self, filepath='models/saved_models.pkl'):
        """
        Load trained models from disk
        
        Parameters:
        -----------
        filepath : str
            Path to the saved models file
        """
        with open(filepath, 'rb') as f:
            model_package = pickle.load(f)
        
        self.models = model_package['models']
        self.scaler = model_package['scaler']
        self.selected_features = model_package['selected_features']
        
        if 'model_results' in model_package:
            self.model_results = model_package['model_results']
        
        return model_package
    
    def export_prediction_script(self, model_name, filepath='deployment/predict.py'):
        """
        Export a standalone prediction script for deployment
        
        Parameters:
        -----------
        model_name : str
            Name of the model to export
        filepath : str
            Path to save the prediction script
        """
        import os
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        needs_scaling = model_name in ['Neural Network', 'Logistic Regression']
        
        script_content = f'''"""
Standalone Prediction Script for {model_name}
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

This script loads the trained model and makes predictions on new data.
"""

import pickle
import pandas as pd
import numpy as np

def load_model(model_path='../models/saved_models.pkl'):
    """Load the trained model and scaler"""
    with open(model_path, 'rb') as f:
        model_package = pickle.load(f)
    
    model = model_package['models']['{model_name}']
    scaler = model_package['scaler']
    selected_features = model_package['selected_features']
    
    return model, scaler, selected_features

def predict(data, model_path='../models/saved_models.pkl'):
    """
    Make predictions on new data
    
    Parameters:
    -----------
    data : pandas DataFrame or dict
        Input features for prediction
    model_path : str
        Path to saved model file
    
    Returns:
    --------
    dict with predictions and probabilities
    """
    # Load model
    model, scaler, selected_features = load_model(model_path)
    
    # Convert to DataFrame if dict
    if isinstance(data, dict):
        data = pd.DataFrame([data])
    
    # Filter to selected features if applicable
    if selected_features:
        data = data[selected_features]
    
    # Scale data if needed
    needs_scaling = {str(needs_scaling).lower()}
    if needs_scaling and scaler is not None:
        X = scaler.transform(data)
    else:
        X = data.values if isinstance(data, pd.DataFrame) else data
    
    # Make predictions
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)
    
    results = []
    for i, (pred, proba) in enumerate(zip(predictions, probabilities)):
        results.append({{
            'prediction': 'Default' if pred == 1 else 'No Default',
            'default_probability': float(proba[1]),
            'no_default_probability': float(proba[0]),
            'risk_level': 'High' if proba[1] > 0.7 else 'Medium' if proba[1] > 0.3 else 'Low'
        }})
    
    return results

def predict_batch(csv_path, output_path='predictions.csv', model_path='../models/saved_models.pkl'):
    """
    Make predictions on a batch of data from CSV
    
    Parameters:
    -----------
    csv_path : str
        Path to input CSV file
    output_path : str
        Path to save predictions
    model_path : str
        Path to saved model file
    """
    # Load data
    data = pd.read_csv(csv_path)
    
    # Make predictions
    results = predict(data, model_path)
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    output_df = pd.concat([data, results_df], axis=1)
    
    # Save results
    output_df.to_csv(output_path, index=False)
    print(f"Predictions saved to {{output_path}}")
    
    return output_df

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python predict.py <input.csv> [output.csv]")
        print("\\nExample:")
        print("  python predict.py new_loans.csv predictions.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'predictions.csv'
    
    predict_batch(input_file, output_file)
    print("\\nPredictions completed successfully!")
'''
        
        with open(filepath, 'w') as f:
            f.write(script_content)
        
        return filepath
    
    def save_performance_history(self, filepath='models/performance_history.json'):
        """
        Save model performance metrics to historical log
        
        Parameters:
        -----------
        filepath : str
            Path to the performance history file
        """
        import os
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Create performance record
        performance_record = {
            'timestamp': datetime.now().isoformat(),
            'models': {}
        }
        
        for name, result in self.model_results.items():
            performance_record['models'][name] = {
                'auc_score': float(result['auc_score']),
                'avg_precision': float(result['avg_precision']),
                'cv_mean': float(result['cv_mean']),
                'cv_std': float(result['cv_std']),
                'precision': float(result['classification_report']['1']['precision']),
                'recall': float(result['classification_report']['1']['recall']),
                'f1_score': float(result['classification_report']['1']['f1-score'])
            }
        
        # Load existing history or create new
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                history = json.load(f)
        else:
            history = {'records': []}
        
        # Append new record
        history['records'].append(performance_record)
        
        # Save updated history
        with open(filepath, 'w') as f:
            json.dump(history, f, indent=2)
        
        return filepath
    
    def load_performance_history(self, filepath='models/performance_history.json'):
        """
        Load historical performance metrics
        
        Parameters:
        -----------
        filepath : str
            Path to the performance history file
        
        Returns:
        --------
        dict with historical records
        """
        if not os.path.exists(filepath):
            return {'records': []}
        
        with open(filepath, 'r') as f:
            history = json.load(f)
        
        return history
    
    def plot_performance_trends(self, history, metric='auc_score'):
        """
        Plot performance trends over time
        
        Parameters:
        -----------
        history : dict
            Performance history data
        metric : str
            Metric to plot (auc_score, avg_precision, etc.)
        """
        import plotly.graph_objects as go
        from datetime import datetime
        
        if not history.get('records'):
            return None
        
        fig = go.Figure()
        
        # Get all unique models
        all_models = set()
        for record in history['records']:
            all_models.update(record['models'].keys())
        
        # Plot each model's trend
        for model_name in all_models:
            timestamps = []
            values = []
            
            for record in history['records']:
                if model_name in record['models']:
                    timestamps.append(record['timestamp'])
                    values.append(record['models'][model_name].get(metric, 0))
            
            fig.add_trace(go.Scatter(
                x=timestamps,
                y=values,
                mode='lines+markers',
                name=model_name,
                line=dict(width=2),
                marker=dict(size=8)
            ))
        
        metric_names = {
            'auc_score': 'AUC Score',
            'avg_precision': 'Average Precision',
            'cv_mean': 'CV Mean Score',
            'precision': 'Precision',
            'recall': 'Recall',
            'f1_score': 'F1 Score'
        }
        
        fig.update_layout(
            title=f'{metric_names.get(metric, metric)} Over Time',
            xaxis_title='Date',
            yaxis_title=metric_names.get(metric, metric),
            hovermode='x unified',
            height=400
        )
        
        return fig
    
    def compare_with_baseline(self, baseline_results):
        """
        Compare current models with baseline performance
        
        Parameters:
        -----------
        baseline_results : dict
            Baseline model results to compare against
        
        Returns:
        --------
        DataFrame with comparison
        """
        if not self.model_results or not baseline_results:
            return None
        
        comparison_data = []
        
        for name in self.model_results.keys():
            if name in baseline_results:
                current = self.model_results[name]
                baseline = baseline_results[name]
                
                comparison_data.append({
                    'Model': name,
                    'Current AUC': f"{current['auc_score']:.3f}",
                    'Baseline AUC': f"{baseline.get('auc_score', 0):.3f}",
                    'AUC Change': f"{(current['auc_score'] - baseline.get('auc_score', 0)):.3f}",
                    'Current Precision': f"{current['classification_report']['1']['precision']:.3f}",
                    'Baseline Precision': f"{baseline.get('classification_report', {}).get('1', {}).get('precision', 0):.3f}",
                    'Status': '📈 Improved' if current['auc_score'] > baseline.get('auc_score', 0) else '📉 Declined' if current['auc_score'] < baseline.get('auc_score', 0) else '➡️ Same'
                })
        
        return pd.DataFrame(comparison_data) if comparison_data else None
