"""
Data Quality Scorer
Evaluates datasets across 5 dimensions:
- Completeness (50%)
- Consistency (20%)
- Uniqueness (6%)
- Validity (15%)
- Correctness (9%)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class QualityScore:
    completeness: float
    consistency: float
    uniqueness: float
    validity: float
    correctness: float
    
    @property
    def overall(self) -> float:
        """Calculate weighted overall score"""
        return (
            self.completeness * 0.50 +
            self.consistency * 0.20 +
            self.uniqueness * 0.06 +
            self.validity * 0.15 +
            self.correctness * 0.09
        )
    
    def to_dict(self) -> Dict[str, float]:
        return {
            'completeness': self.completeness,
            'consistency': self.consistency,
            'uniqueness': self.uniqueness,
            'validity': self.validity,
            'correctness': self.correctness,
            'overall': self.overall
        }


class DataQualityScorer:
    """Analyzes dataset quality across multiple dimensions"""
    
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        self.issues = []
    
    def score_completeness(self) -> float:
        """
        Score based on missing values
        100% = no missing values
        """
        missing_ratio = self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))
        completeness = (1 - missing_ratio) * 100
        
        if missing_ratio > 0:
            self.issues.append(f"Missing values: {missing_ratio*100:.2f}%")
        
        return completeness
    
    def score_consistency(self) -> float:
        """
        Score based on naming conventions and format uniformity
        """
        consistency_score = 100
        
        # Check column naming consistency
        col_names = self.df.columns.tolist()
        naming_styles = self._detect_naming_style(col_names)
        if len(naming_styles) > 1:
            consistency_score -= 20
            self.issues.append(f"Inconsistent column naming: {naming_styles}")
        
        # Check data type consistency per column
        for col in self.df.columns:
            unique_types = len(set(type(x).__name__ for x in self.df[col]))
            if unique_types > 1:
                consistency_score -= 5
                self.issues.append(f"Mixed data types in column '{col}'")
        
        return max(consistency_score, 0)
    
    def score_uniqueness(self) -> float:
        """
        Score based on duplicate records and columns
        """
        uniqueness_score = 100
        
        # Check duplicate rows
        dup_ratio = self.df.duplicated().sum() / len(self.df)
        uniqueness_score -= dup_ratio * 50
        
        if dup_ratio > 0:
            self.issues.append(f"Duplicate rows: {dup_ratio*100:.2f}%")
        
        # Check redundant columns (highly correlated)
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr_matrix = self.df[numeric_cols].corr()
            high_corr = (corr_matrix > 0.95).sum().sum() - len(numeric_cols)
            if high_corr > 0:
                uniqueness_score -= high_corr * 10
                self.issues.append(f"Redundant columns detected: {high_corr} highly correlated")
        
        return max(uniqueness_score, 0)
    
    def score_validity(self) -> float:
        """
        Score based on data type correctness and format validation
        """
        validity_score = 100
        
        for col in self.df.columns:
            # Check for malformed values
            if self.df[col].dtype == 'object':
                # Try to detect inconsistent formatting
                sample = self.df[col].dropna().head(100)
                if len(sample) > 0:
                    lengths = sample.astype(str).str.len()
                    if lengths.std() > lengths.mean() * 0.5:
                        validity_score -= 5
                        self.issues.append(f"Inconsistent format in '{col}'")
        
        return max(validity_score, 0)
    
    def score_correctness(self) -> float:
        """
        Score based on logical errors and data accuracy
        """
        correctness_score = 100
        
        # Check for impossible values
        for col in self.df.columns:
            if self.df[col].dtype in ['int64', 'float64']:
                # Check for negative values that shouldn't be negative
                if (self.df[col] < 0).any():
                    correctness_score -= 10
                    self.issues.append(f"Negative values in '{col}' (may be invalid)")
        
        return max(correctness_score, 0)
    
    def _detect_naming_style(self, names: List[str]) -> List[str]:
        """Detect naming conventions (snake_case, camelCase, PascalCase, etc)"""
        styles = []
        for name in names:
            if '_' in name:
                styles.append('snake_case')
            elif name[0].isupper():
                styles.append('PascalCase')
            elif any(c.isupper() for c in name[1:]):
                styles.append('camelCase')
            else:
                styles.append('lowercase')
        return list(set(styles))
    
    def get_score(self) -> QualityScore:
        """Calculate overall quality score"""
        return QualityScore(
            completeness=self.score_completeness(),
            consistency=self.score_consistency(),
            uniqueness=self.score_uniqueness(),
            validity=self.score_validity(),
            correctness=self.score_correctness()
        )
    
    def get_issues(self) -> List[str]:
        """Get list of detected issues"""
        return self.issues
    
    def generate_report(self) -> str:
        """Generate a quality report"""
        score = self.get_score()
        report = f"""
╔════════════════════════════════════════╗
║        DATA QUALITY REPORT              ║
╚════════════════════════════════════════╝

Dataset Shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns

QUALITY SCORES:
────────────────────────────────────────
Completeness       {score.completeness:>6.1f}%
Consistency        {score.consistency:>6.1f}%
Uniqueness         {score.uniqueness:>6.1f}%
Validity           {score.validity:>6.1f}%
Correctness        {score.correctness:>6.1f}%
────────────────────────────────────────
Overall            {score.overall:>6.1f}%

ISSUES DETECTED:
────────────────────────────────────────
"""
        if self.issues:
            for i, issue in enumerate(self.issues, 1):
                report += f"{i}. {issue}\n"
        else:
            report += "No issues detected!\n"
        
        return report
