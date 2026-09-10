"""
Dataset Simplification Engine
Automatic data cleaning and transformation
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple


class DataSimplifier:
    """Automatically cleans and simplifies datasets"""
    
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()
        self.original_df = dataframe.copy()
        self.transformations = []
    
    def remove_duplicates(self, subset: List[str] = None, keep: str = 'first') -> 'DataSimplifier':
        """Remove duplicate rows"""
        original_rows = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset, keep=keep)
        removed = original_rows - len(self.df)
        self.transformations.append(f"Removed {removed} duplicate rows")
        return self
    
    def remove_redundant_columns(self, threshold: float = 0.95) -> 'DataSimplifier':
        """Remove highly correlated columns"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr_matrix = self.df[numeric_cols].corr().abs()
            upper_triangle = corr_matrix.where(
                np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
            )
            to_drop = [col for col in upper_triangle.columns if any(upper_triangle[col] > threshold)]
            self.df = self.df.drop(columns=to_drop)
            self.transformations.append(f"Removed {len(to_drop)} redundant columns")
        return self
    
    def handle_missing_values(self, strategy: str = 'drop', fill_value=None) -> 'DataSimplifier':
        """Handle missing values"""
        if strategy == 'drop':
            original_rows = len(self.df)
            self.df = self.df.dropna()
            removed = original_rows - len(self.df)
            self.transformations.append(f"Removed {removed} rows with missing values")
        elif strategy == 'fill':
            self.df = self.df.fillna(fill_value)
            self.transformations.append(f"Filled missing values with {fill_value}")
        elif strategy == 'mean':
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                self.df[col].fillna(self.df[col].mean(), inplace=True)
            self.transformations.append("Filled numeric columns with mean values")
        return self
    
    def standardize_column_names(self) -> 'DataSimplifier':
        """Standardize column naming to snake_case"""
        def to_snake_case(name):
            s1 = ''.join([c if c.islower() or c.isdigit() else f'_{c.lower()}' for c in str(name)])
            return s1.lstrip('_').replace(' ', '_')
        
        new_cols = {col: to_snake_case(col) for col in self.df.columns}
        self.df = self.df.rename(columns=new_cols)
        self.transformations.append("Standardized column names to snake_case")
        return self
    
    def remove_unnecessary_columns(self, columns_to_drop: List[str]) -> 'DataSimplifier':
        """Remove specified columns"""
        cols_exist = [col for col in columns_to_drop if col in self.df.columns]
        self.df = self.df.drop(columns=cols_exist)
        self.transformations.append(f"Removed {len(cols_exist)} unnecessary columns")
        return self
    
    def consolidate_categories(self, column: str, mapping: Dict[str, str]) -> 'DataSimplifier':
        """Map fragmented categories to consolidated values"""
        if column in self.df.columns:
            self.df[column] = self.df[column].map(mapping).fillna(self.df[column])
            self.transformations.append(f"Consolidated categories in '{column}'")
        return self
    
    def fix_data_types(self, type_mapping: Dict[str, str]) -> 'DataSimplifier':
        """Convert columns to correct data types"""
        for col, dtype in type_mapping.items():
            if col in self.df.columns:
                try:
                    self.df[col] = self.df[col].astype(dtype)
                    self.transformations.append(f"Converted '{col}' to {dtype}")
                except Exception as e:
                    self.transformations.append(f"Failed to convert '{col}' to {dtype}: {e}")
        return self
    
    def clean_whitespace(self) -> 'DataSimplifier':
        """Remove leading/trailing whitespace from string columns"""
        string_cols = self.df.select_dtypes(include=['object']).columns
        for col in string_cols:
            if self.df[col].dtype == 'object':
                self.df[col] = self.df[col].str.strip()
        self.transformations.append("Cleaned whitespace from string columns")
        return self
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """Return the cleaned dataset"""
        return self.df
    
    def get_transformations(self) -> List[str]:
        """Get list of applied transformations"""
        return self.transformations
    
    def generate_summary(self) -> str:
        """Generate a summary of simplification"""
        original_shape = self.original_df.shape
        new_shape = self.df.shape
        
        summary = f"""
╔════════════════════════════════════════╗
║    DATASET SIMPLIFICATION SUMMARY       ║
╚════════════════════════════════════════╝

ORIGINAL DATASET:
  Rows: {original_shape[0]}
  Columns: {original_shape[1]}

CLEANED DATASET:
  Rows: {new_shape[0]}
  Columns: {new_shape[1]}

REDUCTION:
  Rows removed: {original_shape[0] - new_shape[0]}
  Columns removed: {original_shape[1] - new_shape[1]}

TRANSFORMATIONS APPLIED:
────────────────────────────────────────
"""
        for i, transform in enumerate(self.transformations, 1):
            summary += f"{i}. {transform}\n"
        
        return summary
