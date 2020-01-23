def are_there_concerts_on_these_dates(start_date, end_date):
    """

    :param start_date: The start date passed from the user, in the form of YYYY-MM-DD
    :param end_date: The end date passed from the user, in the form of YYYY-MM-DD
    :return: True or False
    """
    return True


def query_get_genres(start_date, end_date):
    """

    :param start_date: The start date passed from the user, in the form of YYYY-MM-DD
    :param end_date: The end date passed from the user, in the form of YYYY-MM-DD
    :return: A list of genres of shows in these dates
    """
    return ['Rock', 'Pop', 'Metal']


def query_get_artists(start_date, end_date, locations_list):
    """

    :param start_date: The start date passed from the user, in the form of YYYY-MM-DD
    :param end_date: The end date passed from the user, in the form of YYYY-MM-DD
    :param locations_list: How ever you want to get it
    :return: A list of artists
    """
    return ['RHCP', 'Florence and the machine', 'Hi']


def query_get_locations(start_date, end_date, genres_list):
    """

    :param start_date: The start date passed from the user, in the form of YYYY-MM-DD
    :param end_date: The end date passed from the user, in the form of YYYY-MM-DD
    :param genres_list: The list of genres the user picked, e.g. ['Rock', 'Pop', 'Metal']
    :return: A list of dictionaries of the form {"city": , "country": , "continent": }
    """
    print('in get_locations')
    return [
        {"city": "New York", "country": "USA", "continent": "America"},
        {"city": "Tel Aviv", "country": "Israel", "continent": "Europe"},
        {"city": "Berlin", "country": "Germany", "continent": "Europe"},
        {"city": "Adis Ababa", "country": "Ethiopia", "continent": "Africa"},
        {"city": "Paris", "country": "France", "continent": "Europe"}]


def query_get_recommendations():
    """

    :return: You tell me
    """


def query_get_concerts(start_date, end_date, genres_list, locations_list, artists_list):
    """

    :param start_date: The start date passed from the user, in the form of YYYY-MM-DD
    :param end_date: The end date passed from the user, in the form of YYYY-MM-DD
    :param genres_list: The list of genres the user picked, e.g. ['Rock', 'Pop', 'Metal']
    :param locations_list: How ever you want to get it
    :param artists_list: The list of artists the user picked, e.g. ['RHCP', 'Florence and the machine']
    :return: A list of tuples of concerts.
    """


def query_get_filtered_concerts(start_date, end_date, genres_list, locations_list, artists_list, keyword):
    """

    :param start_date: The start date passed from the user, in the form of YYYY-MM-DD
    :param end_date: The end date passed from the user, in the form of YYYY-MM-DD
    :param genres_list: The list of genres the user picked, e.g. ['Rock', 'Pop', 'Metal']
    :param locations_list: How ever you want to get it
    :param artists_list: The list of artists the user picked, e.g. ['RHCP', 'Florence and the machine']
    :param keyword: A keyword from the user for a full-text query
    :return: A list of tuples of filtered concerts.
    """


def query_get_summary(concerts_ids_list):
    """
    We might not need it.
    :param concerts_ids_list: The chosen concerts ids
    :return: The chosen concerts based on their ids, including a link to songkick.
    """

