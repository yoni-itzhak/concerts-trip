import requests
import csv
import ast
import datetime
import time
from time import sleep


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
    if "message" in search.json():
        print("ahhh")
        print(search.json())
        exit()
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
            bands.append(row['Band Name'])
    file.close()
    return bands


def once_in_a_while_update(band_list):
    segments = len(band_list)/100
    start = 0
    now = datetime.datetime.now()
    print("started at {!s}:{!s}:{!s}".format(now.hour, now.minute, now.second))
    for segment in range(int(segments)):
        print("Commenced!")
        t1 = time.time()
        print("Going through {!s} to {!s}".format(100*segment, 100*(segment+1)))
        received = iterate_through_bands(band_list[100*segment:(100*(segment+1))])
        write_to_csv("members", received)
        t2 = time.time()
        print("Written! Took {!s} seconds".format(str(t2-t1)))
        sleep(3)


def iterate_through_bands(band_list):
    bands_final = []
    t1 = time.time()
    for band in band_list:
        try:
            ret_dict = search_artist(band)
            if (ret_dict != dict({})):
                bands_final.append(ret_dict)
        except KeyError as e:
            print("Error! {!s}".format(e))
            continue
    t2 = time.time()
    print(t2-t1)
    return bands_final


def get_artist_deeper_details(url):
    mem_list = []
    deeper_details = dict({})
    res1 = requests.get(url, headers=headers)
    #print(res1)
    try:
        res = res1.json()
        try:
            members = res["members"]
        except KeyError:
            members = []
        for member in members:
            if member["active"] == True:
                mem_list.append((member["name"],member["id"]))
        deeper_details["members"] = mem_list
        try:
            deeper_details["desc"] = res["profile"]
        except KeyError:
            deeper_details["desc"] = ""
        return deeper_details
    except json.decoder.JSONDecodeError:
        print(res.content)
        exit()


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
    tmp = dict({})
    res = get_results(artist_name)
    for sub_res in res:
        if type(sub_res) is dict:
            if sub_res["title"].lower() == artist_name.lower():
                tmp = parse_artist_discogs(sub_res)
                break
    sleep(0.3)
    return tmp


def get_players_for_band(row):
    player_row = dict({})
    ret_players = []
    member_tuple_list = ast.literal_eval(row["members"])
    for member in member_tuple_list:
        iter_dict = player_row.copy()
        iter_dict["band"] = row["name"]
        iter_dict["band_id"] = row["id"]
        iter_dict["member"] = member[0]
        iter_dict["member_id"] = member[1]
        ret_players.append(iter_dict)
    return ret_players
        

def create_player_table(file1):
    path = r"C:\Users\Itamar\Desktop\base_proj\{!s}.csv"
    path1 = path.format(file1)
    all_players = []
    with open(path1, "r") as f1:
        f1_reader = csv.DictReader(f1)
        for row in f1_reader:
            if row["members"] != "[]":
                try:
                    all_players.extend(get_players_for_band(row))
                except ValueError:
                    continue
    return all_players


def create_description_table(file1):
    path = r"C:\Users\Itamar\Desktop\base_proj\{!s}.csv"
    path1 = path.format(file1)
    all_desc = []
    with open(path1, "r") as f1:
        f1_reader = csv.DictReader(f1)
        for row in f1_reader:
            if row["desc"] != "":
                row["desc"] = row["desc"].replace("[a=","").replace("]","").replace("[b][i]","").replace("[/i][/b]","").replace("[a","")
                all_desc.append(row)
    return all_desc


def write_to_player_table(file2, lst):
    path = r"C:\Users\Itamar\Desktop\base_proj\{!s}.csv"
    path2 = path.format(file2)
    with open(path2, "a", newline='') as f2:
        f2_writer = csv.DictWriter(f2, fieldnames=lst[0].keys())
        f2_writer.writeheader()
        for row in lst:
            try:
                f2_writer.writerow(row)
            except UnicodeEncodeError:
                continue
