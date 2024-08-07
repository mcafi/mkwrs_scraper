from scraper import web_scraper
from firebase import add_data, set_game, set_track
from utilities import parse_lap_time, parse_time, console_list
import json

base_url = "https://mkwrs.com/mkds/"

record_list = []

def scrape_DS():
    soup = web_scraper(base_url)
    table_el = soup.find("table", class_ = "wr")

    insert_game_info()

    track_urls = []

    for row_el in table_el.select("tr")[1::4]:
        cell = row_el.find("td")
        link = cell.find("a")
        if (link != None):
            track_urls.append(link["href"])
        
    for url in track_urls:
        scrape_track_page(url)
        #scrape_track_page(url, non_sc = True)
        #scrape_track_page(url, non_prb = True)
        #scrape_flap_page(url)
        #scrape_flap_page(url, non_sc = True)
        #scrape_flap_page(url, non_prb = True)
    
    with open("data.json", "w") as file:
        json.dump(record_list, file)

def insert_game_info():
    game_info = {
        "title": "Mario Kart DS",
        "platform": "Nintendo DS",
        "release_date": "2005-11-14",
        "developer": "Nintendo EAD",
        "publisher": "Nintendo"
    }
    set_track(game_info, "mk_ds")


def scrape_track_page(url, non_sc = False, non_prb = False):
    track_url = base_url + url

    if (non_sc is True):
        track_url += "&m=2"
    
    if (non_prb is True):
        track_url += "&m=1"

    soup = web_scraper(track_url)

    main_el = soup.find("div", id = "main")
    circuit_name = main_el.find("h2").text

    record_history_el = main_el.findAll("table", class_ = "wr")[-1]

    track_name = "ds_" + circuit_name.lower().replace(" ", "_")

    print(circuit_name + (" (Non SC)" if non_sc else "") + (" (Non PRB)" if non_prb else ""))

    retro_console = circuit_name.split(" ")[0]
    is_retro = retro_console.lower() in console_list

    if is_retro:
        circuit_name = circuit_name[len(retro_console) + 1:]

    track_info = {
        "game": "mk_ds",
        "track": circuit_name,
        "retro": retro_console if is_retro else None,
    }

    set_track(track_info, track_name)

    for record_el in record_history_el.findAll("tr")[1:]:

        record = record_el.findAll("td")

        lap_count = len(record) - 7

        video_link_el = record[1].find("a")
        flag_el = record[3].find("img")

        record_item = {
            "game": "mk_ds",
            "track": track_name,
            "lap_count": lap_count,
            "date": record[0].text,
            "time": parse_time(record[1].text),
            "video_link": video_link_el["href"] if video_link_el else None,
            "non_sc": non_sc,
            "non_prb": non_prb,
            "player": record[2].text,
            "nation": flag_el["title"] if flag_el else None,
            "character": record[8].text if record[8].text != "-" else None,
            "vehicle": record[9].text if record[9].text != "-" else None,
            "laps": []
        }

        for i in range(lap_count):
            record_item["laps"].append(parse_lap_time(record[5+i].text))

        #print(record_item)
        record_list.append(record_item)
        #add_data(record_item, "mk_ds")

def scrape_flap_page(url, non_sc = False, non_prb = False):
    track_url = base_url + url + "&f=1"

    if (non_sc is True):
        track_url += "&m=2"
    
    if (non_prb is True):
        track_url += "&m=1"

    soup = web_scraper(track_url)

    main_el = soup.find("div", id = "main")
    circuit_name = main_el.find("h2").text

    record_history_el = main_el.findAll("table", class_ = "wr")[-1]
    print(circuit_name + " Flap" + (" (Non SC)" if non_sc else "") + (" (Non PRB)" if non_prb else ""))

    for record_el in record_history_el.findAll("tr")[1:]:

        record = record_el.findAll("td")

        video_link_el = record[1].find("a")
        flag_el = record[3].find("img")

        record_item = {
            "game": "mk_ds",
            "track": circuit_name,
            "date": record[0].text,
            "lap_time": parse_time(record[1].text),
            "video_link": video_link_el["href"] if video_link_el else None,
            "non_sc": non_sc,
            "non_prb": non_prb,
            "player": record[2].text,
            "nation": flag_el["title"] if flag_el else None,
            "character": record[5].text if record[6].text != "-" else None,
            "vehicle": record[5].text if record[6].text != "-" else None,
        }

        #add_data(record, "mk_ds", "flap")
        record_list.append(record_item)
        #print(record_item)
        