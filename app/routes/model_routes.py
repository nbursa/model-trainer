from flask import Blueprint, request, jsonify
from sklearn.linear_model import LinearRegression
import pandas as pd

model_bp = Blueprint('model_bp', __name__)


# @model_bp.route('/train', methods=['POST'])
# def train_model():
#     data = request.json
#     df = pd.DataFrame(data['dataset'])
#     X = df[data['features']]
#     y = df[data['target']]
#
#     model = LinearRegression()
#     model.fit(X, y)
#
#     score = model.score(X, y)
#     return jsonify({'score': score})
@model_bp.route('/train', methods=['POST'])
def train_model():
    if 'dataset' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['dataset']
    data = request.form.to_dict()
    features = data['features'].split(',')
    target = data['target']

    df = pd.read_csv(file)
    X = df[features]
    y = df[target]

    model = LinearRegression()
    model.fit(X, y)

    score = model.score(X, y)
    return jsonify({'score': score})
