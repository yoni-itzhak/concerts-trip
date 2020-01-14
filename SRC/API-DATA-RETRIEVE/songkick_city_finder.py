import requests
import csv


url = "https://api.songkick.com/api/3.0/search/locations.json?query={!s}&apikey={!s}"
key = "Kg38ZlH0nSOBf8rA"

def city_to_dict(city_json):
    city_dict = dict({})
    #print(1)
    city_dict['Country'] = city_json['city']['country']['displayName']
    #print(2)
    city_dict['City'] = city_json['city']['displayName']
    city_dict['lat'] = city_json['city']['lat']
    city_dict['lon'] = city_json['city']['lng']
    city_dict['id'] = city_json['metroArea']['id']
    #print("Dayumn")
    return city_dict

def country_to_dict(curr_country):
    country_list = []
    for i in range(20):
        try:
            country_list.append(city_to_dict(curr_country[i]))
        except IndexError:
            continue
    return country_list


def find_capitals_by_list(capital_list):
    csv_list = []
    for city in capital_list:
        res = requests.get(url.format(city, key)).json()
        try:
            curr_country = res['resultsPage']['results']['location']
            #print(curr_city)
            curr_dict = country_to_dict(curr_country)
            csv_list.extend(curr_dict)
        except KeyError:
            continue
    #print(csv_list)
    return csv_list

def find_countries_not_us(capital_list):
    csv_list = []
    for city in capital_list:
        res = requests.get(url.format(city, key)).json()
        try:
            #print("Searching for {!s}".format(city))
            curr_country = res['resultsPage']['results']['location']
            curr_dict = get_cities_not_us(curr_country)
            csv_list.extend(curr_dict)
        except KeyError:
            continue
    #print(csv_list)
    return csv_list


def write_cities_to_csv(name, cities_list):
    with open(r"C:\Users\Itamar\Desktop\base_proj\{!s}.csv".format(name), "a", newline='') as curr:
        curr_csv = csv.DictWriter(curr, fieldnames=cities_list[0].keys())
        curr_csv.writeheader()
        for city in cities_list:
            try:
                curr_csv.writerow(city)
            except UnicodeError:
                continue

def get_cities_not_us(not_us):
    ret_list = []
    i = 0
    j = 0
    #print("AAA")
    #print(not_us[2])
    try: 
        while i < 5:
            #print(not_us[j])
            curr_country = not_us[j]['city']['country']['displayName']
            #print(curr_country)
            if (curr_country == 'US'):
                #print("ERROR HERE")
                #print("Found city {!s} in country {!s}...".format(not_us[j]['city']['displayName'],not_us[j]['city']['country']['displayName']))
                j += 1
                continue
            #print("NO HERE")
            #print("Not in us! {!s}".format(city_to_dict(not_us[j])))
            ret_list.append(city_to_dict(not_us[j]))
            i += 1
            j += 1
    except IndexError:
        return ret_lis
    finally:
        return ret_list
        


#ALL_CITIES = ["Yerevan","Vienna","Baku","Minsk","Brussels","Sarajevo","Sofia","Zagreb","Nicosia","Prague","Copenhagen","Tallinn","Helsinki","Paris","Tbilisi","Berlin","Athens","Budapest","Reykjavik","Dublin","Rome","Nur-Sultan","Pristina","Riga","Vaduz","Vilnius","Luxembourg","Valletta","Chisinau","Monaco","Podgorica","Amsterdam","Skopje","Oslo","Warsaw","Lisbon","Bucharest","Moscow","San Marino","Belgrade","Bratislava","Ljubljana","Madrid","Stockholm","Bern","Ankara","Kyiv","Kiev","London"]
COUNTRIES = ["Afghanistan","Albania","Algeria","Andorra","Angola","Antigua and Barbuda","Argentina","Armenia","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Brazil","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Central African Republic","Chad","Chile","China","Colombia","Comoros","Congo","Republic of Costa Rica","Côte d'Ivoire","Croatia","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","East Timor","Ecuador","Egypt","El Salvador","Guinea","Eritrea","Estonia","Ethiopia","Fiji","Finland","France","Gabon","Gambia","Georgia ","Germany","Ghana","Greece","Grenada","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Honduras","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kiribati","Korea"," North","Korea"," South","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nepal","Netherlands","New Zealand","Nicaragua","Nigeria","Northern Ireland","Norway","Oman","P","Pakistan","Palau","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Qatar","Romania","Russia","Rwanda","Eswatini","Samoa","San Marino","São Tomé and Príncipe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","Spain","Sri Lanka","St. Kitts and Nevis","St. Lucia","St. Vincent and the Grenadines","Sudan","Suriname","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Togo","Tonga","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan","Vanuatu","Vatican City","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"]
BAD_CUNT = ['Mexico', 'Panama', 'Canada', 'Cuba', 'Brazil', 'Jordan', 'Jamaica', 'Peru','Macedonia','Malta','Belgium','Greece','Poland','Denmark','Germany','Norway','Sweden']
#cities = find_capitals_by_list(ALL_CITIES)
#my_countries = find_capitals_by_list(COUNTRIES)
#write_cities_to_csv('countries', my_countries)
US = ['US']
all_not_us = find_capitals_by_list(US)
print(all_not_us)
write_cities_to_csv('countries', all_not_us)
