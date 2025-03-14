import logging
from flask import Blueprint, request, jsonify
from sklearn.linear_model import Ridge, Lasso, ElasticNet, LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score
import pandas as pd
import numpy as np

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define Flask Blueprint
model_bp = Blueprint('model_bp', __name__)

# Model Selection
def get_model(model_type, is_classification):
    models = {
        'LinearRegression': LinearRegression(),
        'Ridge': Ridge(),
        'Lasso': Lasso(),
        'ElasticNet': ElasticNet(),
        'RandomForestRegressor': RandomForestRegressor(),
        'RandomForestClassifier': RandomForestClassifier(),
        'GradientBoostingRegressor': GradientBoostingRegressor(),
        'GradientBoostingClassifier': GradientBoostingClassifier(),
        'LogisticRegression': LogisticRegression(),
        'SVM': SVC()
    }
    return models.get(model_type, LinearRegression())

# Parameter Grid for Hyperparameter Tuning
def get_param_grid(model_type):
    param_grids = {
        'LinearRegression': {},
        'Ridge': {'alpha': [0.1, 1.0, 10.0]},
        'Lasso': {'alpha': [0.1, 1.0, 10.0]},
        'ElasticNet': {'alpha': [0.1, 1.0, 10.0], 'l1_ratio': [0.2, 0.5, 0.8]},
        'RandomForestRegressor': {'n_estimators': [100, 200], 'max_depth': [None, 10, 20]},
        'RandomForestClassifier': {'n_estimators': [100, 200], 'max_depth': [None, 10, 20]},
        'GradientBoostingRegressor': {'n_estimators': [100, 200], 'learning_rate': [0.01, 0.1, 0.2]},
        'GradientBoostingClassifier': {'n_estimators': [100, 200], 'learning_rate': [0.01, 0.1, 0.2]},
        'SVM': {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf']}
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

# Check Target Type for Classification or Regression
@model_bp.route('/check_target_type', methods=['POST'])
def check_target_type():
    if 'dataset' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['dataset']
    target = request.form.get('target', '')

    try:
        df = pd.read_csv(file)
        if target not in df.columns:
            return jsonify({'error': f"Target column '{target}' not found"}), 400

        is_regression = df[target].dtype in ['int64', 'float64'] and df[target].nunique() > 10
        return jsonify({'isRegression': is_regression}), 200
    except Exception as e:
        logger.error(f"Error checking target type: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Data Preprocessing Function
def preprocess_data(file, features, target, poly_degree):
    try:
        df = pd.read_csv(file)

        missing_columns = [col for col in features + [target] if col not in df.columns]
        if missing_columns:
            return None, None, None, None, None, None, None, {'error': f"Missing columns: {missing_columns}"}

        df[features] = df[features].fillna(df[features].mean())

        is_classification = df[target].dtype == 'object' or df[target].nunique() < 10

        encoder = None
        if is_classification:
            encoder = LabelEncoder()
            df[target] = encoder.fit_transform(df[target])
            logger.info(f"🔢 Encoded target column '{target}' into numerical values.")

        X = df[features]
        y = df[target]

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        if poly_degree > 1:
            poly = PolynomialFeatures(degree=poly_degree, include_bias=False)
            X_scaled = poly.fit_transform(X_scaled)

        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        return X_train, X_test, y_train, y_test, df, encoder, is_classification, None
    except Exception as e:
        logger.error(f"Error preprocessing data: {str(e)}")
        return None, None, None, None, None, None, None, {'error': str(e)}

# Calculate Model Performance Metrics
def calculate_metrics(y_test, y_pred, num_features, is_classification):
    try:
        if is_classification:
            y_pred = np.round(y_pred).astype(int)
            y_pred = np.clip(y_pred, 0, np.max(y_test))
            accuracy = accuracy_score(y_test, y_pred)
            return {'accuracy': accuracy}
        else:
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)
            adjusted_r2 = 1 - (1 - r2) * (len(y_test) - 1) / max(1, (num_features + 1))
            return {'mae': mae, 'mse': mse, 'rmse': rmse, 'r2': r2, 'adjusted_r2': adjusted_r2}
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
    model_type = data.get('model_type', 'GradientBoostingRegressor')
    poly_degree = int(data.get('poly_degree', 1))

    X_train, X_test, y_train, y_test, df, encoder, is_classification, error = preprocess_data(file, features, target, poly_degree)
    if error:
        return jsonify(error), 400

    model = get_model(model_type, is_classification)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    metrics = calculate_metrics(y_test, y_pred, X_train.shape[1], is_classification)

    return jsonify({'metrics': metrics}), 200
