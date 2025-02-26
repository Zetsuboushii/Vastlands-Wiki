#!/usr/bin/env python3

import sys
import json

def main():
    if len(sys.argv) != 5:
        print("Call: python script.py <NameA> <NameB> <RelationAB> <RelationBA>")
        sys.exit(1)

    nameA = sys.argv[1]
    nameB = sys.argv[2]
    relationAB = sys.argv[3]
    relationBA = sys.argv[4]

    json_path = "characters.json"

    with open(json_path, "r", encoding="utf-8") as f:
        characters = json.load(f)

    # Charaktere suchen
    charA = None
    charB = None

    for char in characters:
        if char.get("name") == nameA:
            charA = char
        elif char.get("name") == nameB:
            charB = char

    if not charA:
        print(f"Charakter '{nameA}' nicht in {json_path} gefunden!")
        sys.exit(1)
    if not charB:
        print(f"Charakter '{nameB}' nicht in {json_path} gefunden!")
        sys.exit(1)

    updated = False
    for rel in charA["relationships"]:
        if rel.get("character") == nameB:
            rel["relation"] = relationAB
            updated = True
            break
    if not updated:
        charA["relationships"].append({"character": nameB, "relation": relationAB})

    updated = False
    for rel in charB["relationships"]:
        if rel.get("character") == nameA:
            rel["relation"] = relationBA
            updated = True
            break
    if not updated:
        charB["relationships"].append({"character": nameA, "relation": relationBA})

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(characters, f, ensure_ascii=False, indent=2)

    print(f"Wrote relation of '{nameA}' and '{nameB}' successfully.")

if __name__ == "__main__":
    main()
