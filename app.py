import random
from datetime import date
from flask import Flask, render_template, abort, g
import json

app = Flask(__name__)


@app.before_request
def before_request():
    g.site_title = "Tome of the Vastlands"
    g.version_number = "v3.⛩"

    g.ingame_date = "24.12.394"
    g.lore_days = ["Lunesdag", "Flamdag", "Quellsdag", "Waldsdag", "Goldag", "Terrasdag", "Sunnesdag"]
    g.lore_months = ["Eismond", "Frostmond", "Saatmond", "Blütenmond", "Wonnemond", "Heumond", "Sonnenmond",
                     "Erntemond", "Fruchtmond", "Weinmond", "Nebelmond", "Julmond"]

    g.static = "/static/"

    g.categories = {
        "Charaktere": "characters",
        "Kompendien": "compendia",
    }

    apex_domain = "zetsuboushii.site/"
    image_subdomain = "https://images."
    g.img_host = image_subdomain + apex_domain + "dnd/"
    g.img_host_resized = image_subdomain + apex_domain + "resized/dnd/"

    g.random_banner = random.randint(1, 9)


def load_from_json(filename):
    with open(f'static/json/{filename}.json') as file:
        return json.load(file)


characters_list = load_from_json("characters")
news_list = load_from_json("news")
compendium_list = load_from_json("compendia")
calendar_list = load_from_json("calendar")


@app.route('/')
def index():
    birthday_characters = []
    for char in characters_list:
        data = char.copy()

        if data.get('birthday') != "":
            birthday_day, birthday_month, _ = map(int, data['birthday'].split('.'))

            current_day = date.today()
            if f"{birthday_day:02}" == f"{current_day.day:02}" and f"{birthday_month:02}" == f"{current_day.month:02}":
                birthday_characters.append(data)

    rand_char = random.choice(characters_list)

    return render_template('index.html', birthday_characters=birthday_characters, news=news_list, rand_char=rand_char,
                           holidays=calendar_list, characters=characters_list)


@app.route('/characters/')
def characters():
    return render_template('characters.html', characters=characters_list)


@app.route('/characters/<character_name>')
def character(character_name):
    character_data = None

    for char in characters_list:
        if char['name'].lower() == character_name.lower():
            data = char.copy()

            if data.get('birthday') != "":
                birthday_day, birthday_month, birthday_year = map(int, data['birthday'].split('.'))
                ingame_day, ingame_month, ingame_year = map(int, g.ingame_date.split('.'))

                data['birth_day'] = str(birthday_day)
                data['birth_month'] = g.lore_months[birthday_month - 1]
                data['birth_year'] = str(birthday_year)
                data['age'] = ingame_year - birthday_year - (
                        (ingame_month, ingame_day) < (birthday_month, birthday_day))

            match data.get('status'):
                case "true":
                    data['status'] = "am Leben"
                    pass
                case "false":
                    data['status'] = "verstorben"
                    pass
                case _:
                    pass

            character_data = data
            break

    if character_data is None:
        abort(404)

    return render_template('character.html', character=character_data)


@app.route('/compendium/')
def compendia():
    return render_template('compendia.html', compendium_list=compendium_list)


@app.route('/compendium/<compendium_name>')
def compendium(compendium_name):
    compendium_data = None

    for compendium in compendium_list:
        if compendium['name'].lower() == compendium_name.lower():
            compendium_data = load_from_json(compendium['name'].lower())
            break

    if compendium_name == "gentarium":
        for race in compendium_data:
            for character in characters_list:
                if character["race"] == race["name"]:
                    race["example"] = character["name"]

    return render_template('compendium.html', compendium_name=compendium_name, compendium=compendium_data)


@app.route('/compendium/<compendium_name>/<entry_name>')
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
            for character in characters_list:
                if character["race"] == entry_name.capitalize():
                    entry["example"] = character["name"]
            return render_template('gentarium.html', entry=entry)
        case "linguarium":
            return render_template('linguarium.html', entry=entry)


@app.route('/holidays/<holiday_name>')
def holidays(holiday_name):
    entry = None

    for entry_json in calendar_list:
        if entry_json['name'].lower().replace(" ", "-") == holiday_name.lower().replace(" ", "-"):
            entry = entry_json

    return render_template('holidays.html', entry=entry)


if __name__ == '__main__':
    app.run(debug=True)
