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


def update_prediction(start_time, prediction):
    current_time = int(time.time())
    new_prediction = prediction - (current_time - start_time)
    return new_prediction


def predict_session_length():

    current_time = datetime.now()
    current_hour = str(current_time.hour)

    with open('/Users/oskarkala/Documents/session-prediction-api/hour_to_sessdur_map.json', 'r') as map:
        hour_sessdur_map = json.load(map)

    prediciton = hour_sessdur_map[current_hour]

    return prediciton


def cookie_maker(ID, page_counter, t, p):
    cookie = str(ID) + ':' + str(page_counter) + ':' + str(t) + ':' + str(p)
    return cookie


@app.route('/on_load_event')
def on_load_event():

    cookie = request.cookies.get('username')

    with open('/Users/oskarkala/Documents/session-prediction-api/user_data.json', 'r') as ud:
        user_data = json.load(ud)

    if cookie:
        splitted_cookie = cookie.split(sep=':')
        #print(cookie)
        ID = str(splitted_cookie[0])
        page_counter = str(splitted_cookie[1])
        t = int(time.time())
        p = int(splitted_cookie[3])

        #print(type(ID), type(page_counter))

        for key, value in user_data[ID][page_counter][-1].items():
            print(key, value)

        #print(value, int(time.time()))

        prediction = update_prediction(int(splitted_cookie[2]), p)
        page_counter = str(int(splitted_cookie[1]) + 1)
        print(page_counter)
        user_data[ID][page_counter] = []

        cookie = cookie_maker(ID=ID, page_counter=page_counter, t=t, p=prediction)


    if not cookie:
        #print("no cookie")
        ID = str(int(max(user_data.keys())) + 1)
        t = int(time.time())
        prediction = predict_session_length()
        page_counter = str(0)

        cookie = cookie_maker(ID=ID, page_counter=page_counter, t=t, p=prediction)

        user_data[ID] = {page_counter: []}

    event = {
        'start': int(time.time())
    }


    user_data[ID][page_counter].append(event)

    with open('user_data.json', 'w') as ud:
        json.dump(user_data, ud)

    resp = jsonify({'user_leaving_in': prediction})
    resp.headers['Cache-Control'] = 'no-cache'
    resp.set_cookie('username', cookie, max_age=2700000)

    return resp


@app.route('/on_unload_event')
def on_unload_event():
    cookie = request.cookies.get('username')
    splitted_cookie = cookie.split(sep=':')

    ID = str(splitted_cookie[0])
    page_counter = str(splitted_cookie[1])
    print(ID, page_counter, "unload")

    if cookie:
        with open('user_data.json', 'r') as ud:
            user_data = json.load(ud)

        event = {
            'stop': int(time.time())
        }
        user_data[ID][page_counter].append(event)

        with open('user_data.json', 'w') as ud:
            json.dump(user_data, ud)

    resp = jsonify({})
    resp.headers['Cache-Control'] = 'no-cache'

    return resp


if __name__ == '__main__':
    app.run(debug=True)

