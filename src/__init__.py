from flask import Flask, jsonify
import os
from src.auth import auth
from src.constants.http_status_code import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.search import search
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            JWT_SECRETKEY=os.environ.get("JWT_SECRET_KEY"),

            SWAGGER={
                'title': 'Song Searching API',
                'uiversion': 3
            }
        )
    else:
        app.config.from_mapping(test_config)

    JWTManager(app)
    app.register_blueprint(auth)
    app.register_blueprint(search)

    Swagger(app, config=swagger_config, template=template)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def error_404(e):
        return jsonify({'Error:' 'Not Found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def error_500(e):
        return jsonify({'Error:' 'Something\'s gone wrong, We will fix it as soon as possible'}), HTTP_500_INTERNAL_SERVER_ERROR

    return app
