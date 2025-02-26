import json
import sys
from typing import Optional, Dict, Any, List

VALID_NATIONALITIES = {"Faergria", "Kradian", "Kouyoukuni", "Markath", "Animus"}

def build_place_nationality_map(places: List[Dict[str, Any]],
                                current_nationality: Optional[str] = None) -> Dict[str, str]:
    place_map = {}

    for place in places:
        place_name = place.get("name")

        new_nationality = current_nationality
        if place_name in VALID_NATIONALITIES:
            new_nationality = place_name

        if new_nationality is not None:
            place_map[place_name] = new_nationality

        if "contains" in place and isinstance(place["contains"], list):
            deeper_map = build_place_nationality_map(place["contains"], new_nationality)
            place_map.update(deeper_map)

    return place_map

def main(characters_file: str, places_file: str, output_file: str) -> None:
    with open(places_file, "r", encoding="utf-8") as f_places:
        places_data = json.load(f_places)

    if isinstance(places_data, dict):
        places_data = [places_data]

    place_nationality_map = build_place_nationality_map(places_data)

    with open(characters_file, "r", encoding="utf-8") as f_char:
        characters_data = json.load(f_char)

    for character in characters_data:
        homes = character.get("homes", [])
        if homes:
            birthplace = homes[0].get("place")
            if birthplace in place_nationality_map:
                character["nationality"] = place_nationality_map[birthplace]
            else:
                character["nationality"] = "Unbekannt"

    with open(output_file, "w", encoding="utf-8") as f_out:
        json.dump(characters_data, f_out, ensure_ascii=False, indent=2)

    print(f"File '{output_file}' successfully written.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Call: python assign_nationalities.py <characters.json> <places.json> <output.json>")
        sys.exit(1)

    characters_file = sys.argv[1]
    places_file = sys.argv[2]
    output_file = sys.argv[3]

    main(characters_file, places_file, output_file)
