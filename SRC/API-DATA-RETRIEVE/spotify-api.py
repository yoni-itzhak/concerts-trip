import base64
import json
import requests
import csv
import time
import os.path

# Spotify
myid = '1de47303577a4fc5811e437f6277daee'
mysec = 'd1d8c369dbe94a46be21a0efdf0c4ccd'
csvPath = r"C:\Users\Sagi\PycharmProjects\csvResults\{!s}.csv"


# input: String 'client_id', String 'client_secret'
# output: String 'authorization'
def get_bearer_token(client_id, client_secret):
    basic = "Basic " + base64.b64encode((client_id + ":" + client_secret).encode()).decode()
    header = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': basic}
    params = {'grant_type': 'client_credentials'}
    received_request = requests.post('https://accounts.spotify.com/api/token', headers=header, params=params)
    json_dict = received_request.json()
    token = json_dict["access_token"]
    bearer = "Bearer " + token
    return bearer


# input: json 'artist', String 'searched_name'
# output: 'artist' dictionary
def parse_artist_search(artist, searched_name):
    url = "None"
    width = 0
    height = 0
    all_necessary = dict({})

    all_necessary["Spotify ID"] = artist["id"]
    all_necessary["name"] = artist["name"]
    all_necessary["followers"] = artist["followers"]["total"]
    all_necessary["genres"] = artist["genres"]
    all_necessary["popularity"] = artist["popularity"]
    try:
        unparsed = artist["images"][0]
        url = unparsed["url"]
        height = unparsed["height"]
        width = unparsed["width"]
        all_necessary["image_url"] = url
        all_necessary["height"] = height
        all_necessary["width"] = width
    except IndexError:
        all_necessary["image_url"] = url
        all_necessary["height"] = height
        all_necessary["width"] = width
    finally:
        all_necessary["search_name"] = searched_name
    return all_necessary


# search artists by name, return as list of jsons - each includes details about an artist
# input: String 'artist_name', int 'limit'
# output: list of 'artist' dictionaries
def artist_search_api(artist_name, limit):
    url = "https://api.spotify.com/v1/search?q=" + artist_name + "&type=artist&offset=0&limit=" + limit
    bearer = get_bearer_token(myid, mysec)
    header2 = {'Authorization': bearer}
    response = requests.get(url, headers=header2)
    if response.status_code == 200:
        res_dict = response.json()["artists"]["items"]
        dict_list = []
        for artist in res_dict:
            curr = parse_artist_search(artist, artist_name)
            iterate_over_dict(curr)
            dict_list.append(curr)
        return dict_list
    elif response.status_code == 429:
        print ("We got a rate limit\n")
        time.sleep(900)
        artist_search_api(artist_name, limit)
    else:
        print("Failed due to response status code is: " + response.status_code)


# prints a dictionary
def iterate_over_dict(dict):
    for i in dict:
        print(str(i) + ": " + str(dict[i]))
    print("\n")


# input: list of dictionaries 'artists_list', String 'filename'
# output csv file with data
def write_output_to_csv(artists_list, filename):
    file = csvPath.format(filename)
    file_exists = os.path.isfile(file)

    with open(file, "a", newline="") as curr:
        curr_csv = csv.DictWriter(curr, fieldnames=artists_list[0].keys())

        if not file_exists:
            curr_csv.writeheader()

        for artist in artists_list:
            try:
                curr_csv.writerow(artist)
            except UnicodeError:
                continue


# read all artists from the existing bands.csv
# input String 'filename'
# output list of Strings 'artists'
def retrieve_all_artists(filename):
    artists = []
    with open(csvPath.format(filename), encoding="ISO-8859-1") as file:
        csv_read = csv.DictReader(file)
        for row in csv_read:
            artists.append(row['Band Name'].translate({ord(i): None for i in '!@#$%^&*()~_+-={}[]|`,./;"'}))
    file.close()
    return artists

# go over a list of strings with artists names, trigger the API call and store the results in a csv file
def iterate_through_artists(artists_list):
    bands_limit = "3"
    artists_final = []
    for band in artists_list:
        returned_list = artist_search_api(band, bands_limit)
        if (returned_list != []):  # result is not empty
            write_output_to_csv(returned_list, "artists_process")  # write directly to file per result
            for result in returned_list:
                artists_final.append(result)

        # time.sleep(0.5)
    return artists_final


# bands = retrieve_all_artists("bands")
# final = iterate_through_artists(bands)
# write_output_to_csv(final, "artists_final")
