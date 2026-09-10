"""
API Server for Dataset Simplifier
Provides REST endpoints for data quality scoring and simplification
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import io
import json
from scorer import DataQualityScorer
from simplifier import DataSimplifier

app = Flask(__name__)
CORS(app)

# Store uploaded datasets in memory (production should use database)
datasets = {}


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Dataset Simplifier API',
        'version': '1.0.0'
    }), 200


@app.route('/api/upload', methods=['POST'])
def upload_dataset():
    """Upload and store a dataset"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        dataset_name = request.form.get('name', file.filename)
        
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        # Read CSV or Excel file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
        else:
            return jsonify({'error': 'Unsupported file format. Use CSV or Excel'}), 400
        
        datasets[dataset_name] = df
        
        return jsonify({
            'message': f'Dataset "{dataset_name}" uploaded successfully',
            'dataset_name': dataset_name,
            'shape': {'rows': len(df), 'columns': len(df.columns)},
            'columns': df.columns.tolist()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/datasets', methods=['GET'])
def list_datasets():
    """List all uploaded datasets"""
    dataset_info = []
    for name, df in datasets.items():
        dataset_info.append({
            'name': name,
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': df.columns.tolist()
        })
    
    return jsonify({
        'count': len(datasets),
        'datasets': dataset_info
    }), 200


@app.route('/api/score/<dataset_name>', methods=['GET'])
def score_dataset(dataset_name):
    """Score a dataset's quality"""
    try:
        if dataset_name not in datasets:
            return jsonify({'error': f'Dataset "{dataset_name}" not found'}), 404
        
        df = datasets[dataset_name]
        scorer = DataQualityScorer(df)
        score = scorer.get_score()
        issues = scorer.get_issues()
        
        return jsonify({
            'dataset': dataset_name,
            'scores': score.to_dict(),
            'issues': issues,
            'shape': {'rows': len(df), 'columns': len(df.columns)}
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/simplify/<dataset_name>', methods=['POST'])
def simplify_dataset(dataset_name):
    """Simplify and clean a dataset"""
    try:
        if dataset_name not in datasets:
            return jsonify({'error': f'Dataset "{dataset_name}" not found'}), 404
        
        df = datasets[dataset_name]
        config = request.get_json() or {}
        
        simplifier = DataSimplifier(df)
        
        # Apply transformations based on config
        if config.get('remove_duplicates', True):
            simplifier.remove_duplicates()
        
        if config.get('handle_missing_values', True):
            strategy = config.get('missing_value_strategy', 'drop')
            simplifier.handle_missing_values(strategy=strategy)
        
        if config.get('standardize_names', True):
            simplifier.standardize_column_names()
        
        if config.get('clean_whitespace', True):
            simplifier.clean_whitespace()
        
        if config.get('remove_redundant', True):
            threshold = config.get('correlation_threshold', 0.95)
            simplifier.remove_redundant_columns(threshold=threshold)
        
        cleaned_df = simplifier.get_cleaned_data()
        datasets[f"{dataset_name}_cleaned"] = cleaned_df
        
        return jsonify({
            'message': 'Dataset simplified successfully',
            'original_shape': {'rows': len(df), 'columns': len(df.columns)},
            'cleaned_shape': {'rows': len(cleaned_df), 'columns': len(cleaned_df.columns)},
            'transformations': simplifier.get_transformations(),
            'cleaned_dataset_name': f"{dataset_name}_cleaned"
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/preview/<dataset_name>', methods=['GET'])
def preview_dataset(dataset_name):
    """Preview dataset (first N rows)"""
    try:
        if dataset_name not in datasets:
            return jsonify({'error': f'Dataset "{dataset_name}" not found'}), 404
        
        df = datasets[dataset_name]
        n = request.args.get('rows', 5, type=int)
        
        preview_data = df.head(n).to_dict(orient='records')
        
        return jsonify({
            'dataset': dataset_name,
            'total_rows': len(df),
            'preview_rows': n,
            'columns': df.columns.tolist(),
            'data': preview_data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<dataset_name>', methods=['GET'])
def download_dataset(dataset_name):
    """Download dataset as CSV"""
    try:
        if dataset_name not in datasets:
            return jsonify({'error': f'Dataset "{dataset_name}" not found'}), 404
        
        df = datasets[dataset_name]
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        
        return {
            'dataset': dataset_name,
            'csv': csv_buffer.getvalue()
        }, 200, {'Content-Disposition': f'attachment; filename="{dataset_name}.csv"'}
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics/<dataset_name>', methods=['GET'])
def get_statistics(dataset_name):
    """Get statistical summary of dataset"""
    try:
        if dataset_name not in datasets:
            return jsonify({'error': f'Dataset "{dataset_name}" not found'}), 404
        
        df = datasets[dataset_name]
        
        # Numeric statistics
        numeric_stats = df.describe().to_dict()
        
        # Column info
        column_info = {}
        for col in df.columns:
            column_info[col] = {
                'dtype': str(df[col].dtype),
                'null_count': int(df[col].isnull().sum()),
                'null_percentage': float(df[col].isnull().sum() / len(df) * 100),
                'unique_count': int(df[col].nunique()),
                'duplicates': int(len(df[col]) - df[col].nunique())
            }
        
        return jsonify({
            'dataset': dataset_name,
            'shape': {'rows': len(df), 'columns': len(df.columns)},
            'numeric_statistics': numeric_stats,
            'column_info': column_info
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/delete/<dataset_name>', methods=['DELETE'])
def delete_dataset(dataset_name):
    """Delete a dataset"""
    try:
        if dataset_name not in datasets:
            return jsonify({'error': f'Dataset "{dataset_name}" not found'}), 404
        
        del datasets[dataset_name]
        
        return jsonify({
            'message': f'Dataset "{dataset_name}" deleted successfully'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
