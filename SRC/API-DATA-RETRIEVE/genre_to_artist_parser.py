import csv
import ast


def read_row(row):
    to_add = []
    to_dict = dict({})
    band_id = row["artist_id"]
    genres = ast.literal_eval(row["genres"])
    for genre in genres:
        curr_dict = to_dict.copy()
        curr_dict["artist_id"] = band_id
        curr_dict["genre"] = genre
        to_add.append(curr_dict)
    return to_add


def make_things_organized():
    all_excel = []
    with open(r"C:\Users\Itamar\Desktop\base_proj\artistGenres_to_edit.csv", "r") as raw:
        reader = csv.DictReader(raw)
        for row in reader:
            curr_list= read_row(row)
            all_excel.extend(curr_list)
    raw.close()
    return all_excel


def count_words(txt):
    words = txt.split(" ")
    n = len(words)
    return n


def avg(lst):
    n = len(lst)
    total = sum(lst)
    return (total/n)


def desc_len():
    cnt = 0
    lens = []
    with open(r"C:\Users\Itamar\Desktop\base_proj\band_and_description.csv", "r") as raw:
        reader = csv.DictReader(raw)
        for row in reader:
            lens.append(count_words(row["desc"]))
            if (count_words(row["desc"]) >= 15):
                cnt += 1
    raw.close()
    print(avg(lens))
    print(cnt)


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
