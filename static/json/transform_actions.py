import json
import re


def transform_actions(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for action in data:
        if "effects" in action:
            for effect in action["effects"]:
                if "severity" in effect and isinstance(effect["severity"], str):
                    severity_str = effect["severity"].replace("lv", "")
                    if severity_str.isdigit():
                        effect["severity"] = int(severity_str)

                if "duration" in effect and isinstance(effect["duration"], str):
                    match = re.match(r"(\d+)([a-zA-Z])?", effect["duration"])
                    if match:
                        number_part = int(match.group(1))
                        letter_part = match.group(2) if match.group(2) else ""
                        effect["duration"] = number_part
                        effect["duration_type"] = letter_part

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    transform_actions("actions.json", "actions.json")
