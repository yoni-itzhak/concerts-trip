import csv
import mysql.connector
import datetime

configs = {
        'user': 'DbMysql06',
        'password': 'bowie',
        'host': '127.0.0.1',
        'database': 'DbMysql06',
        'port': '3305',
        'raise_on_warnings': True,
        # 'use_pure': True
    }

db = mysql.connector.connect(**configs)
db_cur = db.cursor()


def venue_tuple(row):
    cap = 0
    an_id = int(row["new_venue_id"])
    name = row["name"]
    lat = str(row["lat"])
    lon = str(row["lon"])
    desc = row["description"]
    addr = row["address"]
    city_id = int(row["city_id"])
    site = row["site"]
    phone = row["contact_at"]
    try:
        cap = int(row["capacity"])
    except ValueError:
        cap = -1
    return an_id, name, lat, lon, desc, addr, city_id, site, cap, phone


def format_time(time_str):
    if time_str == "":
        return ""
    to_strp = time_str
    split_time = to_strp.split(" ")[0].split(":")
    if "pm" in time_str.lower() and split_time[0] != '12':
        return datetime.time(int(split_time[0]) + 12, int(split_time[1]), int(split_time[2]))
    else:
        return datetime.time(int(split_time[0]), int(split_time[1]), int(split_time[2]))


def format_date(date_str):
    stripped = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    to_out = datetime.date(stripped.year, stripped.month, stripped.day)
    return to_out


def event_tuple(row):
    ev_id = row["id"]
    name = row["name"]
    popularity = float(row["popularity"])
    date = format_date(row["date"])
    time = format_time(row["time"])
    venue_id = int(row["venue_id"])
    return ev_id, name, popularity, date, time, venue_id


def artist_tuple(row):
    ar_id = row["id"]
    name = row["name"]
    pop = int(row["popularity"])
    fol = int(row["followers"])
    desc = row["description"]
    img = row["image_url"]
    h = row["height"]
    w = row["width"]
    return ar_id, name, pop, fol, desc, img, h, w


def push_events():
    frmt = "%H:%M:%S %p"
    query = "INSERT INTO events(id, event_name, popularity, date, time, venue_id) VALUES (%s,%s,%s,%s,%s,%s)"
    path = r"C:\Users\Itamar\Desktop\base_proj\to_push\events.csv"
    with open(path, "r") as raw:
        reader = csv.DictReader(raw)
        for row in reader:
            tup = event_tuple(row)
            db_cur.execute(query, tup)
    db.commit()


def push_artists():
    path = r"C:\Users\Itamar\Desktop\base_proj\to_push\artists.csv"
    query = "INSERT INTO artists(id,artist_name,popularity, followers, description, img_link, img_height, img_width) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    with open(path, "r") as raw:
        reader = csv.DictReader(raw)
        for row in reader:
            tup = artist_tuple(row)
            db_cur.execute(query, tup)
    raw.close()
    db.commit()


def push_combine_evart():
    path = r"C:\Users\Itamar\Desktop\base_proj\to_push\no_dup_arev.csv"
    query = "INSERT INTO artist_event(artist_id, event_id, is_headline) VALUES (%s,%s,%s)"
    with open(path, "r") as raw:
        reader = csv.DictReader(raw)
        for row in reader:
            head = 1;
            if row["isMain"] == "support":
                head = 0
            tup = (row["artist_id"],row["event_id"], head)
            db_cur.execute(query, tup)
    raw.close()
    db.commit()


def push_players():
    path = r"C:\Users\Itamar\Desktop\base_proj\to_push\players.csv"
    query = "INSERT INTO players(id, player_name) VALUES (%s,%s)"
    with open(path, "r") as raw:
        reader = csv.DictReader(raw)
        for row in reader:
            tup = (row["id"], row["name"])
            db_cur.execute(query, tup)
    raw.close()
    db.commit()


def push_genres():
    path = r"C:\Users\Itamar\Desktop\base_proj\to_push\genres.csv"
    query ="INSERT INTO genres(id, genre_name, popularity) VALUES (%s,%s,%s)"
    with open(path, "r") as raw:
        reader = csv.DictReader(raw)
        for row in reader:
            tup = (int(row["id"]), row["name"], int(row["popularity"]))
            db_cur.execute(query, tup)
    raw.close()
    db.commit()


def push_combine_arpla():
    path = r"C:\Users\Itamar\Desktop\base_proj\to_push\artist_player.csv"
    query = "INSERT INTO artist_player(player_id, artist_id) VALUES (%s, %s)"
    with open(path, "r") as raw:
        reader = csv.DictReader(raw)
        for row in reader:
            tup = (int(row["player_id"]), int(row["artist_id"]))
            db_cur.execute(query, tup)
    raw.close()
    db.commit()


def push_countries():
    path = r"C:\Users\Itamar\Desktop\base_proj\to_push\countries.csv"
    query = "INSERT INTO countries(id, country_name, continent_id) VALUES (%s,%s,%s)"
    with open(path, "r") as raw:
        reader = csv.DictReader(raw)
        for row in reader:
            tup = (int(row["id"]), row["name"], int(row["continent_id"]))
            db_cur.execute(query, tup)
    raw.close()
    db.commit()


def push_cities():
    path = r"C:\Users\Itamar\Desktop\base_proj\to_push\better_cities.csv"
    query = "INSERT INTO cities(id, city_name, country_id) VALUES (%s, %s, %s)"
    with open(path, "r") as raw:
        reader = csv.DictReader(raw)
        for row in reader:
            tup = (int(row["id"]), row["new_city_name"], int(row["country_id"]))
            db_cur.execute(query, tup)
    raw.close()
    db.commit()


def push_argen():
    path = r"C:\Users\Itamar\Desktop\base_proj\to_push\artist_genre.csv "
    query = "INSERT INTO artist_genre(artist_id, genre_id) VALUES (%s, %s)"
    with open(path, "r") as raw:
        reader = csv.DictReader(raw)
        for row in reader:
            tup = (int(row["artist_id"]), int(row["genre_id"]))
            db_cur.execute(query, tup)
    raw.close()
    db.commit()


def push_venues():
    tuple_list = []
    query = "INSERT INTO venues(id,name,lat,lon,description,address,city_id,website,capacity,phone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    path = r"C:\Users\Itamar\Desktop\base_proj\to_push\venues.csv"
    with open(path, "r") as raw:
        reader = csv.DictReader(raw)
        for row in reader:
            curr_tuple = venue_tuple(row)
            db_cur.execute(query,curr_tuple)
    db.commit()


def push_updates():
    query = 'UPDATE events SET kick_link = "{!s}" WHERE id = {!s}'
    path = r"C:\Users\Itamar\Desktop\base_proj\to_push\events_with_links.csv"
    with open(path, "r") as raw:
        reader = csv.DictReader(raw)
        for row in reader:
            curr_query = query.format(row["event_link"], row["id"])
            db_cur.execute(curr_query)
    raw.close()
    db.commit()
