import re

def repair_and_remove_newlines(filepath):
    """
    Versucht, eine beschädigte JSON-Datei zu reparieren und Zeilenumbrüche zu entfernen.

    Args:
        filepath (str): Der Pfad zur JSON-Datei.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        # Versuche, grundlegende JSON-Strukturfehler zu reparieren
        content = re.sub(r'},\s*}', '}]', content)  # Ersetze fehlerhafte Array-Enden
        content = re.sub(r',\s*]', ']', content)  # Entferne überflüssige Kommas in Arrays

        # Entferne Zeilenumbrüche aus 'text'- und 'excerpt'-Werten
        content = re.sub(r'"(text|excerpt)":\s*"([^"]*)"', lambda match: '"{}": "{}"'.format(match.group(1), re.sub(r'[\r\n]+', ' ', match.group(2))), content)

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Datei '{filepath}' repariert und Zeilenumbrüche entfernt.")
    except FileNotFoundError:
        print(f"Fehler: Datei '{filepath}' nicht gefunden.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    filepath = "characters.json"  # Passe den Dateipfad bei Bedarf an
    repair_and_remove_newlines(filepath)