
def are_there_concerts_on_these_dates(start_date, end_date):
    """
    :param start_date: The start date passed from the user, in the form of YYYY-MM-DD
    :param end_date: The end date passed from the user, in the form of YYYY-MM-DD
    :return true/false
    """
    if start_date == "":
        start_date = '2020-01-27'
        end_date = '2023-02-12'

    return """
        SELECT E.id
        FROM events as E
        WHERE E.date BETWEEN \"{start}\" AND \"{end}\"
        """.format(start=start_date, end=end_date)



def query_get_genres(start_date, end_date):
    """
    :param start_date: The start date passed from the user, in the form of YYYY-MM-DD
    :param end_date: The end date passed from the user, in the form of YYYY-MM-DD
    :return: A list of genres of shows in these dates
    """
    if start_date == "":
        start_date = '2020-01-27'
        end_date = '2023-02-12'
    return """
    SELECT g.genre_name AS genre
    FROM genres as g, (SELECT DISTINCT G.id
                    FROM events AS E, genres as G, artist_genre as AG, artists as A, artist_event as AE
                    WHERE A.id = AG.artist_id AND AG.genre_id = G.id
                        AND AE.artist_id = A.id AND E.id = AE.event_id
                        AND E.date >= \"{start_date}\" AND  E.date <= \"{end_date}\") AS available_genre
    WHERE g.id = available_genre.id
    ORDER BY g.popularity DESC
    """.format(start_date=start_date, end_date=end_date)



def query_get_artists(start_date, end_date, locations_list):
    """
    :param start_date: The start date passed from the user, in the form of YYYY-MM-DD
    :param end_date: The end date passed from the user, in the form of YYYY-MM-DD
    :param locations_list: How ever you want to get it (we want city,country)
    :return: A list of artists
    """

    location_check = ""
    for i, loc_dict in enumerate(locations_list):
        city = loc_dict['city']
        country = loc_dict['country']
        location_check += "('" + city + "' =  event_artist_by_date.city AND '" + country + "' =  event_artist_by_date.country)"
        if i < len(locations_list) - 1:
            location_check += " OR "

    if start_date == "":
        start_date = '2020-01-27'
        end_date = '2023-02-12'

    query = """             
                        FROM artists a, (SELECT DISTINCT A.id
                                        FROM artists as A, (SELECT AE.artist_id as artist_id, c.city_name as city, co.country_name as country
                                                            FROM events as E, artist_event as AE, venues as V, cities as c, countries as co
                                                            WHERE c.country_id = co.id AND V.city_id = c.id
                                                                AND AE.event_id = E.id AND E.venue_id = V.id
                                                                AND (E.date BETWEEN \"{start}\" AND \"{end}\")) as event_artist_by_date
                                        WHERE A.id = event_artist_by_date.artist_id AND (""" + location_check + """)) as available_artists
                        WHERE a.id = available_artists.id 
                        ORDER BY a.popularity DESC, a.followers DESC"""
    big_query = "SELECT artist FROM ((SELECT a.artist_name AS artist, a.popularity as popularity " + query + """ ) UNION (SELECT p.player_name, -1 as popularity
                                                FROM artists a, artist_player ap, players p
                                                WHERE a.artist_name IN ( SELECT a.artist_name AS artist """ + query + """) 
                                                AND a.id = ap.artist_id AND p.id = ap.player_id )
                                                 order by popularity DESC) as t"""
    return big_query.format(end=end_date, start=start_date)


def query_get_locations(start_date, end_date, genre_list):
    """
    :param start_date: The start date passed from the user, in the form of YYYY-MM-DD
    :param end_date: The end date passed from the user, in the form of YYYY-MM-DD
    :param genre_list: The list of genres the user picked, e.g. ['Rock', 'Pop', 'Metal']
    :return: A list of dictionaries of the form {"city": , "country": , "continent": }
    """
    genre_check = ""
    for i, genre_dict in enumerate(genre_list):
        genre = genre_dict['genre']
        genre_check += "G.genre_name LIKE '%" + genre + "%'"
        if i < len(genre_list) - 1:
            genre_check += " OR "
    if start_date == "":
        start_date = '2020-01-27'
        end_date = '2023-02-12'

    query = """
        SELECT c.city_name as city, co.country_name AS country , con.continent_name AS continent
        FROM cities c, countries co, continents con,(SELECT C.id AS city_id, COUNT( DISTINCT E.id) as event_sum
                                                    FROM genres as G, artist_genre as AG, artist_event as AE,
                                                        events as E, venues as V, cities as C, countries as CO, continents as CON
                                                    WHERE G.id = AG.genre_id AND AG.artist_id = AE.artist_id AND AE.event_id = E.id
                                                        AND E.venue_id = V.id AND V.city_id = C.id AND C.country_id = CO.id
                                                        AND CO.continent_id = CON.id AND (E.date BETWEEN \"{start}\" AND \"{end}\") 
                                                        AND (""" + genre_check + """)  GROUP BY C.id) as city_event_sum
            WHERE c.id = city_event_sum.city_id AND c.country_id = co.id AND co.continent_id = con.id
            ORDER BY city_event_sum.event_sum DESC"""
    return query.format(end=end_date, start=start_date)


def query_get_concerts(start_date, end_date, genre_list, locations_list, artists_list, warm_up):
    """
    :param start_date: The start date passed from the user, in the form of YYYY-MM-DD
    :param end_date: The end date passed from the user, in the form of YYYY-MM-DD
    :param genre_list: The list of genres the user picked, e.g. ['Rock', 'Pop', 'Metal']
    :param locations_list: How ever you want to get it
    :param artists_list: The list of artists the user picked, e.g. ['RHCP', 'Florence and the machine']
    :param warm_up: An indicator if the user wants to include also warm up shows
    :return: A list of tuples of concerts.
    """
    if start_date == "":
        start_date = '2020-01-27'
        end_date = '2023-02-12'
    genre_check = ""
    for i, genre_dict in enumerate(genre_list):
        genre = genre_dict['genre']
        genre_check += "G.genre_name LIKE '%" + genre + "%'"
        if i < len(genre_list) - 1:
            genre_check += " OR "

    location_check = ""
    for i, loc_dict in enumerate(locations_list):
        city = loc_dict['city']
        country = loc_dict['country']
        location_check += "('" + city + "' =  C.city_name AND '" + country + "' =  CO.country_name)"
        if i < len(locations_list) - 1:
            location_check += " OR "

    if artists_list:
        artist_check = ""
        for i, artist_dict in enumerate(artists_list):
            artist = artist_dict['artist']
            artist_check += "'" + artist + "'" + " = A.artist_name "
            if i < len(artists_list) - 1:
                artist_check += " OR "

        player_check = """(SELECT AP.artist_id AS id
            				        FROM players P, artist_player AP
            				        WHERE P.id = AP.player_id AND ("""
        for i, artist_dict in enumerate(artists_list):
            artist = artist_dict['artist']
            player_check += "'" + artist + "'" + " = P.player_name "
            if i < len(artists_list) - 1:
                player_check += " OR "
        player_check += "))"

    if warm_up:
        warm_up_statement = "1 = 1"
    else:
        warm_up_statement = "AE.is_headline = 1"

    query1 = """
                               SELECT DISTINCT E.id, E.date AS date, A.id as artist_id, A.artist_name as artist, AE.is_headline as headline, A.popularity as popularity, E.event_name AS event, E.popularity as e_popularity, CO.country_name as country, C.city_name as city, 1 as sort_key
                               FROM genres as G, artist_genre as AG, artist_event as AE, events as E, venues as V, cities as C, countries as CO, artists AS A
                               WHERE G.id = AG.genre_id AND AG.artist_id = AE.artist_id AND AE.event_id = E.id AND {warm_up}
                                       AND E.venue_id = V.id AND V.city_id = C.id AND C.country_id = CO.id
                                        AND AG.artist_id = A.id AND (E.date BETWEEN \"{start1}\" AND \"{end1}\") 
                                       AND (""" + genre_check + ") AND (" + location_check + ")"
    query = query1
    if artists_list:
        query2 = """
                                   SELECT DISTINCT E.id, E.date AS date, A.id as artist_id, A.artist_name as artist, AE.is_headline as headline, A.popularity as popularity, E.event_name AS event , E.popularity as e_popularity, CO.country_name as country, C.city_name as city, 0 as sort_key
                                   FROM  artists as A, artist_event as AE, events as E, venues as V, cities as C, countries as CO
                                   WHERE A.id = AE.artist_id AND AE.event_id = E.id
                                           AND E.venue_id = V.id AND V.city_id = C.id AND C.country_id = CO.id
                                           AND {warm_up} AND (E.date BETWEEN \"{start2}\" AND \"{end2}\") 
                                           AND (""" + artist_check + ") AND (" + location_check + ")"

        query3 = """SELECT DISTINCT E.id, E.date AS date, A.id as artist_id, A.artist_name as artist, AE.is_headline as headline,
                            A.popularity as popularity, E.event_name AS event , E.popularity as e_popularity, CO.country_name as country, C.city_name as city, 0 as sort_key
    		            FROM """ + player_check + """ AS artists_with_players,
    				        artists as A, artist_event as AE, events as E, venues as V, cities as C, countries as CO
                        WHERE A.id = artists_with_players.id AND A.id = AE.artist_id AND AE.event_id = E.id 
    		                AND E.venue_id = V.id AND V.city_id = C.id AND C.country_id = CO.id 
    		                AND {warm_up} AND (E.date BETWEEN "2020-06-12" AND "2020-06-14") 
    		                AND (""" + location_check + ")"
        query = "(" + query2 + ") UNION (" + query3 + ") UNION " + "(" + query1 + ")"

    big_query = """
                  WITH ORDERED AS
                  ( SELECT distinct id, date, artist_id, artist, event, e_popularity, country, city, sort_key,  ROW_NUMBER() OVER (PARTITION BY id ORDER BY headline DESC, popularity desc) AS rn
                  FROM (""" + query + """) as mytable)
                  SELECT *
                  FROM ORDERED
                  WHERE rn = 1
                  ORDER BY sort_key, date, e_popularity DESC"""
    if artists_list:
        return big_query.format(end1=end_date, end2=end_date, start1=start_date, start2=start_date,
                                warm_up=warm_up_statement)
    return big_query.format(end1=end_date, start1=start_date, warm_up=warm_up_statement)


def query_get_filtered_concerts(concerts_ids_list, keyword):
    """
    :param concerts_ids_list: The list of concerts's id
    :param keyword: A keyword from the user for a full-text query
    :return: A list of tuples of filtered concerts.
    """
    return """
    SELECT DISTINCT E.id
    FROM artists AS A, events AS E, venues AS V, artist_event AS AE 
    WHERE ((MATCH(A.description) AGAINST(\'\"{keyword}\"\')) 
	    OR (MATCH(V.description) AGAINST(\'\"{keyword}\"\')))
	    AND E.id IN {concerts_ids_list}
	    AND E.id = AE.event_id AND AE.artist_id = A.id AND V.id = E.venue_id
    """.format(concerts_ids_list=concerts_ids_list, keyword=keyword)


def query_get_summary(concerts_artists_ids_list):
    """
    We might not need it. we need it!!!
    :param concerts_artists_ids_list: The chosen concerts ids
    :return: The chosen concerts based on their ids, including a link to songkick.
    """
    return """
        SELECT DISTINCT e.date AS date, e.event_name as event, e.kick_link, co.country_name as country, c.city_name as city, a.img_link as photo, v.name as venue_name, v.lat, v.lon
        FROM  artists as a, artist_event as ae, events as e, venues as v, cities as c, countries as co, continents as con
        WHERE a.id = ae.artist_id AND ae.event_id = e.id
          AND e.venue_id = v.id AND v.city_id = c.id AND c.country_id = co.id
          AND co.continent_id = con.id
          AND (e.id, a.id) IN {concerts_artists_ids_list}
        """.format(concerts_artists_ids_list=concerts_artists_ids_list)


def get_best_city_per_main_genre():
    return """
               SELECT t1.genre, t1.city, t2.max_avg
        FROM genres g, (SELECT MG.genre_name as genre, c.city_name AS city, AVG(a.popularity) as avgArtistPopularity
            FROM (SELECT c.id AS id, COUNT(e.id) AS cnt 
                    FROM cities AS c, venues AS v, events AS e 
                    WHERE v.id = e.venue_id AND v.city_id = c.id 
                    GROUP BY c.id 
                    HAVING cnt > 10) AS city_event, venues AS v, artist_event AS ae, countries AS co, cities AS c, events AS e, artists AS a, artist_genre as ag, (SELECT g.id, g.genre_name, g.popularity FROM genres as g ORDER BY g.popularity DESC LIMIT 10) as MG
            WHERE city_event.id = v.city_id AND v.id = e.venue_id AND e.id = ae.event_id AND ae.artist_id = a.id AND ae.is_headline = 1
            AND ag.artist_id = a.id AND co.id = c.country_id AND c.id = city_event.id
            AND MG.id = ag.genre_id AND ag.artist_id = a.id
            GROUP BY MG.genre_name, c.city_name
            HAVING COUNT(*) > 10
            ORDER BY MG.genre_name, avgArtistPopularity DESC) AS t1, (SELECT genre, MAX(avgArtistPopularity) AS max_avg FROM (SELECT MG.genre_name as genre, c.city_name AS city, AVG(a.popularity) as avgArtistPopularity
            FROM (SELECT c.id AS id, COUNT(e.id) AS cnt 
                    FROM cities AS c, venues AS v, events AS e 
                    WHERE v.id = e.venue_id AND v.city_id = c.id 
                    GROUP BY c.id 
                    HAVING cnt > 10) AS city_event, venues AS v, artist_event AS ae, countries AS co, cities AS c, events AS e, artists AS a, artist_genre as ag, (SELECT g.id, g.genre_name, g.popularity FROM genres as g ORDER BY g.popularity DESC LIMIT 10) as MG
            WHERE city_event.id = v.city_id AND v.id = e.venue_id AND e.id = ae.event_id AND ae.artist_id = a.id AND ae.is_headline = 1
            AND ag.artist_id = a.id AND co.id = c.country_id AND c.id = city_event.id
            AND MG.id = ag.genre_id AND ag.artist_id = a.id
            GROUP BY MG.genre_name, c.city_name
            HAVING COUNT(*) > 10
            ORDER BY MG.genre_name, avgArtistPopularity DESC) AS t GROUP BY genre) as t2
    where t2.max_avg = t1.avgArtistPopularity AND t2.genre = t1.genre AND g.genre_name = t1.genre
    ORDER BY g.popularity desc"""


def get_top_3_city_per_continent_by_event_number():
    return """
    SELECT rs.con, rs.city, rs.cnt
    FROM (SELECT con, city, cnt, Rank() over (Partition BY con ORDER BY cnt DESC ) AS rnk
          FROM (SELECT con.continent_name as con, c.city_name as city, cnt
                    FROM (SELECT c.id as cityid, COUNT(e.id) as cnt
                            FROM cities as c, events AS e, venues v
                            WHERE e.venue_id = v.id AND v.city_id = c.id
                            GROUP BY c.id) AS cityEvent, continents as con, cities AS c, countries AS co
                    WHERE con.id = co.continent_id and cityEvent.cityid = c.id AND c.country_id = co.id
                    ORDER BY cnt DESC) AS t) AS rs
    WHERE rnk <=  3
    ORDER BY con, cnt desc
    """


def get_top_3_city_per_continent_by_artist_followers():
    return """
            SELECT rs.con, rs.city, rs.sum
            FROM (
                SELECT con, city, sum, Rank()
                  over (Partition BY con
                        ORDER BY sum DESC ) AS rnk
                FROM (SELECT con.continent_name as con, c.city_name as city, sum
        FROM (SELECT city_ten.id as cityid, SUM(a.followers) as sum
        		FROM events as e, artists AS a, venues AS v, artist_event AS ae, (SELECT c.id AS id, COUNT(e.id) AS cnt FROM cities AS c, venues AS v, events AS e WHERE v.id = e.venue_id AND v.city_id = c.id GROUP BY c.id HAVING cnt > 3) AS city_ten
        		WHERE e.venue_id = v.id AND v.city_id = city_ten.id AND e.id = ae.event_id AND ae.artist_id = a.id AND ae.is_headline = 1
        		GROUP BY city_ten.id) AS cityEvent, continents as con, cities AS c, countries AS co
        WHERE con.id = co.continent_id AND cityEvent.cityid = c.id AND c.country_id = co.id
        ORDER BY sum DESC) AS t
                ) rs WHERE rnk <= 3
        ORDER BY con, sum DESC"""


def get_last_2_city_per_continent_by_artist_followers():
    return """
    SELECT rs.*
    FROM (
        SELECT con, city, sum, Rank()
          over (Partition BY con
                ORDER BY sum ) AS rnk
        FROM (SELECT con.continent_name as con, c.city_name as city, sum
FROM (SELECT c.id as cityid, SUM(a.followers) as sum
		FROM cities AS c, events as e, artists AS a, venues AS v, artist_event AS ae
		WHERE e.venue_id = v.id AND v.city_id = c.id AND e.id = ae.event_id AND ae.artist_id = a.id AND ae.is_headline = 1
		GROUP BY c.id) AS cityEvent, continents as con, cities AS c, countries AS co
WHERE con.id = co.continent_id AND cityEvent.cityid = c.id AND c.country_id = co.id
ORDER BY sum) AS t
        ) rs WHERE rnk <= 2
ORDER BY con, sum DESC"""
