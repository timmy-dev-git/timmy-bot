from datetime import datetime, timedelta
from Data import Data

def format_message(title: str, description: str) -> str:
    formatted_message: str = "```╭──────────────────────────────╮\n"
    MAX_CHARS = 28
    index = 0
    for segment in title.split('\n'):
        MAX_CHARS = 27
        INDENT = 0
        words: list[str] = []
        for word in segment.split(' '):
            if len(word) == 0:
                INDENT += 1
                continue
            while len(word) > MAX_CHARS:
                words.append(word[:MAX_CHARS])
                word = word[MAX_CHARS:]
            words.append(word)

        MAX_CHARS = 28
        formatted_message += f"│ {' ' * INDENT}"
        index = INDENT
        for word in words:
            if index + len(word) + 1 > MAX_CHARS:
                formatted_message += f"{' ' * (MAX_CHARS - index)} │\n│ {' ' * INDENT}"
                index = INDENT
            formatted_message += word + ' '
            index += len(word) + 1
        formatted_message += f"{' ' * (MAX_CHARS - index)} │\n"

    formatted_message += "├══════════════════════════════┤\n"

    for segment in description.split('\n'):
        MAX_CHARS = 27
        INDENT = 0
        words = []
        for word in segment.split(' '):
            if len(word) == 0:
                INDENT += 1
                continue
            while len(word) > MAX_CHARS:
                words.append(word[:MAX_CHARS])
                word = word[MAX_CHARS:]
            words.append(word)

        MAX_CHARS = 28
        formatted_message += f"│ {' ' * INDENT}"
        index = INDENT
        for word in words:
            if index + len(word) + 1 > MAX_CHARS:
                formatted_message += f"{' ' * (MAX_CHARS - index)} │\n│ {' ' * INDENT}"
                index = INDENT
            formatted_message += word + ' '
            index += len(word) + 1
        formatted_message += f"{' ' * (MAX_CHARS - index)} │\n"

    formatted_message += "╰──────────────────────────────╯```"

    return formatted_message

def format_time(id: int, date: datetime) -> str:
    d: datetime = date + timedelta(hours=Data(id, "offset").read()["offset"])
    return f"[{d.hour:02d}:{d.minute:02d} {d.day:02d}/{d.month:02d}/{d.year:04d}]"