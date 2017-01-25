import json
import time
import pytz
from flask import Flask, make_response, render_template, jsonify, request
from datetime import datetime
from redis import Redis

expiration_time = 10 # seconds
app = Flask(__name__)
redis = Redis(host='redis', port=6379)


@app.route('/one')
def html_page_one():
    resp = make_response(render_template('one.html'))
    return resp, 200


@app.route('/two')
def html_page_two():
    resp = make_response(render_template('two.html'))
    return resp, 200


def make_prediction():
    sessdur_map = {
        "0": 347,
        "1": 292,
        "2": 311,
        "3": 321,
        "4": 392,
        "5": 480,
        "6": 480,
        "7": 426,
        "8": 462,
        "9": 454,
        "10": 453,
        "11": 429,
        "12": 431,
        "13": 441,
        "14": 449,
        "15": 433,
        "16": 398,
        "17": 409,
        "18": 409,
        "19": 407,
        "20": 391,
        "21": 377,
        "22": 348,
        "23": 243
    }
    current_time = datetime.now(pytz.timezone('Europe/Tallinn'))
    return sessdur_map[str(current_time.hour)]


def update_prediction(start_time, prediction):
    current_time = int(time.time())
    new_prediction = prediction - (current_time - start_time)
    return new_prediction


@app.route('/on_load_event')
def on_load_event():
    cookie = request.cookies.get('_ga')

    # if doesn't exist
    if redis.exists(cookie + ':visited') == 0:
        visited = 0
        exp_time = expiration_time
        print('visited, ', visited)

    # if exists
    else:
        visited = 1
        exp_time = redis.ttl(cookie + ':visited')
        print('visited, ', visited)

    # if doesn't exist
    if redis.exists(cookie) == 0:

        prediction = make_prediction()

        counter = str(1)

        user_data = {
            counter: []
        }

        event = {
            'start': int(time.time())
        }
        user_data[counter].append(event)

        redis.set(cookie, json.dumps(user_data))
        redis.set(cookie + ':prediction', prediction)

    # if exists
    else:
        user_data = json.loads(redis.get(cookie).decode('utf-8'))

        counter = max(user_data.keys(), key=int)

        prev_prediction = redis.get(cookie + ':prediction')

        prev_prediction_start = user_data[str(counter)][0]['start']
        prediction = update_prediction(prev_prediction_start, int(prev_prediction))
        if prediction <= 0:
            prediction = make_prediction()

        counter = str(int(counter) + 1)

        user_data[counter] = []

        event = {
            'start': int(time.time())
        }

        user_data[counter].append(event)

        redis.set(cookie, json.dumps(user_data))
        redis.set(cookie + ':prediction', prediction)

    resp = jsonify({'user_leaving_in': prediction, 'counter': counter, 'visited': visited, 'exp_time': exp_time})
    resp.headers['Cache-Control'] = 'no-cache'
    return resp, 200


@app.route('/on_unload_event/<counter>')
def on_unload_event(counter):
    cookie = request.cookies.get('_ga')
    try:
        user_data = json.loads(redis.get(cookie).decode('utf-8'))
        event = {
            'stop': int(time.time())
        }
        user_data[counter].append(event)
        redis.set(cookie, json.dumps(user_data))
        print('on unload event')
    except AttributeError:
        pass
    resp = jsonify({})
    resp.headers['Cache-Control'] = 'no-cache'
    return resp, 200


@app.route('/exit_intent_event/<counter>')
def exit_intent_event(counter):
    cookie = request.cookies.get('_ga')
    try:
        user_data = json.loads(redis.get(cookie).decode('utf-8'))

        event = {
            'exit_intent': int(time.time())
        }
        user_data[counter].append(event)

        redis.set(cookie, json.dumps(user_data))
        redis.setex(cookie + ':visited', 1, expiration_time)

        print('exit intent event')
    except AttributeError:
        pass
    resp = jsonify({})
    resp.headers['Cache-Control'] = 'no-cache'
    return resp, 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

