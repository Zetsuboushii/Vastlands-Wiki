from flask import url_for
from flask_frozen import Freezer
from app import app, load_from_json

freezer = Freezer(app)

@freezer.register_generator
def holiday_urls():
    holidays_list = load_from_json("calendar")

    for holiday in holidays_list:
        yield url_for('holidays', holiday_name=holiday['name'].lower().replace(" ", "-"))

if __name__ == '__main__':
    freezer.freeze()