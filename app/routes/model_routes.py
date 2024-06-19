from io import StringIO
from flask import Blueprint, request, jsonify
from sklearn.linear_model import Ridge, Lasso, ElasticNet, LinearRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
import pandas as pd
import numpy as np

model_bp = Blueprint('model_bp', __name__)


@model_bp.route('/train', methods=['POST'])
def train_model():
    if 'dataset' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['dataset']
    data = request.form.to_dict()
    features = data['features'].split(',')
    target = data['target']
    model_type = data.get('model_type', 'LinearRegression')
    poly_degree = int(data.get('poly_degree', 1))

    # Read the file contents into a pandas DataFrame
    file_content = file.read().decode('utf-8')
    df = pd.read_csv(StringIO(file_content))

    # Check if specified features and target exist in the dataset
    missing_columns = [col for col in features + [target] if col not in df.columns]
    if missing_columns:
        return jsonify({'error': f"Columns {missing_columns} not found in the dataset"}), 400

    X = df[features]
    y = df[target]

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Polynomial Features
    if poly_degree > 1:
        poly = PolynomialFeatures(degree=poly_degree, include_bias=False)
        X_scaled = poly.fit_transform(X_scaled)

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Model Selection
    models = {
        'LinearRegression': LinearRegression(),
        'Ridge': Ridge(),
        'Lasso': Lasso(),
        'ElasticNet': ElasticNet(),
        'RandomForest': RandomForestRegressor(),
        'GradientBoosting': GradientBoostingRegressor()
    }

    if model_type not in models:
        return jsonify({'error': f"Model type {model_type} is not supported"}), 400

    model = models[model_type]

    # Example hyperparameters - could be extended based on model type
    param_grids = {
        'LinearRegression': {},
        'Ridge': {'alpha': [0.1, 1.0, 10.0]},
        'Lasso': {'alpha': [0.1, 1.0, 10.0]},
        'ElasticNet': {'alpha': [0.1, 1.0, 10.0], 'l1_ratio': [0.2, 0.5, 0.8]},
        'RandomForest': {'n_estimators': [100, 200], 'max_depth': [None, 10, 20]},
        'GradientBoosting': {'n_estimators': [100, 200], 'learning_rate': [0.01, 0.1, 0.2]}
    }

    grid_search = GridSearchCV(model, param_grids.get(model_type, {}), cv=5, scoring='r2', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_

    score = best_model.score(X_test, y_test)
    df['predicted'] = best_model.predict(X_scaled)
    response_data = df.to_dict(orient='records')

    return jsonify({'score': score, 'data': response_data, 'best_params': grid_search.best_params_})
