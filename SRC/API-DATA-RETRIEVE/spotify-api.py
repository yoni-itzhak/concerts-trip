import requests
import base64
import re
import csv

myid = 'ecff86f0a66c4414bd946e80bf40624f'
mysec = '4b4538e271bf49c486afb4f3e973227e'


def get_bearer_token(client_id, client_secret):
    basic = "Basic "+base64.b64encode((client_id+":"+client_secret).encode()).decode()
    header = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': basic}
    params = {'grant_type': 'client_credentials'}
    received_request = requests.post('https://accounts.spotify.com/api/token', headers=header, params=params)
    json_dict = received_request.json()
    token = json_dict["access_token"]
    bearer = "Bearer "+token
    return bearer


def search_func_spotify(query, elem_type, kwargs=None):
    url = 'https://api.spotify.com/v1/search'
    bearer = get_bearer_token(myid, mysec)
    header2 = {'Authorization': bearer}
    query = {'q':query,'type': elem_type}
    if (kwargs != None):
        print("It's not none!")
        query.update(kwargs)
    response = requests.get(url, headers=header2, params=query)
    print(response.url)
    res_dict = response.json()
    #print(res_dict)
    return res_dict[elem_type+"s"]['items']


def search_raw(url, elem):
    bearer = get_bearer_token(myid, mysec)
    header2 = {'Authorization': bearer}
    response = requests.get(url, headers=header2)
    #print(response.content)
    print(response.url)
    res_dict = response.json()
    print(res_dict[elem+'s'].keys())
    print("next: "+str(res_dict[elem+'s']["next"]))
    print("offset: "+str(res_dict[elem+'s']["offset"]))
    print("total: "+str(res_dict[elem+'s']["total"]))
    return res_dict[elem+"s"]['items']


def iterate_over_dict(json_dict):
    for i in json_dict:
        if (type(json_dict[i]) == list):
            print(i+":")
            for j in json_dict[i]:
                print("\t"+str(j))
        else:
            print(str(i)+": "+str(json_dict[i]))


def parse_artist(artist_elem, found_from):
    url = "None"
    width = 0
    height = 0
    all_necessary = dict({})
    all_necessary["name"] = artist_elem["name"]
    all_necessary["Spotify ID:"] = artist_elem["id"]
    all_necessary["follow_num"] = artist_elem["followers"]["total"]
    all_necessary["genres"] = artist_elem["genres"]
    all_necessary["popularity"] = artist_elem["popularity"]
    try:
        unparsed = artist_elem["images"][0]
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
        all_necessary["main_genre"]=found_from
    return all_necessary


def parse_playlist(playlist_elem):
    elem = dict({})
    elem["name"] = playlist_elem["name"]
    elem["description"] = playlist_elem["description"]
    elem["id"] = playlist_elem["id"]
    elem["num_tracks"] = playlist_elem["tracks"]["total"]
    return elem


def modify_params(query):
    retstr = ""
    for i in query:
        restr += "%20" + i+":%22"+query[i]
    return retstr


"""
search = search_func_spotify("Alice in Chains", "artist", {"genre":"grunge"})
print(search)
artist = parse_artist(search[0])
iterate_over_dict(artist)

search = search_func_spotify("a*", "artist", "asdfasdf")
for i in search:
    curr = parse_artist(i)
    for j in curr:
        print(j+": "+str(curr[j]))
    print("")
"""


def get_offset(next_url):
    regex = re.compile("offset=(\d+)")
    res = regex.findall(next_url)[0]
    return int(res)


def genre_search_api(genre, limit):
    url = "https://api.spotify.com/v1/search?q=genre:{!s}&type=artist".format(genre)
    bearer = get_bearer_token(myid, mysec)
    header2 = {'Authorization': bearer}
    response = requests.get(url, headers=header2)
    res_dict = response.json()["artists"]["items"]
    print(response.json()["artists"].keys())
    dict_list = []
    offset = 0;
    while (offset < limit):
        next_one = response.json()["artists"]["next"]
        for artist in res_dict:
            curr = parse_artist(artist, genre)
            dict_list.append(curr)
        #print("Moving to {!s}".format(next_one))
        response = requests.get(next_one, headers=header2)
        res_dict = response.json()["artists"]["items"]
        offset = get_offset(next_one)
    return dict_list

def write_dictlist_to_csv(csv_name, dict_list):
    path = "C:\\Users\\Itamar\\Desktop\\base_proj\\{!s}.csv"
    full_path = path.format(csv_name)
    headers = dict_list[0].keys()
    with open(full_path, "w", newline='') as xl:
        writer = csv.DictWriter(xl, fieldnames=headers)
        writer.writeheader()
        for res in dict_list:
            try:
                writer.writerow(res)
            except UnicodeEncodeError:
                continue
    xl.close()


"""
search = search_raw("https://api.spotify.com/v1/search?q=genre:rock&type=artist", "artist")
for i in search:
    curr = parse_artist(i)
    for j in curr:
        print(j+": "+str(curr[j]))
    print("")
"""
