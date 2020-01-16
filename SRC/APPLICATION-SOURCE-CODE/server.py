import json
from flask import Flask, render_template, request, jsonify

import queries

app = Flask(__name__)


class DateRange(object):
    def __init__(self):
        self.start = ''
        self.end = ''


date_range = DateRange()
genres_list = []
locations_list = []
artists_list = []
free_text = ''


def _get_mysql_date_format(date):
    stripped_date = date.strip()
    day, month, year = stripped_date.split('/')
    return f'20{year}-{month}-{day}'


def _get_date_range_mysql(date_range_input):
    start, end = date_range_input.split('-')
    return _get_mysql_date_format(start), _get_mysql_date_format(end)


@app.route('/date_range_process')
def date_range_process():
    try:
        global date_range
        date_range_result = request.args.get('date_range')
        date_range.start, date_range.end = _get_date_range_mysql(date_range_result)
        are_there_shows = queries.are_there_concerts_on_these_dates(date_range.start, date_range.end)
        if not are_there_shows:
            return jsonify(result='Sorry, no concerts on these dates')
        else:
            return jsonify(result='Great time to travel!')
    except Exception as e:
        return str(e)


@app.route('/genres_process')
def genres_process():
    global genres_list
    chosen_genres = request.args.get('chosen_genres')
    genres_list = chosen_genres.split(',')
    # print(f'genres_list:{genres_list}')
    if genres_list == ['']:
        return jsonify(result='')
    return jsonify(result='Great Choices')


@app.route('/locations_process')
def locations_process():
    global locations_list
    chosen_locations = request.args.get('chosen_locations')
    locations_list = chosen_locations.split(',')
    # print(f'locations_list:{locations_list}')
    if locations_list == ['']:
        return jsonify(result='')
    return jsonify(result='Great Choices')


@app.route('/artists_process')
def artists_process():
    global artists_list
    chosen_artists = request.args.get('chosen_artists')
    artists_list = chosen_artists.split(',')
    # print(f'genres_list:{genres_list}')
    if artists_list == ['']:
        return jsonify(result='')
    return jsonify(result='Great Choices')


@app.route('/get_artists')
def get_artists():
    # print("in get_artists")
    shown_artists_list = queries.query_get_artists(date_range.start, date_range.end, locations_list)
    return jsonify(result=shown_artists_list)


@app.route('/get_genres')
def get_genres():
    # print("in get_genres")
    shown_genres_list = queries.query_get_genres(date_range.start, date_range.end)
    return jsonify(result=shown_genres_list)


@app.route('/get_locations')
def get_locations():
    # print('in get_locations')
    shown_locations_list = queries.query_get_locations(date_range.start, date_range.end, genres_list)
    result = {'results': shown_locations_list}
    return result


@app.route('/concerts', methods=['POST'])
def process_form():
    print('here')
    return render_template('concerts.html')


@app.route('/get_recommendations')
def get_recommendations():
    recommendations = queries.query_get_recommendations()
    return jsonify(result=recommendations)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port="8081", debug=True)
