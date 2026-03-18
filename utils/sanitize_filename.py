import re


def sanitize_filename(name):
    name = name.replace("\n", " ").replace("\r", " ").strip()
    name = re.sub(r'[<>:"/\\|?*]', "", name)  # remove inválidos
    return name
