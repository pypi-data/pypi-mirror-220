from collections import defaultdict

icon_mapping = {
    ".py": ":snake:",
    ".pyc": ":snake:",
    ".ipynb": ":snake:",
    ".rs": ":crab:",
    ".ts": ":paperclip:",
    ".tsx": ":paperclip:",
    ".js": ":rhinoceros:",
    ".jsx": ":rhinoecros:",
    ".lua": ":ringed_planet:",
    ".md": ":blue_book:",
    ".txt": ":book:",
    ".yaml": ":closed_book:",
    ".yml": ":closed_book:",
    ".toml": ":closed_book:",
    ".json": ":closed_book:",
    ".html": ":globe_showing_americas:",
    ".css": ":paintbrush:",
    ".exe": ":floppy_disk:",
    ".cc": ":tropical_fish:",
    ".cpp": ":tropical_fish:",
    ".jar": ":robot:",
    ".java": ":robot:",
    ".php": ":elephant:",
    ".sql": ":dolphin:",
    ".sqlite": ":dolphin:",
    ".db": ":floppy_disk:",
    ".jpg": ":framed_picture:",
    ".jpeg": ":framed_picture:",
    ".svg": ":framed_picture:",
    ".png": ":framed_picture:",
    ".gif": ":framed_picture:",
    ".mp3": ":musical_note:",
    ".wav": ":musical_note:",
    ".flac": ":musical_note:",
    ".aac": ":musical_note:",
    ".ogg": ":musical_note:",
    ".wma": ":musical_note:",
    ".mp4": ":movie_camera:",
    ".flv": ":movie_camera:",
    ".webm": ":movie_camera:",
    ".ogv": ":movie_camera:",
}

icons = defaultdict(lambda: ":seedling:", icon_mapping)