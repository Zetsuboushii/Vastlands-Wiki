import random
from datetime import date

from flask import Flask, render_template, request, g, redirect, url_for
import json

from flask_frozen import Freezer

app = Flask(__name__, static_folder="static")
freezer = Freezer(app)

app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'


def load_from_json(filename):
    with open(f'static/json/{filename}.json', encoding="utf8") as file:
        return json.load(file)


@app.before_request
def before_request():
    g.site_title = "Tome of the Vastlands"
    g.version_number = "b3.⛩"

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

    g.random_banner = f'ui/banner-{random.randint(1, 9)}.png'


def find_place_recursively(place_list, place_slug, parent_name=None):
    for place in place_list:
        if place['name'].lower().replace(" ", "-") == place_slug:
            return place, parent_name

        if "contains" in place and isinstance(place["contains"], list):
            found, parent = find_place_recursively(place["contains"], place_slug, place["name"])
            if found is not None:
                return found, parent

    return None, None


news_list = load_from_json("news")
enemy_list = load_from_json("bestiarium")
actions_list = load_from_json("actions")
places_list = load_from_json("places")
abilities_list = load_from_json("abilities")


@app.route('/')
def index():
    characters_list = load_from_json("characters")
    characters_list = [entry for entry in characters_list if not entry.get('hidden')]
    characters_list.sort(key=lambda character: character["name"].lower())
    calendar_list = load_from_json("calendar")
    current_day = date.today()

    birthday_characters = []
    for char in characters_list:
        data = char.copy()

        if data.get('birthday') != "":
            birthday_day, birthday_month = 0, 0
            if len(data["birthday"].split(".")) == 2:
                birthday_day, birthday_month = map(int, data['birthday'].split('.'))

            if len(data["birthday"].split(".")) == 3:
                birthday_day, birthday_month, birthday_year = map(int, data['birthday'].split('.'))

            if f"{birthday_day:02}" == f"{current_day.day:02}" and f"{birthday_month:02}" == f"{current_day.month:02}":
                birthday_characters.append(data)

    rand_char = random.choice(characters_list)

    return render_template('index.html', birthday_characters=birthday_characters, news=news_list, rand_char=rand_char,
                           holidays=calendar_list, characters=characters_list, current_day=current_day)


@app.route('/characters/')
def characters():
    characters_list = load_from_json("characters")
    characters_list = [entry for entry in characters_list if not entry.get('hidden')]
    characters_list.sort(key=lambda character: character["name"].lower())

    letters = sorted({character['name'][0].upper() for character in characters_list})
    nationalities = sorted({character['nationality'] for character in characters_list if "nationality" in character})

    return render_template('characters.html', characters=characters_list, letters=letters, nationalities=nationalities)


@app.route('/characters/<character_name>/')
def character(character_name):
    characters_list = load_from_json("characters")
    characters_list = [entry for entry in characters_list if not entry.get('hidden')]
    characters_list.sort(key=lambda character: character["name"].lower())
    character_data = None
    data = None

    character_name = character_name.lower().replace(" ", "-")

    for char in characters_list:
        char_name = char['name'].lower().replace(" ", "-")
        if char_name == character_name:
            data = char.copy()

            break
        else:
            for alias in char["aliases"]:
                if character_name == alias['alias'].lower().replace(" ", "-"):
                    data = char.copy()
                    break

    if data is not None and data.get('birthday') != "":
        ingame_day, ingame_month, ingame_year = map(int, g.ingame_date.split('.'))

        if len(data["birthday"].split(".")) == 2:
            birthday_day, birthday_month = map(int, data['birthday'].split('.'))
            data['birth_day'] = str(birthday_day)
            data['birth_month'] = g.lore_months[birthday_month - 1]

        if len(data["birthday"].split(".")) == 3:
            birthday_day, birthday_month, birthday_year = map(int, data['birthday'].split('.'))
            data['birth_year'] = str(birthday_year)
            data['age'] = ingame_year - birthday_year - (
                    (ingame_month, ingame_day) < (birthday_month, birthday_day))
            data['birth_day'] = str(birthday_day)
            data['birth_month'] = g.lore_months[birthday_month - 1]

    character_data = data

    if character_data is None:
        return redirect('/')
    return render_template('character.html', character=character_data)


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
    elif compendium_name == "gladiarium":
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
    characters_list = [entry for entry in characters_list if not entry.get('hidden')]
    characters_list.sort(key=lambda character: character["name"].lower())

    return render_template('tierlist.html', characters=characters_list)


if __name__ == '__main__':
    app.run(debug=True)
