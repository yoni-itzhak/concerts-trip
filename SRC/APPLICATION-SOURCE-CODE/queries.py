def are_there_concerts_on_these_dates(start_date, end_date):
    """

    :param start_date: The start date passed from the user, in the form of YYYY-MM-DD
    :param end_date: The end date passed from the user, in the form of YYYY-MM-DD
    :return: boolean
    """
    return True


def query_get_genres():
    return ['Rock', 'Pop', 'Metal']


def query_get_artists():
    return ['RHCP', 'Adele', 'Florence and the machine', 'Hi']


def query_get_locations():
    print('in get_locations')
    return [
        {"city": "New York", "country": "USA", "continent": "America"},
        {"city": "Tel Aviv", "country": "Israel", "continent": "Europe"},
        {"city": "Berlin", "country": "Germany", "continent": "Europe"},
        {"city": "Adis Ababa", "country": "Ethiopia", "continent": "Africa"},
        {"city": "Paris", "country": "France", "continent": "Europe"}]
