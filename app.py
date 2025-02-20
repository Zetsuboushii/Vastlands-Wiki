import random

from flask import Flask, render_template, abort, g
import json

app = Flask(__name__)


def load_characters_from_json():
    with open('static/json/characters.json') as file:
        return json.load(file)


characters = load_characters_from_json()


@app.before_request
def before_request():
    g.site_title = "Tome of the Vastlands"
    g.version_number = "b3.⛩"

    g.ingame_date = "24.12.394"
    g.lore_days = ["Lunesdag", "Flamdag", "Quellsdag", "Waldsdag", "Goldag", "Terrasdag", "Sunnesdag"]
    g.lore_months = ["Eismond", "Frostmond", "Saatmond", "Blütenmond", "Wonnemond", "Heumond", "Sonnenmond",
                     "Erntemond", "Fruchtmond", "Weinmond", "Nebelmond", "Julmond"]

    g.static = "/static/"

    apex_domain = "zetsuboushii.site/"
    g.img_host = "https://images." + apex_domain + "/dnd/characters/"

    g.random_banner = random.randint(1, 9)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/characters/<character_name>')
def character(character_name):
    character_data = None

    for char in characters:
        if char['name'].lower() == character_name.lower():
            data = char.copy()

            if data.get('birthday') != "":
                birthday_day, birthday_month, birthday_year = map(int, data['birthday'].split('.'))
                ingame_day, ingame_month, ingame_year = map(int, g.ingame_date.split('.'))

                data['birth_day'] = str(birthday_day)
                data['birth_month'] = g.lore_months[birthday_month - 1]
                data['birth_year'] = str(birthday_year)
                data['age'] = ingame_year - birthday_year - ((ingame_month, ingame_day) < (birthday_month, birthday_day))

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


if __name__ == '__main__':
    app.run(debug=True)
