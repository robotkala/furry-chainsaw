import random
import time
import json
from datetime import timedelta, datetime
from pprint import pprint
from flask import Flask, jsonify, abort, request, render_template, Response, session, make_response, redirect, url_for
from flask_cors import CORS
import pygeoip

app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/html')
def initialize_user_session():

    resp = make_response(render_template('main_html_page.html'))

    return resp, 200


@app.route('/sec_html')
def second_html():

    resp = make_response(render_template('main_html_page2.html'))

    return resp, 200


def predict_session_length():

    current_time = datetime.now()
    current_hour = str(current_time.hour)

    with open('/Users/martinl/Documents/Docker/session-prediction-python-api/hour_to_sessdur_map.json', 'r') as map:
        hour_sessdur_map = json.load(map)

    prediciton = hour_sessdur_map[current_hour]

    return prediciton


@app.route('/on_load_event')
def on_load_event():

    cookie = request.cookies.get('username')

    with open('user_data.json', 'r') as ud:
        user_data = json.load(ud)

    if cookie:
        for key, value in user_data[cookie][-1].items():
            print(key,value)

        print(value, int(time.time()))

        time_difference = int(time.time()) - value

        print(time_difference)

        if time_difference >= 1800:
            prediction = predict_session_length()
        else:
            prediction = 1234

        resp = jsonify({'user_leaving_in': prediction})

    if not cookie:
        cookie = str(int(max(user_data.keys())) + 1)
        user_data[cookie] = []
        prediction = predict_session_length()

        resp = jsonify({'user_leaving_in': prediction})

        resp.set_cookie('username', cookie, max_age=2700000)
        print(cookie)

    event = {
        'start': int(time.time())
    }

    user_data[cookie].append(event)

    with open('user_data.json', 'w') as ud:
        json.dump(user_data, ud)

    resp.headers['Cache-Control'] = 'no-cache'

    return resp


@app.route('/on_unload_event')
def on_unload_event():
    cookie = request.cookies.get('username')

    if cookie:
        with open('user_data.json', 'r') as ud:
            user_data = json.load(ud)

        event = {
            'stop': int(time.time())
        }

        user_data[cookie].append(event)

        with open('user_data.json', 'w') as ud:
            json.dump(user_data, ud)

    resp = jsonify({})
    resp.headers['Cache-Control'] = 'no-cache'

    return resp


if __name__ == '__main__':
    app.run(debug=True)

