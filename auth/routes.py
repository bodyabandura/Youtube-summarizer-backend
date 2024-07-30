from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import *
from generate_token import generate_token

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")


@auth_bp.route('/signup', methods=['POST'])
def create_user():
    print("SIGNUP REQUEST")
    email = request.json['email']
    password = generate_password_hash(request.json['password'])

    user = db['user']
    existing_email = user.find_one({"email": email})

    if existing_email:
        print('EMAIL ALREADY EXISTS')
        return jsonify({
            "error": "EMAIL ALREADY EXISTS"
        }), 409

    user.insert_one({"email": email, "password": password, "summary": []})

    return jsonify({
        "msg": "OK"
    })


@auth_bp.route('/signin', methods=['POST'])
def signin():
    print("LOG IN")
    data = request.get_json()
    email = data['email']
    password = data['password']

    # user = User.objects(email=email).first()
    user = db['user']
    exist_user = user.find_one({"email": email})
    if exist_user and check_password_hash(exist_user['password'], password):
        token = generate_token(exist_user)
        print("REGISTERED USER")
        return jsonify({
            'token': token,
            "email": str(exist_user['email'])
        }), 200

    error_ = "INVALID USER"
    print(error_)
    return jsonify({'error': error_}), 401
