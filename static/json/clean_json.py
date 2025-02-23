import re

def repair_and_remove_newlines(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        content = re.sub(r'},\s*}', '}]', content)
        content = re.sub(r',\s*]', ']', content)

        content = re.sub(r'"(text|excerpt)":\s*"([^"]*)"', lambda match: '"{}": "{}"'.format(match.group(1), re.sub(r'[\r\n]+', ' ', match.group(2))), content)

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"File '{filepath}' is now good.")
    except FileNotFoundError:
        print(f"File '{filepath}' not found.")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    filepath = "calendar.json"
    repair_and_remove_newlines(filepath)