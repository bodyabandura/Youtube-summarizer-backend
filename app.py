from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mail import Mail, Message
from utils import *
from auth.routes import auth_bp
from users.routes import users_bp
import ssl

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)

app.secret_key = SECRET_KEY
CORS(app)

app.config.update(UPDATE_CONFIG_DICT)
mail = Mail(app)

ssl._create_default_https_context = ssl._create_stdlib_context


@app.route('/sendMail', methods=['POST'])
def send_email():
    data = request.get_json()
    name, email, message = data['name'], data['email'], data['message']

    msg = Message(f'Contact message from {name}',
                  sender='radu.vrabie@gmail.com',
                  recipients=['radu.vrabie@gmail.com'],
                  body=f"{message}\n User Email:{email}")
    mail.send(msg)
    print("MAIL SENT")
    return {"message": "success"}, 200


@app.route('/getSummary', methods=['POST'])
def get_summary():
    data = request.get_json()
    data = generate_summary(data)
    return jsonify(data), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
