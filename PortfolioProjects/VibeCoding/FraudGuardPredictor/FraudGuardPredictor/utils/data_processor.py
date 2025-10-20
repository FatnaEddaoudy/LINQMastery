import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import streamlit as st

class DataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.imputers = {}
        
    def load_data(self, file_path):
        """Load the loan dataset"""
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return None
    
    def preprocess_data(self, df):
        """Comprehensive data preprocessing"""
        df_processed = df.copy()
        
        # Convert date columns
        date_columns = ['rep_loan_date', 'first_loan', 'first_overdue_date']
        for col in date_columns:
            if col in df_processed.columns:
                df_processed[col] = pd.to_datetime(df_processed[col], errors='coerce')
        
        # Create new features from dates
        if 'rep_loan_date' in df_processed.columns and 'first_loan' in df_processed.columns:
            df_processed['loan_duration'] = (df_processed['rep_loan_date'] - df_processed['first_loan']).dt.days
        
        # Handle categorical variables
        categorical_cols = ['federal_district_nm', 'gender']
        for col in categorical_cols:
            if col in df_processed.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    df_processed[f'{col}_encoded'] = self.label_encoders[col].fit_transform(
                        df_processed[col].fillna('Unknown')
                    )
                else:
                    df_processed[f'{col}_encoded'] = self.label_encoders[col].transform(
                        df_processed[col].fillna('Unknown')
                    )
        
        # Handle numerical features
        numerical_cols = ['dpd_5_cnt', 'dpd_15_cnt', 'dpd_30_cnt', 'close_loans_cnt', 
                         'past_billings_cnt', 'score_1', 'score_2', 'age']
        
        for col in numerical_cols:
            if col in df_processed.columns:
                if col not in self.imputers:
                    self.imputers[col] = SimpleImputer(strategy='median')
                    df_processed[col] = self.imputers[col].fit_transform(
                        df_processed[[col]]
                    ).flatten()
                else:
                    df_processed[col] = self.imputers[col].transform(
                        df_processed[[col]]
                    ).flatten()
        
        # Create aggregate payment features
        payment_cols = ['payment_type_0', 'payment_type_1', 'payment_type_2', 
                       'payment_type_3', 'payment_type_4', 'payment_type_5']
        
        # Total payments
        df_processed['total_payments'] = df_processed[payment_cols].sum(axis=1)
        
        # Payment diversity (number of different payment types used)
        df_processed['payment_diversity'] = (df_processed[payment_cols] > 0).sum(axis=1)
        
        # Risk score based on DPD counts
        dpd_cols = ['dpd_5_cnt', 'dpd_15_cnt', 'dpd_30_cnt']
        df_processed['risk_score'] = df_processed[dpd_cols].fillna(0).sum(axis=1)
        
        # Age groups
        df_processed['age_group'] = pd.cut(
            df_processed['age'], 
            bins=[0, 25, 35, 45, 55, 100], 
            labels=[0, 1, 2, 3, 4]
        ).astype(float)
        
        return df_processed
    
    def get_feature_columns(self, df):
        """Get relevant feature columns for modeling"""
        # Select numerical and encoded categorical features
        feature_cols = [
            'dpd_5_cnt', 'dpd_15_cnt', 'dpd_30_cnt', 'close_loans_cnt',
            'TraderKey', 'payment_type_0', 'payment_type_1', 'payment_type_2',
            'payment_type_3', 'payment_type_4', 'payment_type_5',
            'past_billings_cnt', 'score_1', 'score_2', 'age',
            'total_payments', 'payment_diversity', 'risk_score', 'age_group'
        ]
        
        # Add encoded categorical features
        if 'federal_district_nm_encoded' in df.columns:
            feature_cols.append('federal_district_nm_encoded')
        if 'gender_encoded' in df.columns:
            feature_cols.append('gender_encoded')
        if 'loan_duration' in df.columns:
            feature_cols.append('loan_duration')
        
        # Filter only existing columns
        existing_cols = [col for col in feature_cols if col in df.columns]
        
        return existing_cols
    
    def prepare_modeling_data(self, df):
        """Prepare data specifically for modeling"""
        df_processed = self.preprocess_data(df)
        feature_cols = self.get_feature_columns(df_processed)
        
        # Create feature matrix
        X = df_processed[feature_cols].fillna(0)
        y = df_processed['bad_flag'].fillna(0)
        
        return X, y, feature_cols
    
    def get_data_summary(self, df):
        """Get comprehensive data summary"""
        summary = {
            'total_records': len(df),
            'total_features': len(df.columns),
            'missing_values': df.isnull().sum().sum(),
            'default_rate': df['bad_flag'].mean() if 'bad_flag' in df.columns else 0,
            'date_range': {
                'min_date': df['rep_loan_date'].min() if 'rep_loan_date' in df.columns else None,
                'max_date': df['rep_loan_date'].max() if 'rep_loan_date' in df.columns else None
            }
        }
        
        return summary
