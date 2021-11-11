from flask import Blueprint, request, jsonify
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from src.DataSource import DataSource
from src.constants.http_status_code import HTTP_200_OK, HTTP_404_NOT_FOUND
from flasgger import Swagger, swag_from
search = Blueprint("search", __name__, url_prefix="/api/v1/search")


@search.route('/lyric_search', methods=['GET'])
@jwt_required()
@swag_from('./docs/search/lyric.yaml')
def get_song_by_lyric():
    identity = get_jwt_identity()
    DB = DataSource()
    DB.open()
    if request.method == 'GET':
        kw = request.args.get('kw')
        kw = kw.split(',')
        searching_type = request.args.get('type')
        result = DB.query_song_by_lyrics(kw, searching_type)
        if len(result) > 0:
            return jsonify(result), HTTP_200_OK
        else:
            return jsonify({
                'Message': 'No Result Found'
            }), HTTP_404_NOT_FOUND


@search.route('/artist_search', methods=['GET'])
@jwt_required()
@swag_from('./docs/search/artist.yaml')
def artist_search():
    DB = DataSource()
    DB.open()
    if request.method == 'GET':
        kw = request.args.get('artist')
        kw = kw.split(',')
        searching_type = request.args.get('type')
        result = DB.query_artist_by_name(kw, searching_type)
        if len(result) > 0:
            return jsonify(result), HTTP_200_OK
        else:
            return jsonify({
                'Message': 'No Result Found'
            }), HTTP_404_NOT_FOUND


@search.route('/title_search', methods=['GET'])
@jwt_required()
@swag_from('./docs/search/title.yaml')
def title_search():
    DB = DataSource()
    DB.open()
    if request.method == 'GET':
        kw = request.args.get('title')
        kw = kw.split(',')
        searching_type = request.args.get('type')
        result = DB.query_song_by_title(kw, searching_type)
        if len(result) > 0:
            return jsonify(result), HTTP_200_OK
        else:
            return jsonify({
                'Message': 'No Result Found'
            }), HTTP_404_NOT_FOUND
