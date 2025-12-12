import random
from datetime import date

import requests
from flask import Flask, render_template, request, g, redirect, url_for
import json

from flask_frozen import Freezer

app = Flask(__name__, static_folder="static")
freezer = Freezer(app)

app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'


def load_from_json(filename):
    with open(f'static/api/{filename}.json', encoding="utf8") as file:
        return json.load(file)


@app.before_request
def before_request():
    g.site_title = "Tome of the Vastlands"
    g.version_number = "4.0.0"

    g.ingame_date = load_from_json("current_date")["current_ingame_date"]
    g.lore_days = ["Lunesdag", "Flamdag", "Quellsdag", "Waldsdag", "Goldag", "Terrasdag", "Sunnesdag"]
    g.lore_months = ["Eismond", "Frostmond", "Saatmond", "Blütenmond", "Wonnemond", "Heumond", "Sonnenmond",
                     "Erntemond", "Fruchtmond", "Weinmond", "Nebelmond", "Julmond"]

    g.static = "/static/"
    g.debug = app.debug

    g.categories = {
        "Charaktere": "characters",
        "Kompendien": "compendia",
        "Orte": "places",
        "Tierlist": "tierlist"
    }

    apex_domain = "zetsuboushii.site/"
    image_subdomain = "https://images."
    g.img_host = image_subdomain + apex_domain + "dnd/"
    g.img_host_resized = image_subdomain + apex_domain + "resized/dnd/"
    g.current_date = date.today()
    g.random_banner = f'ui/banner-{random.randint(1, 3)}.png'


def find_place_recursively(place_list, place_slug, parent_name=None):
    for place in place_list:
        if place['name'].lower().replace(" ", "-") == place_slug:
            return place, parent_name

        if "contains" in place and isinstance(place["contains"], list):
            found, parent = find_place_recursively(place["contains"], place_slug, place["name"])
            if found is not None:
                return found, parent

    return None, None


def check_alt_image_exists(name: str, timeout: float = 5.0) -> dict:
    base_url = f"{g.img_host}characters/{name} alt"
    extensions = ["png", "jpg"]

    for ext in extensions:
        url = f"{base_url}.{ext}"
        try:
            response = requests.head(url, timeout=timeout, allow_redirects=True)
            if response.status_code == 200:
                return {
                    "alt_exists": True,
                    "url": url,
                    "status_code": response.status_code,
                }
        except requests.RequestException:
            pass

    return {
        "alt_exists": False,
        "url": None,
        "status_code": None,
    }


journal = load_from_json("journal")
enemy_list = load_from_json("bestiarium")
actions_list = load_from_json("actions")
places_list = load_from_json("places")
abilities_list = load_from_json("abilities")


@app.route('/')
def index():
    characters_list = load_from_json("npcs")
    characters_list[:] = [c for c in characters_list if "," not in c["name"] and "[hidden]" not in c["name"]]
    characters_list.sort(key=lambda character: character["name"].lower().replace(" & ", ""))
    calendar_list = load_from_json("calendar")
    current_day = g.current_date

    birthday_characters = []
    for char in characters_list:
        data = char.copy()

        if data.get('birthday') != "":
            birthday_day, birthday_month = 0, 0
            if len(data["birthday"].split(".")) == 2:
                birthday_day, birthday_month = map(int, data['birthday'].split('.'))
            if f"{birthday_day:02}" == f"{current_day.day:02}" and f"{birthday_month:02}" == f"{current_day.month:02}":
                birthday_characters.append(data)

    rand_char = random.choice(characters_list)

    return render_template('index.html', birthday_characters=birthday_characters, journal=journal, rand_char=rand_char,
                           holidays=calendar_list, characters=characters_list, current_day=current_day)


@app.route('/characters/')
def characters():
    characters_list = load_from_json("npcs")
    characters_list[:] = [c for c in characters_list if "," not in c["name"] and "[hidden]" not in c["name"]]
    characters_list.sort(key=lambda character: character["name"].lower().replace(" & ", ""))

    letters = sorted({character['name'][0].upper() for character in characters_list})
    nationalities = sorted({character['nationality'] for character in characters_list if "nationality" in character})

    def is_complete(entry):
        for value in entry.values():
            if isinstance(value, str) and not value.strip():
                return False
            if isinstance(value, (list, dict)) and not value:
                return False
        return True

    return render_template('characters.html', characters=characters_list, letters=letters, nationalities=nationalities,
                           is_complete=is_complete)


@app.route('/characters/<character_name>/')
def character(character_name):
    characters_list = load_from_json("npcs")
    characters_list[:] = [c for c in characters_list if "," not in c["name"] and "[hidden]" not in c["name"]]
    characters_list.sort(key=lambda character: character["name"].lower().split(",")[0])
    character = None

    character_name = character_name.lower().replace(" ", "-")

    for char in characters_list:
        char_name = char['name'].lower().replace(" ", "-")
        if char_name == character_name:
            character = char.copy()

            if character['birthday']:
                birthday_d, birthday_m, _ = character['birthday'].split('.')
                birthday_string = f"{birthday_d}. Tag des {g.lore_months[int(birthday_m) - 1]}"
                character['birthday'] = birthday_string

            if check_alt_image_exists(char_name):
                character['has_alt'] = True
            break

    if character is None:
        return redirect('/')
    return render_template('character.html', character=character)


@app.route('/places/')
def places():
    return render_template('places.html', places=places_list)


@app.route('/places/<place_name>/')
def place(place_name):
    place_data, parent = find_place_recursively(places_list, place_name)

    return render_template('place.html', place=place_data, parent=parent)


@app.route('/edit/places/<place_name>/', methods=['POST'])
def edit_place(place_name):
    if app.debug:
        place_data, _ = find_place_recursively(places_list, place_name)

        if request.method == "POST":
            return


@app.route('/compendium/')
def compendia():
    compendium_list = load_from_json("compendia")
    compendium_list.sort(key=lambda compendium: compendium["name"])

    return render_template('compendia.html', compendium_list=compendium_list)


@app.route('/compendium/<compendium_name>/')
def compendium(compendium_name):
    compendium_list = load_from_json("compendia")
    compendium_data = None

    for compendium in compendium_list:
        if compendium['name'].lower() == compendium_name.lower():
            compendium_data = load_from_json(compendium['name'].lower())
            break

    if compendium_name == "gentarium":
        characters_list = load_from_json("characters")
        for race in compendium_data:
            for character in characters_list:
                if character["race"] == race["name"]:
                    race["example"] = character["name"]
    elif compendium_name in ["gladiarium", "antiquarium"]:
        types = []
        for entry in compendium_data:
            types.append(entry['type'])
        types = list(set(types))
        return render_template('compendium.html', compendium_name=compendium_name, compendium=compendium_data,
                               types=types)
    elif compendium_name == "magickarium":
        compendium_list.sort(key=lambda compendium: compendium["name"])
        types = []
        associations = []
        for entry in compendium_data:
            types.append(entry['type'])
            associations.append(entry['association'])
        types = list(set(types))
        associations = list(set(associations))
        return render_template('compendium.html', compendium_name=compendium_name, compendium=compendium_data,
                               types=types, associations=associations)

    return render_template('compendium.html', compendium_name=compendium_name, compendium=compendium_data)


@app.route('/compendium/<compendium_name>/<entry_name>/')
def compendium_entry(compendium_name, entry_name):
    entry = None

    for entry_json in load_from_json(compendium_name):
        temp_name = entry_json['name'].lower()
        temp_name = temp_name.replace(" ", "-")
        if temp_name == entry_name:
            entry = entry_json

    match compendium_name:
        case "theologarium":
            return render_template('theologarium.html', entry=entry)
        case "gentarium":
            characters_list = load_from_json("characters")
            for character in characters_list:
                if character["race"] == entry_name.capitalize():
                    entry["example"] = character["name"]
            return render_template('gentarium.html', entry=entry)
        case "linguarium":
            return render_template('linguarium.html', entry=entry)
        case "bestiarium":
            actions = []
            for enemy_action in entry["actions"]:
                for action in actions_list:
                    if action["name"] == enemy_action:
                        actions.append(action)
            return render_template('bestiarium.html', enemy=entry, actions=actions)
        case "classarium":
            return render_template('classarium.html')
        case "herbarium":
            return render_template('herbarium.html')
        case "gladiarium":
            abilities = []
            for weapon_ability in entry["abilities"]:
                for ability in abilities_list:
                    if ability['name'] == weapon_ability:
                        abilities.append(ability)
            return render_template('gladiarium.html', weapon=entry, abilities=abilities)
        case "magickarium":
            return render_template('magickarium.html', spell=entry)
        case "antiquarium":
            return render_template('antiquarium.html', item=entry)


@app.route('/holidays/<holiday_name>/')
def holidays(holiday_name):
    calendar_list = load_from_json("calendar")

    entry = None

    for entry_json in calendar_list:
        if entry_json['name'].lower().replace(" ", "-") == holiday_name.lower().replace(" ", "-"):
            entry = entry_json

    return render_template('holidays.html', entry=entry)


@app.route('/tierlist/')
def tierlist():
    characters_list = load_from_json("npcs")
    characters_list[:] = [c for c in characters_list if "," not in c["name"] and "[hidden]" not in c["name"]]
    characters_list.sort(key=lambda character: character["name"].lower().replace(" & ", ""))

    return render_template('tierlist.html', characters=characters_list)


@app.route('/timeline/')
def timeline():
    EPOCH_OFFSETS = {
        "vor langer Zeit": -9999999,
        "vor Vereinigung": -4000,
        "nach Vereinigung": 0
    }

    events = load_from_json("timeline")

    def parse_event_date(event):
        epoch = event["epoch"]
        offset = EPOCH_OFFSETS.get(epoch, 0)

        if "date" not in event or not event["date"]:
            return (offset, 0, 0)

        day_str, month_str, year_str = event["date"].split(".")
        day = int(day_str)
        month = int(month_str)
        year = int(year_str)
        sort_year = offset + year

        return (sort_year, month, day)

    events.sort(key=parse_event_date)

    return render_template("timeline.html", events=events)


if __name__ == '__main__':
    app.run(debug=True)
