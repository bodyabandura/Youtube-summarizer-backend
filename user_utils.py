from flask import jsonify, request
from config import *


def get_user_data():
    email = request.json['email']
    print(email)

    user = db['user']
    user_data = user.find_one({"email": email})

    if not user_data:
        error_ = "NO DATA"
        print(error_)
        return jsonify({'error': error_}), 409
    return user_data
