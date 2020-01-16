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
        # print("\npossible keys are: ")
        # print(res_dict[0].keys())
        # print("\n")
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


# write_output_to_csv(iterate_through_artists(retrieve_all_artists()), "artists.csv")

# artist_search_api("Infected")

# artists = retrieve_all_artists("bands")
# list_of_dicts = [
# {"name": "Tom", "age": 10},
# {"name": "Mark", "age": 5},
# {"name": "Pam", "age": 7}
# ]
# time.sleep(5)
# print(artists)
# time.sleep(5)
# print(list_of_dicts)

# write_output_to_csv(list_of_dicts, "artists")
# write_output_to_csv(list_of_dicts, "artists")


# def build_artists_table():
#
#     for band in bands:
#         iterate_through_artists(band)

print("\n")
# lst = ["Tierra", "THROWDOWN (US)", "DIVES (@divesband)", "C.W. Stoneking", "Roanoke (US)", "The Kings of Rnb", "Jhen? Aiko", "Big Lo", "Mace (AT)", "Matthias Hoefs", "Petros Klampanis Trio", "The Scott Henderson Trio", "il:lo", "Pizzera & Jaus", "Vitaa & Slimane", "Yipee!", "Psuedo Echo", "The Music of Cream", "Zusatzshow", "Gabriel Bismut", "Loewe", "churrosconchoco", "Jake Pinto", "Gnawbox", "Arlt.", "Rodrigue", "Radio 3", "A Spectacular Night of Queen", "Mariachi Reyna de Los ?ngeles", "M?sl?m", "Wild Child a Jim Morrison Celebration", "Larry", "Andr? Rieu", "Taylor Perry", "Michael Wolff Trio", "Wayne Marshall (UK)", "YATTA (Sierra Leone)", "Jaguar Jaguar", "Tyler-james Kelly", "Shantel & Bucovina Club Orkestar", "Le?n Benavente", "Bone Church (CT)", "capitals mx", "Pool", "The Cavern Beatles", "The Dreamboats (CAN)", "Fabian 2.0", "Christophe", "Jen Hartswick", "Gurschach", "Black Veil Bridges", "Molly", "K", "Diogo Pi?arra", "Automatic (band)", "?stkyst Hustlers", "Maxi Jazz (Faithless)", "Queen Live 86", "Bark", "La Revolucion De Emilio Zapata", "JUNE (AUS)", "Mathea Official", "suna (JP)", "Ra?na Ra?", "Baylee Barrett", "PROM", "Jasper", "Camille & Julie Berthollet", "Dave Blight", "Donore", "SCURA", "Bait (Barcelona)", "Mal ?lev?", "Bandit", "Deville (SWE)", "FortSumter", "Jessie's Girl", "Dares (US)", "Rudy P?rez", "Kieran Kane & Rayna Gellert", "Thomas and the Work-Men", "SWIMS (CH)", "Red", "buzzed lightbeer", "Obat Batuk", "Victor Julien-Laferriere", "La terza via - Album presentation", "Nick Mason’s Saucerful Of Secrets", "La Adictiva Banda San Jose De Mesillas", "Matt Ferranti", "Steal Your Peach Band", "V?ster?s Sinfonietta", "Paulabulus", "Space", "Pigs: Canada's Pink Floyd Tribute", "Dead Root Revival", "Into-Orleans", "Bob Seger & The Silver Bullet Band", "MiA.Berlin", "Pia Davila", "Sol'e (LJR)", "Midnight", "FM", "The Container", "C.l. Smooth", "Anti-Pop Consortium", "F?llakzoid", "Ballak? Sissoko", "Soul Sacrifice - The Music of Santana", "Morbid", "Earl Brothers", "TOYBLO?D", "Afro-latin Jazz Orchestra", "Michael Wheeler Blues Band", "The Wet Ones! (VT)", "Melt The Band (NYC)", "Ga?tan (Chansons pour les marmots)", "Benny Holst Trio", "Mike Nash & Southern Drawl Band", "Tom L?neburger", "Bumper Jacksons Duo", "Magnus (Singer/Songwriter)", "Jody", "Hive Mind (US)", "Montreal", "Alice", "Brubecks Play Brubeck", "Ten?re4you", "Leandro Andrea", "Pablo Heras-Casado", "Granrojo", "Corner Caf? Chronicles", "Made in the 90's", "Compagnia del Madrigale", "De Maria", "Cirque FLIP Fabrique", "Aggramakabra", "Hr. Sk?g", "Cinzia Caffio", "Fantasy", "Violence", "Mato Seco e Planta e Raiz", "The Jacks (US)", "Gideon Tazelaar", "Lehtoj?rven Hirvenp??", "V0id b0ys", "Introducing Nashville", "Bach to Rock", "Jason Ajemian", "Garvan Shvarts", "The Music of Hans Zimmer", "Lakeshore (US)", "Portland Symphony Orchestra", "DJ Diesel (Shaquille O'Neal)", "N.T.O.", "The Exploding Boys (AU)", "DJ Richard Reich", "Mom Jeans", "HunkaJunk", "Ron Artis II & The Truth", "Les Fran?oises", "Eyaculacion Post Mortem", "The Flat Cats", "Chromb", "MARIA AGUADO", "L?poka", "Proper (UK)", "drab (Andrew Nault)", "Rokia Traor?", "Ivar Myrset Asheim", "Dune (DE)", "Wolf-e-Wolf", "DJ Three", "K-Paz de la Sierra", "Frameworks (UK)", "Till Br?nner", "Blood, Sweat and Tears", "Rico Breesh", "Youth Pride Chorus", "locutor99", "L?vestad", "Lila Ik?", "My Three Song Piss Rock EP", "Mytallica", "INZO (US)", "Whiskey Houston", "Satan", "Jeffrey James Gang", "Irena Tomain", "Jamie Saft's New Zion Trio", "Conor Macfinn", "amanie // illfated", "Jerry's Middle Finger", "David Aknin", "Eric Slim Zahl", "F?bio Jr.", "abend", "Thierry von der Warth", "Milk(Bcn)", "Taj Mahal Trio", "The Pimps of Joytime", "Dirk Bross?", "G?raldine Laurent", "New York Philharmonic String Quartet", "Lazy Eye (PHL)", "Eva", "Glaze (USA)", "Basstripper (BE)", "Wacken Metal Battle", "K-maro", "Romeo Elvis", "Brittany Cardinale", "tunic (CA)", "Geneva Camerata", "Dog Date", "Perfume Genius (USA)", "Takacs String Quartet", "Bootleg Beatles", "Jeremy Star", "Hyryder", "Lina_Ra?l Refree", "WALLACE HARTLEY EXPERIENCE", "Kubilay Kar?a", "Soon", "Billy Davis (AUS)", "Maria Dybbroe", "Da Silva", "Noa (Achinoam Nini)", "Holly", "Renee Fleming", "Women of the Choral Arts Chorus", "The Sentimentals (DK)", "Reik Vip", "Orchestra Gold", "Jimmy Kenny and the Pirate Beach Band", "Leslie Odom, Jr.", "HERF (ID)", "Flotsam and Jetsam", "Amber Valentine", "Donny Benet", "Main act : Morcheeba ; Open act : Daysy", "DEUTSCHE ASHRAM", "Orgel", "Mateusz Kowalski Classical Guitarist", "C.Shreve the Professor", "Blackwater (Ohio)", "Mariachi Vargas de Tecalitl?n", "B?nabar", "Cat Stevens", "Grenzen Los", "Scraplord", "Kelvin Sanches", "Schmidbauer & K?lberer", "Loic Lantoine", "Serpent", "Pierre Durand ROOTS 4tet", "Split Persona", "Chamber Music", "Back to the 70's", "Heap", "GA-20", "June’s Landing", "Lena", "Blue Antidote", "The Lioness (MN)", "Ben B?hmer", "Jackal Jyve", "The Knockout Kings", "Holmes", "Ron Bennington (Comedian)", "Ge Reinders", "Support Act (TBC)", "Yeti", "Dimash Kudaybergen", "Brothers Reed", "Jazzkafe I Glasshuset", "Karel", "S?s", "Matt Barber Experience", "Castillo", "Dead On", "La P'tite Fum?e", "The Bawdy", "Coro Encanto", "Nelson", "Mike Mass?", "Tove B?ygard", "Le?ther Strip", "Santtu-Matias Rouvali", "Munch", "Clyde Leland", "Serration (Michigan)", "Deja Vu - A Musical Retrospective of CSN&Y", "Fang", "Choral Arts Chamber Singers", "Markku Lepist?", "Scorpio", "It's Rock 'N Soul", "CARL", "U-God", "The Crackups", "DANA (CH)", "Murphy", "Moh Kouyate", "Plus Special Guests", "Pororo", "Silvina G?mez", "DJ Sosupersam", "FAYREWETHER", "Rafal Blechacz", "So Soon The Truth", "Steal The Rain", "Ideaali & JayWho?", "Benjam?n Amadeo", "PRMD", "Pyre", "Rent Party (Chicago)", "Rawdriguez", "J?rgen Tr?en", "Queen Nation", "Tusk", "La Original Banda El Limon", "Conjunto Brio Norteno", "Muda Mc", "Stress", "Vaughan Misener", "Mgla", "Jamie Tiller", "Niklas Stromstedt", "Tonu Kaljuste", "Brib?n", "Spider SK Tortoise", "Mood", "G-Space", "Voodoo", "T Chronic", "Replicant (NJ)", "Bobbing For Apples", "Boris", "Ferrulo (Spain)", "Unity: Amjad Ali Khan, Shostakovich", "The Iron Maidens", "sortilege", "Sojourner (NZ/SWE/IT)", "ilia (BE)", "Make War", "Detroit Cobras", "Next Step (ES)", "Kennedy Center Educational Outreach 2020", "Proletariat (US)", "Est?re", "Ayo", "MC Drivah (NL)", "Hoffman (BE)", "Sein", "Jeffrey", "James Morrison Quartet", "Notations", "Throne Of Iron", "The Mccartney Years", "Chlo? Lacan", "Hook", "Soiree Tzigane", "Ulf", "Wynonna & The Big Noise", "Cumbia", "Dust of Ruin", "Hua Li", "Cat Ridgeway & The Tourists", "Langer", "The Beattells", "Brit Floyd", "The Best of Woodstock", "Les Yeux D'La T?te", "Dixon", "Alivan Blu", "Moulin Rose", "Hot Tuna Electric", "Thomas Str?nen", "Mar?lia Mendon?a", "B?RA G?SLAD?TTIR", "Carbonfools", "Early James and the Latest", "Dogs in a Pile", "All Boy/All Girl", "ILLE$T", "DJ Zachariah Love", "?lise Caron", "Angela Coltri", "16 Again", "Resurrection", "Captives(UK)", "Hija de la Luna", "J?r?me Regard", "Festival Strings Lucerne", "Rip", "Blake", "Evangeline Gentle", "dj mike sincere", "Jos? Madero", "Jay & Silent Bob Reboot Roadshow", "Horseshoes and Hand Grenades", "Alexandra Str?liski", "Star", "R?n? Jacobs", "TVO (Philadelphia)", "sAuce", "All-Turn", "Inferno", "Binomio de Oro de Am?rica", "Pr?xima Parada", "Carlo Brunners Superl?ndlerkapelle", "Jukebox (France)", "E.M.I.L. (RO)", "Friend Zone", "Russian Renaissance", "S?tyr (Beatmaker)", "Hakon Aase", "Neal Black And The Healers", "P?terfy Bori & Love Band", "79.5", "Polaris (AUS)", "Sam Pace & the Gilded Grit", "Nick Cave and The Bad Seeds", "Mary-Elaine Jenkins", "Los Cumplea?os", "Loan", "Hielo", "Ingrid Bj?rnov", "Cedric Duchemann", "Das Mortal", "Kenny Flowers", "ILLEAGLES - Bay Area's Premier Eagles Tribute Band", "Susanna", "Ian Jorg", "Battalion Zoska", "Noel", "Note Noire Quartet", "The Links (USA)", "Ryoko Aoki", "Ken Lazee", "La Nuit Du Kompa", "L?nasa", "My little Mayhem", "Discobole", "Mike Salazar", "The Wedding Crashers (CH)", "I Liguriani", "The Globally Jaguars", "RHGCOVERS", "Arianna  Neikrug", "Ganger (DK)", "The Mike Dillon Band", "Houben & Son", "Michael Charles", "Yannick", "Vikingur Olafsson", "Philharmonie Baden-Baden", "Los Chikos Del Ma?z", "West-Eastern Divan Orchestra", "Banda Bostick", "Slippin Jimmy", "Jan Paul Grijpink", "DR?NN", "The Music Man", "Molly Sarle", "Monteverdi Choir", "DJ MADD?G", "Les Strychnine", "That Arena Rock Show", "Kamma & Masalo", "JD Allen sax", "Neighbor", "K?lan Mikla", "Yannick N?zet-S?guin", "La Maquinaria Norte?a", "Critical", "Ross Mathews", "Pneuma Quartet", "Shitxyz"]
# final = iterate_through_artists(lst)
# write_output_to_csv(final, "artists_final")

bands = retrieve_all_artists("bands")
final = iterate_through_artists(bands)
write_output_to_csv(final, "artists_final")
