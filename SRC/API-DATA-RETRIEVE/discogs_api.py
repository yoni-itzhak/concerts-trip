import requests
import csv

token = 'LkPupZrwLVFxWCeTMdcezMkdBGtFhzrILNLFktwr'

url = "https://api.discogs.com/database/search"

headers = {'Authorization': 'Discogs token=LkPupZrwLVFxWCeTMdcezMkdBGtFhzrILNLFktwr'}


def get_content(page):
    search = requests.get(url+str(page), headers=headers)
    print(search.json()["pagination"])
    res = search.json()["results"]
    for elem in res:
        print(elem)
        print_artist(elem)

def get_results(artist):
    params = {"q": artist, "type": "artist"}
    search = requests.get(url, headers=headers, params=params)
    #print(search.url)
    return search.json()["results"]

def print_artist(json):
    print(json["title"]+", ID: "+str(json["id"]))

def parse_artist_discogs(artist_elem):
    to_dict = dict({})
    to_dict["name"] = artist_elem["title"]
    to_dict["id"] = artist_elem["id"]
    url_next = artist_elem["resource_url"]
    more_dict = get_artist_deeper_details(url_next)
    to_dict.update(more_dict)
    return to_dict

def retrieve_all_bands():
    bands = []
    with open(r"C:\Users\Itamar\Desktop\base_proj\bands.csv") as file:
        csv_read = csv.DictReader(file)
        for row in csv_read:
            #print(row['Band Name'])
            bands.append(row['Band Name'])
    file.close()
    return bands

def iterate_through_bands(band_list):
    bands_final = []
    for band in band_list:
        ret_dict = search_artist(band)
        if (ret_dict != dict({})):
            bands_final.append(ret_dict)
    return bands_final

def get_artist_deeper_details(url):
    mem_list = []
    deeper_details = dict({})
    res = requests.get(url, headers=headers).json()
    try:
        members = res["members"]
    except KeyError:
        members = []
    for member in members:
        if member["active"] == True:
            mem_list.append(member["name"])
    deeper_details["members"] = mem_list
    deeper_details["desc"] = res["profile"]
    return deeper_details

def write_to_csv(filename, dict_list):
    with open(r"C:\Users\Itamar\Desktop\base_proj\{!s}.csv".format(filename), "a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=dict_list[0].keys())
        writer.writeheader()
        for band in dict_list:
            try:
                writer.writerow(band)
            except UnicodeEncodeError:
                continue
        file.close()


def search_artist(artist_name):
    artist_search = artist_name.replace(" ", "%20")
    #print(artist_name)
    tmp = dict({})
    res = get_results(artist_name)
    for sub_res in res:
        #print(sub_res["title"])
        if sub_res["title"].lower() == artist_name.lower():
            #print("found.")
            tmp = parse_artist_discogs(sub_res)
    return tmp
