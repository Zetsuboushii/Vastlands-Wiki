import json


def extract_effect_types(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    effect_types = set()

    for action in data:
        if "effects" in action:
            for effect in action["effects"]:
                if "type" in effect:
                    effect_types.add(effect["type"])

    effects_list = []
    for et in sorted(effect_types):
        effects_list.append({
            "name": et,
            "impact": 0,
            "text": ""
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(effects_list, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    extract_effect_types("actions.json", "v2/effects.json")
