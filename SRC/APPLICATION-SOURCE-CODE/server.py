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


class ImgCol(Col):
    def __init__(self, name, img_attr, **kwargs):
        self.img_attr = img_attr
        super(ImgCol, self).__init__(name, **kwargs)

    def td_contents(self, item, attr_list):
        img = self.from_attr_list(item, [self.img_attr])
        return html.element('img', {'src': img, 'alt': 'hi', 'height': 80, 'width': 80})


class AllConcertsTable(Table):
    checkbox = CheckboxCol(' ', attr_list=['id'], text_fallback='')
    date = Col('Date')
    artist = Col('Leading Artist')
    event = Col('Event')
    country = Col('Country')
    city = Col('City')


class ResultsConcertsTable(Table):
    date = Col('Date')
    location = ExternalURLCol('Location', url_attr='venue_link', attr='location')
    event_name = ExternalURLCol('Event Name', url_attr='kick_link', attr='event')
    photo = ImgCol(' ', img_attr='photo')


class RecommendShowsTable(Table):
    city = Col('Cities')
    cnt = Col('Number of shows')


class RecommendArtistsTable(Table):
    city = Col('Cities')
    sum = Col('Sum of Artists\' Followers')


class RecommendGenreTable(Table):
    genre = Col('Genre')
    city = Col('City')


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


def _format_displayed_result_concerts(displayed_concerts):
    for concert in displayed_concerts:
        concert['date'] = _get_normal_date(concert['date'])
        event = concert['event']
        display, *_ = event.rpartition('(')
        if display:
            concert['event'] = display.strip()
        location_tuple = (concert['venue_name'], concert['city'], concert['country'])
        concert['location'] = ', '.join(location_tuple)
        concert['venue_link'] = 'https://www.google.com/maps/place/{0},{1}'.format(concert['lat'], concert['lon'])


@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('405_error.html'), 405


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404_error.html'), 404


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
        return render_template('server_error.html', error_str=str(e))


@app.route('/genres_process', methods=['POST'])
def genres_process():
    try:
        global genres_list
        genres_list_str = request.get_json()
        if genres_list_str:
            genres_list = ast.literal_eval(genres_list_str)
        for genre in genres_list:
            genre['genre'] = genre['genre'].lower()
        return jsonify(result='Success')
    except Exception as e:
        return render_template('server_error.html', error_str=str(e))


@app.route('/locations_process', methods=['POST'])
def locations_process():
    try:
        global locations_list
        locations_list_str = request.get_json()
        if locations_list_str:
            locations_list = ast.literal_eval(locations_list_str)
        return jsonify(result='Success')
    except Exception as e:
        return render_template('server_error.html', error_str=str(e))


@app.route('/artists_process', methods=['POST'])
def artists_process():
    try:
        global artists_list
        artists_list_str = request.get_json()
        if artists_list_str:
            artists_list = ast.literal_eval(artists_list_str)
        return jsonify(result='Success')
    except Exception as e:
        return render_template('server_error.html', error_str=str(e))


@app.route('/get_artists')
def get_artists():
    try:
        shown_artists_list = DBConnection.execute_query(
            queries.query_get_artists(date_range.start, date_range.end, locations_list))
        result = {'results': shown_artists_list}
        return result
    except Exception as e:
        return render_template('server_error.html', error_str=str(e))


@app.route('/get_genres')
def get_genres():
    try:
        shown_genres_list = DBConnection.execute_query(queries.query_get_genres(date_range.start, date_range.end))
        for genre in shown_genres_list:
            genre['genre'] = genre['genre'].title()
        return {'results': shown_genres_list}
    except Exception as e:
        return render_template('server_error.html', error_str=str(e))


@app.route('/get_locations')
def get_locations():
    try:
        shown_locations_list = DBConnection.execute_query(queries.query_get_locations(date_range.start, date_range.end, genres_list))
        result = {'results': shown_locations_list}
        return result
    except Exception as e:
        return render_template('server_error.html', error_str=str(e))


@app.route('/concerts', methods=['GET', 'POST'])
def process_form():
    try:
        global matching_concerts
        if request.method == "GET":
            return render_template('submit_form.html')
        else:  # POST
            warm_up = True if request.form.get('warmUp') else False
            matching_concerts = DBConnection.execute_query(
                queries.query_get_concerts(date_range.start, date_range.end, genres_list,locations_list, artists_list,
                                           warm_up))
            _format_displayed_concerts(matching_concerts)
            concerts_table = matching_concerts.copy()
            if len(concerts_table) > 50:
                concerts_table = concerts_table[:50]
            displayed_concerts_table = (AllConcertsTable(concerts_table, classes=['table']) if concerts_table
                                        else 'No matching concerts')
        return render_template('concerts.html', concerts_table=displayed_concerts_table)
    except Exception as e:
        return render_template('server_error.html', error_str=str(e))


@app.route('/concerts_filter', methods=['POST'])
def concerts_filter():
    try:
        matching_concerts_ids = []
        concerts_table = []
        if request.form.get("keyWord"):  # The user inserted a filter
            keyword = request.form.get("keyWord")
            for concert in matching_concerts:
                matching_concerts_ids.append(concert['id'])
            if len(matching_concerts_ids) == 1:
                matching_concerts_ids.append(-1)
            filtered_concerts_ids = DBConnection.execute_query(
                queries.query_get_filtered_concerts(tuple(matching_concerts_ids), keyword))
            for concert in matching_concerts:
                for event_id in filtered_concerts_ids:
                    if event_id['id'] == concert['id']:
                        concerts_table.append(concert)
        displayed_concerts_table = (AllConcertsTable(concerts_table, classes=['table']) if concerts_table
                                    else 'No matching concerts')
        return render_template('concerts_filter.html', concerts_table=displayed_concerts_table)
    except Exception as e:
        return render_template('server_error.html', error_str=str(e))


@app.route('/results', methods=['GET', 'POST'])
def results():
    try:
        if request.method == "GET":
            return render_template('submit_form.html')
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
            _format_displayed_result_concerts(chosen_concerts)
            shown_chosen_concerts = ResultsConcertsTable(chosen_concerts, classes=['table'])
        return render_template('results.html', chosen_concerts=shown_chosen_concerts)
    except Exception as e:
        return render_template('server_error.html', error_str=str(e))


@app.route('/check_new_dates')
def check_new_chosen_dates():
    try:
        result = ''
        date_range_result = request.args.get('date_range')
        date_range.start, date_range.end = _get_date_range_mysql(date_range_result)
        new_possible_genres_dict = DBConnection.execute_query(queries.query_get_genres(date_range.start, date_range.end))
        new_possible_genres = {genre['genre'] for genre in new_possible_genres_dict}
        existing_genres_set = {genre['genre'] for genre in genres_list}
        diff = existing_genres_set.difference(new_possible_genres)
        if diff:
            result = 'There are no shows in the following genre on the new date: {0}'.format(', '.join(diff))
        return jsonify(result=result)
    except Exception as e:
        return render_template('server_error.html', error_str=str(e))


def _get_recommended_shows(recommend_shows_list, continent):
    recommend_shows_formatted_list = []
    for record in recommend_shows_list:
        if record['con'] == continent:
            recommend_shows_formatted_list.append(record)
    return RecommendShowsTable(recommend_shows_formatted_list, classes=['table'])


def _get_recommended_genres(recommend_artists_list, worse_artists_list, continent):
    recommend_shows_formatted_list = []
    worse_artists_formatted_list = []
    for record in recommend_artists_list:
        if record['con'] == continent:
            recommend_shows_formatted_list.append(record)
    recommend_shows_formatted_list.append({'city': '...', 'sum': '...'})

    for record in worse_artists_list:
        if record['con'] == continent:
            worse_artists_formatted_list.append(record)
    if len(worse_artists_formatted_list) > 2:
        worse_artists_formatted_list = worse_artists_formatted_list[-2:]
    recommend_shows_formatted_list.extend(worse_artists_formatted_list)
    return RecommendArtistsTable(recommend_shows_formatted_list, classes=['table'])


@app.route('/')
def index():
    try:
        recommend_shows_list = DBConnection.execute_query(queries.get_top_3_city_per_continent_by_event_number())
        recommend_shows_africa = _get_recommended_shows(recommend_shows_list, 'Africa')
        recommend_shows_asia = _get_recommended_shows(recommend_shows_list, 'Asia')
        recommend_shows_europe = _get_recommended_shows(recommend_shows_list, 'Europe')
        recommend_shows_north_america = _get_recommended_shows(recommend_shows_list, 'North America')
        recommend_shows_south_america = _get_recommended_shows(recommend_shows_list, 'South America')
        recommend_shows_north_oceania = _get_recommended_shows(recommend_shows_list, 'Oceania')

        recommend_artists_list = DBConnection.execute_query(queries.get_top_3_city_per_continent_by_artist_followers())
        worse_artists_list = DBConnection.execute_query(queries.get_last_2_city_per_continent_by_artist_followers())
        recommend_artists_africa = _get_recommended_genres(recommend_artists_list, worse_artists_list, 'Africa')
        recommend_artists_asia = _get_recommended_genres(recommend_artists_list, worse_artists_list, 'Asia')
        recommend_artists_europe = _get_recommended_genres(recommend_artists_list, worse_artists_list, 'Europe')
        recommend_artists_north_america = _get_recommended_genres(recommend_artists_list, worse_artists_list, 'North America')
        recommend_artists_south_america = _get_recommended_genres(recommend_artists_list, worse_artists_list, 'South America')
        recommend_artists_north_oceania = _get_recommended_genres(recommend_artists_list, worse_artists_list, 'Oceania')

        city_genre_recommend = DBConnection.execute_query(queries.get_best_city_per_main_genre())
        for record in city_genre_recommend:
            record['genre'] = record['genre'].title()
        recommend_city_genre = RecommendGenreTable(city_genre_recommend, classes=['table'])

        return render_template('index.html',
                               recommend_shows_africa=recommend_shows_africa,
                               recommend_shows_asia=recommend_shows_asia,
                               recommend_shows_europe=recommend_shows_europe,
                               recommend_shows_north_america=recommend_shows_north_america,
                               recommend_shows_south_america=recommend_shows_south_america,
                               recommend_shows_north_oceania=recommend_shows_north_oceania,
                               recommend_artists_africa=recommend_artists_africa,
                               recommend_artists_asia=recommend_artists_asia,
                               recommend_artists_europe=recommend_artists_europe,
                               recommend_artists_north_america=recommend_artists_north_america,
                               recommend_artists_south_america=recommend_artists_south_america,
                               recommend_artists_north_oceania=recommend_artists_north_oceania,
                               recommend_city_genre=recommend_city_genre)
    except Exception as e:
        return render_template('server_error.html', error_str=str(e))


if __name__ == '__main__':
    app.run(port="8081", debug=True)
    # app.run(host="delta-tomcat-vm", port="40997", debug=False) in production
