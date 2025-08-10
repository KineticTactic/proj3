from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return jsonify(message="Welcome to the Flask application!")

@bp.route('/api/data')
def get_data():
    data = {
        "key1": "value1",
        "key2": "value2"
    }
    return jsonify(data)