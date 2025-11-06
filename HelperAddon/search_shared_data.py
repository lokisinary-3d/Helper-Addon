# search_shared_data.py

from datetime import datetime
from typing import List

search_history: List[str] = []
MAX_SEARCH_HISTORY: int = 20

def format_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

def sanitize_input(text: str) -> str:
    return text.replace('-', ' ')

def append_search_history(entry: str) -> None:
    global search_history
    search_history.append(entry)
    search_history = search_history[-MAX_SEARCH_HISTORY:]

def add_search_history(search_text: str, search_query: str, bl_label: str) -> None:
    timestamp = format_timestamp()
    bl_label = sanitize_input(bl_label)
    search_query = sanitize_input(search_query)
    
    new_entry = f"{search_text} {timestamp} {bl_label} {search_query}"
    append_search_history(new_entry)