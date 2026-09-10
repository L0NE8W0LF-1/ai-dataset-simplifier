# AI Dataset Simplifier

An AI-powered tool for dataset quality assessment and automatic data cleaning.

## Features

### Data Quality Scoring

Analyzes datasets across 5 critical dimensions:

- **Completeness (50%)** - Missing values detection
- **Consistency (20%)** - Naming conventions, format uniformity
- **Uniqueness (6%)** - Duplicate records and redundant columns
- **Validity (15%)** - Data type correctness, format validation
- **Correctness (9%)** - Logical errors, impossible values

### Automatic Data Simplification

The tool automatically detects and fixes:

- Redundant columns (highly correlated features)
- Duplicate records
- Inconsistent column naming
- Mixed data types
- Unnecessary fields
- Fragmented categories
- Malformed values
- Missing values

## Installation

```bash
pip install pandas numpy
```

## Quick Start

### Score Dataset Quality

```python
import pandas as pd
from scorer import DataQualityScorer

# Load your dataset
df = pd.read_csv('data.csv')

# Score quality
scorer = DataQualityScorer(df)
report = scorer.generate_report()
print(report)
```

### Simplify Dataset

```python
from simplifier import DataSimplifier

# Initialize simplifier
simplifier = DataSimplifier(df)

# Apply transformations
cleaned_df = (simplifier
    .remove_duplicates()
    .handle_missing_values(strategy='drop')
    .standardize_column_names()
    .clean_whitespace()
    .remove_redundant_columns(threshold=0.95)
    .get_cleaned_data()
)

# View summary
print(simplifier.generate_summary())
```

## Data Transformation Pipeline

```
RAW DATA
   │
   ├── redundant columns
   ├── duplicated records
   ├── inconsistent naming
   ├── mixed data types
   ├── unnecessary fields
   ├── fragmented categories
   └── malformed values
          │
          ▼
SIMPLIFICATION
          │
          ▼
CLEAN DATASET
```

## Quality Score Breakdown

```
DATA QUALITY
────────────────────────
Completeness       50%
Consistency        20%
Uniqueness         6%
Validity           15%
Correctness        9%
────────────────────────
Overall            100%
```

## API Reference

### DataQualityScorer

- `score_completeness()` - Score based on missing values
- `score_consistency()` - Score based on naming and format
- `score_uniqueness()` - Score based on duplicates
- `score_validity()` - Score based on data types
- `score_correctness()` - Score based on logical errors
- `get_score()` - Get overall QualityScore object
- `generate_report()` - Generate formatted quality report

### DataSimplifier

- `remove_duplicates()` - Remove duplicate rows
- `remove_redundant_columns()` - Remove highly correlated columns
- `handle_missing_values()` - Handle NULL/NA values
- `standardize_column_names()` - Convert to snake_case
- `clean_whitespace()` - Strip whitespace from strings
- `consolidate_categories()` - Map fragmented values
- `fix_data_types()` - Convert column types
- `get_cleaned_data()` - Return cleaned dataset
- `generate_summary()` - Generate transformation summary

## License

MIT
