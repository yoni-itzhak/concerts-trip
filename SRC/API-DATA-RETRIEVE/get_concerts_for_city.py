import requests
import csv

key = 'Kg38ZlH0nSOBf8rA'


def songkick_get_city(city, min_date, page):
    url = "https://api.songkick.com/api/3.0/metro_areas/{!s}/calendar.json"
    full_url = url.format(city)
    params = {"min_date": min_date, "apikey": key, "page": page}
    res_raw = requests.get(full_url, params=params)
    #print(res_raw.url)
    #print(res_raw)
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
    out_dict = dict({})
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
    i = 10;
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
            #print(band)
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

# def parse_event_details(


# def songkick_get_event(event_id):
#     raw_url = "https://api.songkick.com/api/3.0/events/{!s}.json?apikey={!s}"
#     url = raw_url.format(event_id, key)
#     res = requests.get(url).json()["resultsPage"]["results"]["event"]
    


#res = songkick_get_city("31802", "2020-01-01")
#output = add_event_to_list(res)
#write_output_to_csv(output, "lisbon_shows")


#for i in output:
#    print("")
#    for j in i:
#        print(str(j)+": "+str(i[j]))
        
