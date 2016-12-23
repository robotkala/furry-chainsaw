import random
import time
import json
from datetime import timedelta
from pprint import pprint
from flask import Flask, jsonify, abort, request, render_template, Response, session, make_response, redirect, url_for
from flask_cors import CORS
import pygeoip

app = Flask(__name__)
CORS(app, resources=r'/*')

users_on_page = dict()

gi = pygeoip.GeoIP('/Users/martinl/Documents/Docker/session-prediction-python-api/static/GeoLiteCity.dat', pygeoip.MEMORY_CACHE)

@app.route('/html')
def initialize_user_session():

    resp = make_response(render_template('main_html_page.html'))

    return resp, 200


@app.route('/sec_html')
def second_html():

    resp = make_response(render_template('main_html_page2.html'))

    return resp, 200


def make_cookie(id, t, p, page_counter):
    cookie = str(id) + ':' + str(t) + ':' + str(p) + ':' + str(page_counter)
    return cookie


def get_user_data():
    user_data = {}

    # get ip

    try:
        # Currently request.remote_addr is overridden for work in localhost
        # user_data['ip'] = request.remote_addr
        user_data['ip'] = '91.146.64.107'
    except KeyError:
        pass

    if 'ip' in user_data.keys():
        # one time, get location
        geo_data = gi.record_by_addr(user_data['ip'])
        user_data['country'] = geo_data['country_name']
        user_data['city'] = geo_data['city']

    try:
        user_data['charset'] = request.charset
    except KeyError:
        pass

    try:
        user_data['browser'] = request.user_agent.browser
    except KeyError:
        pass

    try:
        user_data['version'] = request.user_agent.version and int(request.user_agent.version.split('.')[0])
    except KeyError:
        pass

    try:
        user_data['platform'] = request.user_agent.platform
    except KeyError:
        pass

    return user_data


def predict_session_length(data):
    print(data)
    return 100


@app.route('/make_prediction')
def cookie_monster():

    cookie = str()

    temp_cookie = request.cookies.get('username')

    print('temp_cookie', temp_cookie)

    if not temp_cookie:
        # get first time visitor data
        user_data = get_user_data()

        # make this !!!
        prediction_time = predict_session_length(user_data)

        ID = random.randint(0, 100000)
        T = int(time.time())
        P = prediction_time
        page_counter = 0
        cookie = make_cookie(id=ID, t=T, p=P, page_counter=page_counter)

    if temp_cookie:
        # if returning visitor
        splitted_cookie = temp_cookie.split(sep=':')
        # print((int(splitted_cookie[1]), int(splitted_cookie[2])), current_unix)
        P = (int(splitted_cookie[1]) + int(splitted_cookie[2])) - int(time.time())
        page_counter = int(splitted_cookie[3]) + 1
        cookie = make_cookie(id=splitted_cookie[0], t=int(time.time()), p=P, page_counter=page_counter)

    print(cookie)

    resp = jsonify({'user_leaving_in': P})
    resp.headers['Cache-Control'] = 'no-cache'
    resp.set_cookie('username', cookie, max_age=P)

    return resp


if __name__ == '__main__':
    app.run(debug=True)


'''
    user_state = {}



    try:
        user_state['cookie'] = request.cookies.get('pmuser')
    except KeyError:
        pass

    try:
        user_state['ip'] = request.remote_addr
    except KeyError:
        pass

    try:
        user_state['referrer'] = request.referrer
    except KeyError:
        pass

    # eelmine lehekulg ehk localhost:5000/index.html

    try:
        user_state['charset'] = request.charset
    except KeyError:
        pass

    try:
        user_state['browser'] = request.user_agent.browser
    except KeyError:
        pass

    try:
        user_state['version'] = request.user_agent.version and int(request.user_agent.version.split('.')[0])
    except KeyError:
        pass

    try:
        user_state['platform'] = request.user_agent.platform
    except KeyError:
        pass

    try:
        user_state['uas'] = request.user_agent.string
    except KeyError:
        pass

    user_state[user_state['cookie']] = {'came': time.time()}

    #pprint(user_state)

    users_on_page[user_state['cookie']] = user_state

    print(user_state['cookie'])
'''
'''
    if temp_cookie:
        print('temp_cookie', type(temp_cookie), temp_cookie)
        print(type(json.loads(temp_cookie)), json.loads(temp_cookie))
        cookie = temp_cookie
        cookie['P'] = int(cookie['P']) - (current_unix - int(cookie['T']))


    if not temp_cookie:
        prediction_time = 30

        cookie = {
            'ID': str(random.randint(0, 100000)),
            'T': str(current_unix),
            'P': prediction_time
        }
'''