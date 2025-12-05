import json


def extract_classes(json_file_path):
    base_classes = set()
    sub_classes = set()
    master_classes = set()

    with open(json_file_path, 'r', encoding='utf-8') as f:
        characters = json.load(f)

    for char in characters:
        classes_info = char.get("classes", {})

        baseclass = classes_info.get("baseclass")
        if baseclass:
            base_classes.add(baseclass)

        subclasses = classes_info.get("subclasses", [])
        for subclass in subclasses:
            sub_classes.add(subclass)

        masterclass = classes_info.get("masterclass")
        if masterclass:
            master_classes.add(masterclass)

    print("Base Classes:", sorted(base_classes))
    print("Sub classes:", sorted(sub_classes))
    print("Master classes:", sorted(master_classes))


if __name__ == "__main__":
    extract_classes("characters.json")
