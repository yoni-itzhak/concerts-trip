import mysql.connector
import queries
from mysql.connector import errorcode

serverName = 'mysqlsrv1.cs.tau.ac.il'
user = 'DbMysql06'
password = 'bowie'
dbName = 'DbMysql06'


def execute_query(query, *kargs):
    config = {
        'user': 'DbMysql06',
        'password': 'bowie',
        'host': '127.0.0.1',  # Change to the DB server IP
        'database': 'DbMysql06',
        'port': '3305',
        'raise_on_warnings': True,
        # 'use_pure': True
    }
    cnx = mysql.connector.connect(**config)

    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = cnx.cursor(dictionary=True)
        print(query, kargs)
        cursor.execute(query, kargs)
        my_list = []
        for event in cursor:
            my_list.append(event)
        print(my_list)
        cnx.close()
        return my_list


# print(query('2020-03-11', '2020-03-12', ('pop', 'rock', 'jazz'), (('Paris', 'France'), ('Lisbon', 'Portugal')), ('Gost', 'Ninho')))
# print(query1('2020-03-11', '2020-03-12', (('Paris', 'France'), ('Lisbon', 'Portugal')), ('Gost', 'Ninho')))
# execute_query(query((12, 145, 22)))
# execute_query(query())
# print(query((12, 145, 22)))
# execute_query(queries.query_get_summary((2, 4, 6)))
#
def query():
    return """
    (
                                   SELECT DISTINCT E.id, E.date AS date, A.id as artist_id, A.artist_name as artist, AE.is_headline as headline, A.popularity as popularity, E.event_name AS event , E.popularity as e_popularity, CO.country_name as country, C.city_name as city, 0 as sort_key
                                   FROM  artists as A, artist_event as AE, events as E, venues as V, cities as C, countries as CO
                                   WHERE A.id = AE.artist_id AND AE.event_id = E.id
                                           AND E.venue_id = V.id AND V.city_id = C.id AND C.country_id = CO.id
                                           AND 1 = 1 AND (E.date BETWEEN "2020-01-29" AND "2020-01-29")
                                           AND ('James Genus' = A.artist_name ) AND (('New York' =  C.city_name AND 'US' =  CO.country_name))) UNION (SELECT DISTINCT E.id, E.date AS date, A.id as artist_id, A.artist_name as artist, AE.is_headline as headline,
                            A.popularity as popularity, E.event_name AS event , E.popularity as e_popularity, CO.country_name as country, C.city_name as city, 0 as sort_key
    		            FROM (SELECT AP.artist_id AS id
            				        FROM players P, artist_player AP
            				        WHERE P.id = AP.player_id AND ('James Genus' = P.player_name )) AS artists_with_players,
    				        artists as A, artist_event as AE, events as E, venues as V, cities as C, countries as CO
                        WHERE A.id = artists_with_players.id AND A.id = AE.artist_id AND AE.event_id = E.id
    		                AND E.venue_id = V.id AND V.city_id = C.id AND C.country_id = CO.id
    		                AND 1 = 1 AND (E.date BETWEEN "2020-06-12" AND "2020-06-14")
    		                AND (('New York' =  C.city_name AND 'US' =  CO.country_name))) UNION (
                               SELECT DISTINCT E.id, E.date AS date, A.id as artist_id, A.artist_name as artist, AE.is_headline as headline, A.popularity as popularity, E.event_name AS event, E.popularity as e_popularity, CO.country_name as country, C.city_name as city, 1 as sort_key
                               FROM genres as G, artist_genre as AG, artist_event as AE, events as E, venues as V, cities as C, countries as CO, artists AS A
                               WHERE G.id = AG.genre_id AND AG.artist_id = AE.artist_id AND AE.event_id = E.id AND AE.is_headline = 1
                                       AND E.venue_id = V.id AND V.city_id = C.id AND C.country_id = CO.id
                                        AND AG.artist_id = A.id AND (E.date BETWEEN "2020-01-29" AND "2020-01-29")
                                       AND (G.genre_name LIKE '%jazz drums%') AND (('New York' =  C.city_name AND 'US' =  CO.country_name)))
                                       """


def query2():
    return """
    (
                               SELECT DISTINCT E.id, E.date AS date, A.id as artist_id, A.artist_name as artist, AE.is_headline as headline, A.popularity as popularity, E.event_name AS event, E.popularity as e_popularity, CO.country_name as country, C.city_name as city, 1 as sort_key
                               FROM genres as G, artist_genre as AG, artist_event as AE, events as E, venues as V, cities as C, countries as CO, artists AS A
                               WHERE G.id = AG.genre_id AND AG.artist_id = AE.artist_id AND AE.event_id = E.id AND AE.is_headline = 1
                                       AND E.venue_id = V.id AND V.city_id = C.id AND C.country_id = CO.id
                                        AND AG.artist_id = A.id AND (E.date BETWEEN "2020-01-29" AND "2020-01-29")
                                       AND (G.genre_name LIKE '%jazz drums%') AND (('New York' =  C.city_name AND 'US' =  CO.country_name)))
    """
# execute_query(query('2020-02-12', '2020-02-19',[{'city': 'Toronto', 'country': 'Canada'}]))
print("are_there_concerts_on_these_dates:")
print("\n")
print(queries.are_there_concerts_on_these_dates('2020-02-14', '2020-02-15'))
print("\n")
print("query_get_concerts:")
print("\n")
print(queries.query_get_concerts('2020-02-14', '2020-02-15', [{"genre": "rock"}], [{"city": "Toronto", "country": "Canada"}], [{"artist": "Post Malone"}], 0))
print("\n")
print("query_get_locations:")
print("\n")
print(queries.query_get_locations('2020-02-14', '2020-02-15', [{"genre": "rock"}]))
print("\n")
print("query_get_artists:")
print("\n")
print(queries.query_get_artists('2020-02-14', '2020-02-15', [{"city": "Toronto", "country": "Canada"}]))
print("\n")
print("query_get_genres:")
print("\n")
print(queries.query_get_genres('2020-02-14', '2020-02-15'))
print("\n")
print("get_best_city_per_main_genre:")
print("\n")
print(queries.get_best_city_per_main_genre())
print("\n")
print("get_top_3_city_per_continent_by_event_number:")
print("\n")
print(queries.get_top_3_city_per_continent_by_event_number())
print("\n")
print("get_top_3_city_per_continent_by_artist_followers:")
print("\n")
print(queries.get_top_3_city_per_continent_by_artist_followers())
print("\n")
print("get_last_2_city_per_continent_by_artist_followers:")
print("\n")
print(queries.get_last_2_city_per_continent_by_artist_followers())
print("\n")
print("query_get_summary:")
print("\n")
print(queries.query_get_summary(((3, 1794), (4, 6592))))
print("\n")
print("query_get_filtered_concerts:")
print("\n")
print(queries.query_get_filtered_concerts((3, 4), "keyword"))
