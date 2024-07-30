from config import *
from flask import Blueprint, request, jsonify
from utils import generate_summary
from user_utils import get_user_data

users_bp = Blueprint('users', __name__, url_prefix="/users")


@users_bp.route('/getSummaryData', methods=['POST'])
def get_summary():
    print("GET SUMMARY DATA")
    data = request.get_json()

    # userData= User.objects(email = email).first()
    # user = db['users']
    # user_data = user.find_one({"email": email})
    #
    # if not user_data:
    #     error_ = 'NO DATA'
    #     print(error_)
    #     return jsonify({'error': error_}), 409

    # for data in user_data['summary']:
    #     if data['url'] == url:
    #         print(data)
    #         return jsonify({'data': data})

    data = generate_summary(data)

    # user_data = user.find_one({"email": email})
    # print(user_data)
    return {"data": data}

    # for data in user_data['summary']:
    #     if data['url'] == url:
    #         return jsonify({'data': data})


@users_bp.route('/getAllTitle', methods=['POST'])
def get_all_title():
    # user_data = get_user_data()
    data = request.get_json()

    url_, email = data['url'], data['email']

    # result = []
    # for data in reversed(user_data['summary'][-5:]):
    #     result.append({'video_title': data['data']['video_title'], 'url': data['url']})
    #
    # print(result)

    result = ['video_title', url_]
    return result


@users_bp.route('/get_all_title', methods=['GET'])
def get_title():
    # user_data = get_user_data()
    #
    # result = [{'video_title': data['data']['video_title'], 'url': data['url']} for data in user_data["summary"]]
    #
    # print(result)
    return jsonify({'message': "This route does not work temporarily"})
