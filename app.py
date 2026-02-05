import random
from collections import defaultdict
from datetime import date
import requests
from flask import Flask, render_template, request, g, redirect
import json

from flask_frozen import Freezer

app = Flask(__name__, static_folder="static")
freezer = Freezer(app)

app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'


def load_from_json(filename):
    with open(f'static/api/v2/{filename}.json', encoding="utf8") as file:
        return json.load(file)


@app.before_request
def before_request():
    g.site_title = "Tome of the Vastlands"
    g.version_number = "5.5.13"

    g.ingame_date = load_from_json("current_date")["current_ingame_date"]
    g.lore_days = ["Lunesdag", "Flamdag", "Quellsdag", "Waldsdag", "Goldag", "Terrasdag", "Sunnesdag"]
    g.lore_months = ["Eismond", "Frostmond", "Saatmond", "Blütenmond", "Wonnemond", "Heumond", "Sonnenmond",
                     "Erntemond", "Fruchtmond", "Weinmond", "Nebelmond", "Julmond"]

    g.static = "/static/"
    g.debug = app.debug

    g.categories = {
        "Characterium": "characters",
        "Gentarium": "gentarium",
        "Geographium": "locations",
        "Gradarium": "tierlist",
        "Linguarium": "linguarium",
        "Theologarium": "theologarium"
    }

    apex_domain = "zetsuboushii.site/"
    image_subdomain = "https://images."
    g.img_host = image_subdomain + apex_domain + "dnd/"
    g.img_host_resized = image_subdomain + apex_domain + "dnd/"
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


def check_alt_image_exists(name: str, timeout: float = 5.0) -> tuple[bool, str, int] | tuple[bool, None, None]:
    base_url = f"{g.img_host}characters/{name} alt"
    extensions = ["png", "jpg"]

    for ext in extensions:
        url = f"{base_url}.{ext}"
        try:
            response = requests.head(url, timeout=timeout, allow_redirects=True)
            if response.status_code == 200:
                return True, url, response.status_code
        except requests.RequestException:
            pass

    return False, None, None


@app.route('/')
def index():
    highlights = ["Amlin", "Acilia", "Justicia", "Fortuna", "Meilira", "Thanatos", "Scarlet", "Cinnabar", "Seloue", "Craindre", "Zora", "Phaerille", "Finnea", "Alice", "Ar-Merer", "Artie", "Avarne", "Aya", "Carmesine", "Zetta", "Cordelia", "Felix", "Flüstern", "Fubuki", "Grenze", "Grund", "Hama", "Hindrik", "Iddra", "Igmusur"]
    characters_list = load_from_json("characters")
    characters_list[:] = [c for c in characters_list if "," not in c["name"] and "[hidden]" not in c["name"]]
    highlighted_characters = [c for c in characters_list if "<h2>" in c["biography"]]
    characters_list.sort(key=lambda character: character["name"].lower().replace(" & ", ""))
    calendar_list = load_from_json("calendar")
    current_day = g.current_date
    journals = {
        "nayru": load_from_json("journals/journal_nayru"),
        "agraston": load_from_json("journals/journal_agraston")
    }

    birthday_characters = []
    for char in characters_list:
        data = char.copy()

        if data.get('birthday') != "":
            birthday_day, birthday_month = 0, 0
            if len(data["birthday"].split(".")) == 2:
                birthday_day, birthday_month = map(int, data['birthday'].split('.'))
            if f"{birthday_day:02}" == f"{current_day.day:02}" and f"{birthday_month:02}" == f"{current_day.month:02}":
                birthday_characters.append(data)

    return render_template('index.html', birthday_characters=birthday_characters, journals=journals,
                           highlighted_characters=highlighted_characters, holidays=calendar_list,
                           characters=characters_list, current_day=current_day)


@app.route('/characterium/')
def characters():
    characters_list = load_from_json("characters")
    if app.debug:
        for character in characters_list:
            character["name"] = character["name"].replace(" [hidden]", "")
    else:
        characters_list[:] = [c for c in characters_list if "," not in c["name"] and "[hidden]" not in c["name"]]
    characters_list.sort(key=lambda character: character["name"].lower().replace(" & ", ""))

    letters = sorted({character['name'][0].upper() for character in characters_list})
    nationalities = sorted({character['nationality'] for character in characters_list if "nationality" in character})
    races = sorted({character['race'] for character in characters_list if
                    "race" in character and character.get('race') is not None})

    def is_complete(entry):
        for value in entry.values():
            if isinstance(value, str) and not value.strip():
                return False
            if isinstance(value, (list, dict)) and not value:
                return False
        return True

    return render_template('characters.html', characters=characters_list, letters=letters, nationalities=nationalities,
                           races=races, is_complete=is_complete)


@app.route('/characterium/<character_name>/')
def character(character_name):
    characters_list = load_from_json("characters")
    if app.debug:
        for character in characters_list:
            character["name"] = character["name"].replace(" [hidden]", "")
    else:
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
                birthday_string = f"{birthday_d.lstrip('0')}. Tag des {g.lore_months[int(birthday_m) - 1]}es"
                character['birthday'] = birthday_string

            character['has_alt'], character['alt_img_url'], _ = check_alt_image_exists(character_name)
            break

    if character is None:
        return redirect('/')
    return render_template('character.html', character=character, characters=characters_list)


@app.route('/geographium/')
def locations():
    locations_list = load_from_json("locations")
    return render_template('locations.html', locations=locations_list)


@app.route('/geographium/<location_name>/')
def location(location_name):
    locations_list = load_from_json("locations")
    location_data, parent = find_place_recursively(locations_list, location_name)

    return render_template('place.html', location=location_data, parent=parent)


@app.route('/edit/geographium/<place_name>/', methods=['POST'])
def edit_place(place_name):
    if app.debug:
        locations_list = load_from_json("locations")
        place_data, _ = find_place_recursively(locations_list, place_name)

        if request.method == "POST":
            return


@app.route('/compendium/')
def compendia():
    compendium_list = load_from_json("compendia")
    compendium_list.sort(key=lambda compendium: compendium["name"])

    return render_template('old/compendia.html', compendium_list=compendium_list)


@app.route('/gentarium/')
def gentarium():
    gentarium_data = load_from_json(f"compendia/gentarium")
    characters_list = load_from_json("characters")

    by_race = defaultdict(list)
    for c in characters_list:
        name = c.get("name", "")
        if "[hidden]" not in name.lower():
            by_race[c.get("race")].append(c)

    for race in gentarium_data:
        matches = by_race.get(race.get("title"), [])
        race["example"] = random.choice(matches)["name"] if matches else None

    return render_template('compendia/gentarium.html', compendium=gentarium_data)


@app.route('/gentarium/<entry_name>/')
def gentarium_entry(entry_name):
    entries = load_from_json("compendia/gentarium")
    entry = next((e for e in entries if e.get("title", "").lower() == entry_name.lower()), None)
    characters_list = load_from_json("characters")

    by_race = defaultdict(list)
    for character in characters_list:
        name = character.get("name", "")
        if "[hidden]" not in name.lower():
            by_race[character.get("race")].append(character)

        matches = by_race.get(entry.get("title"), [])
        entry["example"] = random.choice(matches)["name"] if matches else None
    return render_template('compendia/gentarium_entry.html', entry=entry)


@app.route('/linguarium/')
def linguarium():
    linguarium_data = load_from_json(f"compendia/linguarium")
    return render_template('compendia/linguarium.html', compendium=linguarium_data)


@app.route('/linguarium/<entry_name>/')
def linguarium_entry(entry_name):
    entries = load_from_json("compendia/linguarium")
    entry = next((e for e in entries if e.get("title", "").lower() == entry_name), None)

    return render_template('compendia/linguarium_entry.html', entry=entry)


@app.route('/theologarium/')
def theologarium():
    theologarium_data = load_from_json(f"compendia/theologarium")
    return render_template('compendia/theologarium.html', compendium=theologarium_data)


@app.route('/theologarium/<entry_name>/')
def theologarium_entry(entry_name):
    entries = load_from_json("compendia/theologarium")
    entry = next((e for e in entries if e.get("id", "").lower().replace(" ", "-") == entry_name), None)

    return render_template('compendia/theologarium_entry.html', entry=entry)


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
    characters_list = load_from_json("characters")
    characters_list[:] = [c for c in characters_list if "," not in c["name"] and "[hidden]" not in c["name"]]
    characters_list.sort(key=lambda character: character["name"].lower().replace(" & ", ""))

    return render_template('tierlist.html', characters=characters_list)


if __name__ == '__main__':
    app.run()
