import logging
from io import StringIO
from flask import Blueprint, request, jsonify
from sklearn.linear_model import Ridge, Lasso, ElasticNet, LinearRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pandas as pd
import numpy as np

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define Flask Blueprint
model_bp = Blueprint('model_bp', __name__)

# Model Selection
def get_model(model_type):
    models = {
        'LinearRegression': LinearRegression(),
        'Ridge': Ridge(),
        'Lasso': Lasso(),
        'ElasticNet': ElasticNet(),
        'RandomForest': RandomForestRegressor(),
        'GradientBoosting': GradientBoostingRegressor()
    }
    return models.get(model_type, LinearRegression())

# Parameter Grid for Hyperparameter Tuning
def get_param_grid(model_type):
    param_grids = {
        'LinearRegression': {},
        'Ridge': {'alpha': [0.1, 1.0, 10.0]},
        'Lasso': {'alpha': [0.1, 1.0, 10.0]},
        'ElasticNet': {'alpha': [0.1, 1.0, 10.0], 'l1_ratio': [0.2, 0.5, 0.8]},
        'RandomForest': {'n_estimators': [100, 200], 'max_depth': [None, 10, 20]},
        'GradientBoosting': {'n_estimators': [100, 200], 'learning_rate': [0.01, 0.1, 0.2]}
    }
    return param_grids.get(model_type, {})

# Show Features in Uploaded CSV
@model_bp.route('/show_features', methods=['POST'])
def show_features():
    if 'dataset' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['dataset']
    try:
        df = pd.read_csv(file)
        return jsonify({'features': df.columns.tolist()}), 200
    except Exception as e:
        logger.error(f"Error reading dataset: {str(e)}")
        return jsonify({'error': f"Failed to process file: {str(e)}"}), 500

# Data Preprocessing Function
def preprocess_data(file, features, target, poly_degree):
    try:
        df = pd.read_csv(file)

        # Validate feature columns
        missing_columns = [col for col in features + [target] if col not in df.columns]
        if missing_columns:
            return None, None, None, None, None, {'error': f"Missing columns: {missing_columns}"}

        # Handle missing values
        df[features] = df[features].fillna(df[features].mean())

        X = df[features]
        y = df[target]

        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Apply Polynomial Features if needed
        if poly_degree > 1:
            poly = PolynomialFeatures(degree=poly_degree, include_bias=False)
            X_scaled = poly.fit_transform(X_scaled)

        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        return X_train, X_test, y_train, y_test, df, None
    except Exception as e:
        logger.error(f"Error preprocessing data: {str(e)}")
        return None, None, None, None, None, {'error': str(e)}

# Calculate Model Performance Metrics
def calculate_metrics(y_test, y_pred, num_features):
    try:
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        # Fix adjusted R² formula
        adjusted_r2 = 1 - (1 - r2) * (len(y_test) - 1) / (num_features - 1)

        return {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'r2': r2,
            'adjusted_r2': adjusted_r2
        }
    except Exception as e:
        logger.error(f"Error calculating metrics: {str(e)}")
        return {'error': str(e)}

# Train Model API
@model_bp.route('/train', methods=['POST'])
def train_model():
    if 'dataset' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['dataset']
    data = request.form.to_dict()

    features = [f.strip() for f in data.get('features', '').split(',')]
    target = data.get('target', '')
    model_type = data.get('model_type', 'LinearRegression')
    poly_degree = int(data.get('poly_degree', 1))

    logger.info(f"Starting training: {model_type} | Features: {features} | Target: {target}")

    model = get_model(model_type)
    if model is None:
        return jsonify({'error': f"Model type {model_type} is not supported"}), 400

    try:
        X_train, X_test, y_train, y_test, df, error = preprocess_data(file, features, target, poly_degree)
        if error:
            return jsonify(error), 400

        # Grid Search Hyperparameter Tuning
        grid_search = GridSearchCV(model, get_param_grid(model_type), cv=5, scoring='r2', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        best_model = grid_search.best_estimator_

        # Predict and Compute Metrics
        y_pred = best_model.predict(X_test)
        num_features = X_train.shape[1]
        metrics = calculate_metrics(y_test, y_pred, num_features)

        # Predict entire dataset
        df['predicted'] = best_model.predict(StandardScaler().fit_transform(df[features]))

        return jsonify({
            'score': metrics['r2'],
            'mae': metrics['mae'],
            'mse': metrics['mse'],
            'rmse': metrics['rmse'],
            'adjusted_r2': metrics['adjusted_r2'],
            'coefficients': best_model.coef_.tolist() if hasattr(best_model, 'coef_') else None,
            'intercept': best_model.intercept_ if hasattr(best_model, 'intercept_') else None,
            'best_params': grid_search.best_params_,
            'data': df[features + [target, 'predicted']].to_dict(orient='records')
        }), 200

    except Exception as e:
        logger.error(f"Error during training: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred during training.'}), 500
