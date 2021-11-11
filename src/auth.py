from flasgger import swag_from
from flask import Blueprint, request
from flask import json
from flask.json import jsonify
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.http_status_code import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_201_CREATED
import validators
from src.DataSource import User
from flask_jwt_extended import create_access_token, create_refresh_token
auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.route('/register', methods=['POST'])
@swag_from('./docs/auth/register.yaml')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    db = User()
    db.open()

    if len(password) < 6:
        return jsonify({'Error': 'Password is too short'}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({'Error': 'Username is too short'}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'Error': 'User name should be alphalnumeric and no spaces'}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'Error': 'Email is not valid'}), HTTP_400_BAD_REQUEST

    if db.query_email(email) is not None:
        return jsonify({'Error': 'email is already existed. Please try another one'}), HTTP_409_CONFLICT

    if db.query_username(username) is not None:
        return jsonify({'Error': 'Username is already existed. Please try another one'}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)
    db.create_user(username=username, email=email, password=pwd_hash)
    db.close()

    return jsonify({'message:': 'user created',
                    'user:': {
                        'username': username,
                        'email': email,
                    }
                    }), HTTP_201_CREATED


@auth.route('/login', methods=['POST'])
@swag_from('./docs/auth/login.yaml')
def login():
    user = User()
    user.open()

    # get post request
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    # query from the user database
    _user = user.query_email(email)
    if _user is not None:
        check_password = check_password_hash(
            user.query_password(email), password)
        if check_password:
            id = user.query_id(email)
            username = user.query_username_by_id(id)
            refresh = create_refresh_token(identity=id)
            access = create_access_token(identity=id)

            user.close()
            return jsonify({
                'user': {
                    'refresh token:': refresh,
                    'access token': access,
                    'username': username,
                    'email': email,
                }
            }), HTTP_200_OK
    user.close()
    return jsonify({
        'Error': 'Unauthorized Login'
    }), HTTP_401_UNAUTHORIZED


@auth.route('/home', methods=['GET'])
@jwt_required()
def me():
    db = User()
    db.open()
    user_id = get_jwt_identity()
    user = db.query_user_by_id(user_id)
    return jsonify({
        'username': user['username'],
        'email': user['email']
    })


@auth.route('/token/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)
    return jsonify({
        'access': access
    }), HTTP_200_OK
