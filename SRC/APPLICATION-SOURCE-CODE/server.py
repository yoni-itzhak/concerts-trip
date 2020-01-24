import os
import ast
from flask import Flask, render_template, request, jsonify
from flask_table import Table, Col, html
import DBConnection
import queries

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


class DateRange(object):
    def __init__(self):
        self.start = ''
        self.end = ''


date_range = DateRange()
genres_list = []
locations_list = []
artists_list = []
free_text = ''
matching_concerts = []


class CheckboxCol(Col):
    def __init__(self, name, attr=None, attr_list=None, text_fallback=None, **kwargs):
        super(CheckboxCol, self).__init__(
            name,
            attr=attr,
            attr_list=attr_list,
            **kwargs)

        self.text_fallback = text_fallback

    def get_attr_list(self, attr):
        return super(CheckboxCol, self).get_attr_list(None)

    def text(self, item, attr_list):
        if attr_list:
            return self.from_attr_list(item, attr_list)
        elif self.text_fallback:
            return self.text_fallback
        else:
            return self.name

    def td_contents(self, item, attr_list):
        text = self.td_format(self.text(item, attr_list))
        attrs = dict(type='checkbox', value=text, name='input_checkbox')
        return html.element('input', attrs=attrs, content=' ', escape_content=False)


class ExternalURLCol(Col):
    def __init__(self, name, url_attr, **kwargs):
        self.url_attr = url_attr
        super(ExternalURLCol, self).__init__(name, **kwargs)

    def td_contents(self, item, attr_list):
        text = self.from_attr_list(item, attr_list)
        url = self.from_attr_list(item, [self.url_attr])
        return html.element('a', {'href': url}, content=text)


class AllConcertsTable(Table):
    checkbox = CheckboxCol(' ', attr_list=['id'], text_fallback='')
    date = Col('Date')
    artist = Col('Leading Artist')
    event = Col('Event')
    country = Col('Country')
    city = Col('City')


class ResultsConcertsTable(Table):
    date = Col('Date')
    artist = Col('Leading Artist')
    event_name = ExternalURLCol('Event Name', url_attr='kick_link', attr='event')
    country = Col('Country')
    city = Col('City')
    # photo


def _get_mysql_date_format(date):
    stripped_date = date.strip()
    day, month, year = stripped_date.split('/')
    return f'20{year}-{month}-{day}'


def _get_date_range_mysql(date_range_input):
    start, end = date_range_input.split('-')
    return _get_mysql_date_format(start), _get_mysql_date_format(end)


def _get_normal_date(sql_date):
    return f'{sql_date.day}/{sql_date.month}/{sql_date.year}'


def _format_displayed_concerts(displayed_concerts):
    for concert in displayed_concerts:
        concert['date'] = _get_normal_date(concert['date'])
        event = concert['event']
        display, *_ = event.rpartition('(')
        if display:
            concert['event'] = display.strip()


@app.route('/date_range_process')
def date_range_process():
    try:
        global date_range
        date_range_result = request.args.get('date_range')
        date_range.start, date_range.end = _get_date_range_mysql(date_range_result)
        are_there_shows = DBConnection.execute_query(
            queries.are_there_concerts_on_these_dates(date_range.start, date_range.end))
        if not are_there_shows:
            return jsonify(result='Sorry, no concerts on these dates')
        else:
            return jsonify(result='Great time to travel!')
    except Exception as e:
        return str(e)


@app.route('/genres_process')
def genres_process():
    global genres_list
    genres_list = ast.literal_eval((request.args.get('chosen_genres')))
    for genre in genres_list:
        genre['genre'] = genre['genre'].lower()
    # genres_list = chosen_genres.split(',')
    # print(f'genres_list:{genres_list}')
    if genres_list == ['']:
        return jsonify(result='')
    return jsonify(result='Great Choices')
    # TODO: Make sure genre is picked only once
    # TODO: Make sure the DB call is being done only once


@app.route('/locations_process')
def locations_process():
    global locations_list
    locations_list = ast.literal_eval(request.args.get('chosen_locations'))
    # locations_list = chosen_locations.split(',')
    # print(f'locations_list:{locations_list}')
    if locations_list == ['']:
        return jsonify(result='')
    return jsonify(result='Great Choices')


@app.route('/artists_process')
def artists_process():
    global artists_list
    artists_list = ast.literal_eval(request.args.get('chosen_artists'))
    # artists_list = chosen_artists.split(',')
    # print(f'genres_list:{genres_list}')
    if artists_list == ['']:
        return jsonify(result='')
    return jsonify(result='Great Choices')


@app.route('/get_artists')
def get_artists():
    shown_artists_list = DBConnection.execute_query(
        queries.query_get_artists(date_range.start, date_range.end, locations_list))
    result = {'results': shown_artists_list}
    return result


@app.route('/get_genres')
def get_genres():
    shown_genres_list = DBConnection.execute_query(queries.query_get_genres(date_range.start, date_range.end))
    for genre in shown_genres_list:
        genre['genre'] = genre['genre'].title()
    # TODO: take care of capitalize and the alert
    return {'results': shown_genres_list}


@app.route('/get_locations')
def get_locations():
    # print('in get_locations')
    shown_locations_list = DBConnection.execute_query(queries.query_get_locations(date_range.start, date_range.end, genres_list))
    result = {'results': shown_locations_list}
    return result


@app.route('/concerts', methods=['GET', 'POST'])
def process_form():
    global matching_concerts
    concerts_table = []
    if request.method == "GET":
        return "Please submit the form instead"
    else:  # POST
        warmup = True if request.form.get('warmUp') else False
        if request.form.get("keyWord"):  # The user inserted a filter
            keyword = request.form.get("keyWord")
            matching_concerts_ids = []
            for concert in matching_concerts:
                matching_concerts_ids.append(concert['id'])
            if len(matching_concerts_ids) == 1:
                matching_concerts_ids.append(-1)
            filtered_concerts_ids = DBConnection.execute_query(queries.query_get_filtered_concerts(tuple(matching_concerts_ids), keyword))
            for concert in matching_concerts:
                for event_id in filtered_concerts_ids:
                    if event_id['id'] == concert['id']:
                        concerts_table.append(concert)
        else:  # The first time the user got to the page
            matching_concerts = DBConnection.execute_query(queries.query_get_concerts(date_range.start, date_range.end, genres_list,
                                                           locations_list, artists_list, warmup))
            _format_displayed_concerts(matching_concerts)
            concerts_table = matching_concerts.copy()

        displayed_concerts_table = (AllConcertsTable(concerts_table, classes=['table']) if concerts_table
                                    else 'No matching concerts')
        # TODO: !!!!!!!!!!!!!!!!!!!!   BLOCK SUBMIT    !!!!!!!!!!!!!!!!!
        # TODO: Don't call the DB again when there is no filter. unfilter button
        # TODO: LIMIT TABLE
    return render_template('concerts.html', concerts_table=displayed_concerts_table)


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == "GET":
        return "Please submit the form instead"
    else:
        checkbox_values = request.form.getlist('input_checkbox')
    if not checkbox_values:
        shown_chosen_concerts = "No concerts were chosen"
    else:
        event_artist = []
        checkbox_values = [int(event_id) for event_id in checkbox_values]
        for event_id in checkbox_values:
            for concert in matching_concerts:
                if event_id == concert['id']:
                    event_artist.append((event_id, concert['artist_id']))
        if len(event_artist) == 1:
            event_artist.append((-1, -1))
        chosen_concerts = DBConnection.execute_query(queries.query_get_summary(tuple(event_artist)))
        _format_displayed_concerts(chosen_concerts)
        shown_chosen_concerts = ResultsConcertsTable(chosen_concerts, classes=['table'])
    return render_template('results.html', chosen_concerts=shown_chosen_concerts)


@app.route('/check_new_dates')
def check_new_chosen_dates():
    result = ''
    date_range_result = request.args.get('date_range')
    date_range.start, date_range.end = _get_date_range_mysql(date_range_result)
    new_possible_genres_dict = DBConnection.execute_query(queries.query_get_genres(date_range.start, date_range.end))
    new_possible_genres = {genre['genre'] for genre in new_possible_genres_dict}
    existing_genres_set = {genre['genre'] for genre in new_possible_genres_dict}
    diff = existing_genres_set.difference(new_possible_genres)
    if diff:
        result = 'There are no shows in the following genre: {0}'.format(', '.join(diff))
    return jsonify(result=result)


@app.route('/get_recommendations')
def get_recommendations():
    recommendations = queries.query_get_recommendations()
    return jsonify(result=recommendations)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port="8081", debug=True)
