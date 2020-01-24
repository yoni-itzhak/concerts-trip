import requests
import csv
from time import sleep
import time

key = 'Kg38ZlH0nSOBf8rA'


def songkick_get_city(city, min_date, page):
    url = "https://api.songkick.com/api/3.0/metro_areas/{!s}/calendar.json"
    full_url = url.format(city)
    params = {"min_date": min_date, "apikey": key, "page": page}
    res_raw = requests.get(full_url, params=params)
    res = res_raw.json()
    return res


def parse_event(event):
    event_dict = dict({})
    event_list = []
    if event["status"] != 'ok':
        return []
    lineup = event["performance"]
    event_dict["location_id"] = event["venue"]["metroArea"]["id"]
    event_dict["songkicks_id"] = event["id"]
    event_dict["name"] = event["displayName"]
    event_dict["popularity"] = "{:.16f}".format(float(event["popularity"]))
    event_dict["date"] = event["start"]["date"]
    event_dict["time"] = event["start"]["time"]
    event_dict["date_as_datetime"] = event["start"]["datetime"]
    event_dict["venue_id"] = event["venue"]["id"]
    event_dict["venue_name"] = event["venue"]["displayName"]
    event_dict["venue_link"] = event["venue"]["uri"]
    for band in lineup:
        event_list.append(include_all_lineup(event_dict, band))
    return event_list


def get_city_metadata(res):
    all_results = res["resultsPage"]["totalEntries"]
    return all_results


def include_all_lineup(curr_dict, band):
    new_dict = curr_dict.copy()
    new_dict["songkick_artist_id"] = band["artist"]["id"]
    new_dict["is_main"] = band["billing"]
    new_dict["band_name"] = band["artist"]["displayName"]
    return new_dict


def add_event_to_list(res):
    parsed_event_list = []
    try:
        event_list = res["resultsPage"]["results"]["event"]
        for event in event_list:
            parsed_event = parse_event(event)
            parsed_event_list.extend(parsed_event)
    finally:
        return parsed_event_list


def write_output_to_csv(event_list, filename):
    with open(r"C:\Users\Itamar\Desktop\base_proj\{!s}.csv".format(filename), "a", newline="") as curr:
        curr_csv = csv.DictWriter(curr, fieldnames=event_list[0].keys())
        curr_csv.writeheader()
        for event in event_list:
            try:
                curr_csv.writerow(event)
            except UnicodeError:
                continue
    curr.close()


def get_event_details_tickets(event_list):
    all_events = []
    tmp = dict({})
    url_raw = "https://api.songkick.com/api/3.0/events/{!s}.json?apikey=Kg38ZlH0nSOBf8rA"
    for event in event_list:
        curr = tmp.copy()
        url = url_raw.format(event)
        res_raw = requests.get(url).json()
        try:
            res = res_raw["resultsPage"]
            curr["songkick_id"] = res["results"]["event"]["id"]
            curr["link"] = res["results"]["event"]["uri"]
            all_events.append(curr)
            sleep(0.4)
        except KeyError:
            continue
    return all_events


def get_all_events():
    events = []
    with open(r"C:\Users\Itamar\Desktop\base_proj\all_events_for_tickets.csv", "r") as raw:
        reader = csv.DictReader(raw)
        for row in reader:
            events.append(row["id"])
    raw.close()
    return events


def retrieve_ids_as_list():
    ids = []
    with open(r"C:\Users\Itamar\Desktop\base_proj\countries.csv", "r") as cnt:
        file = csv.DictReader(cnt)
        for row in file:
            ids.append(row["id"])
    cnt.close()
    return list(set(ids))


def get_all_cities_up_to_index(countries, index):
    all_shows = []
    good_cities = []
    cnt = 0
    for c_id in countries[:index]:
        res = songkick_get_city(str(c_id), "2020-01-27", 1)
        all_results = get_city_metadata(res)
        if (all_results) > 1000:
            good_cities.append(c_id)
        cnt += 1
        total = res["resultsPage"]["totalEntries"]
        if total == "0" or total == 0:
            continue
        tmp_list = add_event_to_list(res)
        all_shows.extend(tmp_list)
    print(cnt)
    return all_shows, good_cities


def iterate_good_cities(cities_list):
    all_shows = []
    for city in cities_list:
        i = 50
        while i < 70:
            print(str(i)+", "+city)
            res = songkick_get_city(str(city), "2020-01-27", i)
            if (res["resultsPage"]['results'] == {}):
                break
            print(res)
            tmp_list = add_event_to_list(res)
            all_shows.extend(tmp_list)
            i += 1
    return all_shows


def count_bands():
    bands = []
    with open(r"C:\Users\Itamar\Desktop\base_proj\all_shows.csv", "r") as c:
        reader = csv.DictReader(c)
        for row in reader:
            bands.append(row["band_name"])
    c.close()
    return list(set(bands))


def make_bands_xl():
    bands = count_bands()
    with open(r"C:\Users\Itamar\Desktop\base_proj\bands.csv", "w") as r:
        for band in bands:
            r.write(band+"\n")
    r.close()


def get_all_event_ids():
    events = []
    with open(r"C:\Users\Itamar\Desktop\base_proj\all_shows.csv", "r") as c:
        reader = csv.DictReader(c)
        for row in reader:
            events.append(row["songkicks_id"])
    c.close()
    return list(set(events))


def songkick_get_event(event_id):
    raw_url = "https://api.songkick.com/api/3.0/events/{!s}.json?apikey={!s}"
    url = raw_url.format(event_id, key)
    res = requests.get(url).json()["resultsPage"]["results"]["event"]


def all_venues():
    path = r"C:\Users\Itamar\Desktop\base_proj\venue.csv"
    venues = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            venues.append(row["venue_id"])
    return venues


def get_info_for_venue(venue):
    url = "https://api.songkick.com/api/3.0/venues/{!s}.json?apikey=Kg38ZlH0nSOBf8rA".format(venue)
    res = requests.get(url).json()["resultsPage"]
    try:
        if res["status"] == "ok":
            return parse_venue(res["results"])
        else:
            print("res encountered error for {!s}".format(venue))
            print(res)
            return []
    except KeyError as e:
        print(str(res["results"])+" - "+str(e)+" for "+str(venue))


def parse_venue(venue):
    venue_obj = dict({})
    venue_obj["id"] = venue["venue"]["id"]
    venue_obj["name"] = venue["venue"]["displayName"]
    venue_obj["lat"] = venue["venue"]["lat"]
    venue_obj["lon"] = venue["venue"]["lng"]
    venue_obj["address"] = venue["venue"]["street"]
    venue_obj["city"] = venue["venue"]["city"]["displayName"]
    venue_obj["city_id"] = venue["venue"]["metroArea"]["id"]
    venue_obj["country"] = venue["venue"]["city"]["country"]["displayName"]
    venue_obj["site"] = venue["venue"]["website"]
    venue_obj["capacity"] = venue["venue"]["capacity"]
    venue_obj["contact_at"] = '"'+str(venue["venue"]["phone"])+'"'
    venue_obj["description"] = venue["venue"]["description"]
    return venue_obj


def from_venue_list(venues):
    all_venues = []
    t1 = time.time()
    for venue in venues:
        try:
            info = get_info_for_venue(venue)
            if info != []:
                all_venues.append(info)
            sleep(0.7)
        except KeyError:
            print(str(venue)+" encountered error.")
            continue
    t2 = time.time()
    print("Took {!s} seconds".format(t2-t1))
    return all_venues