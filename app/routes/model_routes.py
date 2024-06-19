from io import StringIO
from flask import Blueprint, request, jsonify
from sklearn.linear_model import LinearRegression
import pandas as pd

model_bp = Blueprint('model_bp', __name__)


@model_bp.route('/train', methods=['POST'])
def train_model():
    if 'dataset' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['dataset']
    data = request.form.to_dict()
    features = data['features'].split(',')
    target = data['target']

    # Read the file contents into a pandas DataFrame
    file_content = file.read().decode('utf-8')
    df = pd.read_csv(StringIO(file_content))

    # Check if specified features and target exist in the dataset
    missing_columns = [col for col in features + [target] if col not in df.columns]
    if missing_columns:
        return jsonify({'error': f"Columns {missing_columns} not found in the dataset"}), 400

    X = df[features]
    y = df[target]

    model = LinearRegression()
    model.fit(X, y)

    df['predicted'] = model.predict(X)
    score = model.score(X, y)
    response_data = df.to_dict(orient='records')

    return jsonify({'score': score, 'data': response_data})
