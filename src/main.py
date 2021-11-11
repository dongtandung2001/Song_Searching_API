from DataSource import DataSource
import sqlite3
from flask import Flask, render_template, request, jsonify


def continue_searching(results):
    a = input('Do you want to continue your searching? (Y/n): ')
    if a.lower() == 'y':
        a = int(input('Enter the result number from the above lists: '))
        print(results[a][1] + " By " + results[a][5])
        print("Lyrics:")
        print(results[a][3])
    else:
        pass


def split_input():
    x = input('Enter the list of keywords, can be separated by comma: ')
    x = x.split(', ')
    return x


app = Flask(__name__)


@app.route('/Test', methods=['POST', 'GET'])
def search_by_lyric():
    DB = DataSource()
    DB.open()
    if request.method == 'GET':
        kw = request.args.get('kw')
        kw = kw.split(',')
        searching_type = request.args.get('type')
        result = DB.query_by_lyrics(kw, searching_type)
    return result


@app.route('/')
@app.route('/HomePage')
def home_page():
    return render_template("base.html")


@app.route('/market', methods=['GET'])
def market_page():
    DB = DataSource()
    DB.open()
    if request.method == 'GET':
        kw = request.args.get('kw')
        kw = kw.split(',')
        searching_type = request.args.get('type')
        items = (DB.query_song_by_lyrics(kw, searching_type))

    """items = [
        {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
        {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
        {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    ]"""
    return render_template("market.html", items=items)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
