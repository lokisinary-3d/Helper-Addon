#text_web_search.py

import bpy
import webbrowser
import random

# List of highly sensitive inappropriate keywords
INAPPROPRIATE_KEYWORDS = [
    "adult", "explicit", "nude", "prostitute", "nsfw", "inappropriate",
    "porn", "xxx", "sex", "nude", "erotic", "hentai",
    "sensual", "intimate", "passion", "erogenous",
    "playboy", "penthouse", "playgirl", "brazzers",
    "redtube", "xvideos", "youporn", "chaturbate",
    "escort", "prostitute", "massage", "escort service",
    "sexy", "naked", "lingerie", "orgasm", "intimacy",
    "seduce", "pleasure", "provocative", "lust", "bare",
    "eroticism", "stimulate", "kinky", "risque", "sensuality",
    "violence", "harm", "danger", "kill", "death",
    "brutal", "aggression", "abuse", "hate", "suicide",
    "self-harm", "illegal", "crime", "drugs", "terrorist",
    "extremist", "cult", "brazzers", "racism", "terrorism", "misogyny",
    "hate speech", "incest", "bestiality", "incestuous",
    "pedophilia", "child pornography", "rape", "rape scene",
    "cannibalism", "necrophilia", "zoophilia", "gore",
    "torture", "mutilation", "snuff", "self-cannibalism", "dickhead", "pussy", "vegina", "penis",
    # Add more highly sensitive keywords as needed
]

# Additional allowed keywords
ALLOWED_KEYWORDS = ["gun", "weapon", "car", "fantasy", "sword", "tutorial", "blender", "documment", "blender documment", "blender manual", "Reference",]

# URLs to check for search text
SEARCH_URLS = [
    "https://docs.blender.org/manual/en/latest/index.html",
    "https://docs.blender.org/manual/en/latest/genindex.html",
    "https://docs.blender.org/manual/en/latest/glossary/index.html"
]

def perform_web_search(search_text, search_engine):
    if search_text:
        lower_search_text = search_text.lower()

        for keyword in ALLOWED_KEYWORDS:
            if keyword in lower_search_text:
                search_query = f"Blender {search_text} "
                search_query = search_query.replace(" ", "+")
                search_url = f"https://www.google.com/search?q={search_query}&safe=active"
                if search_engine == 'youtube':
                    search_url = f"https://www.youtube.com/results?search_query={search_query}"
                webbrowser.open_new_tab(search_url)
                return f"Searching for Blender-related '{search_text}' with keyword '{keyword}'..."

        # Check if any highly sensitive inappropriate keyword is present
        if any(keyword in lower_search_text for keyword in INAPPROPRIATE_KEYWORDS):
            random_inappropriate_keyword = random.choice(INAPPROPRIATE_KEYWORDS)
            search_query = f"Blender {random_inappropriate_keyword} "
            search_query = search_query.replace(" ", "+")
            if search_engine == 'google':
                search_url = f"https://www.google.com/search?q={search_query}&safe=active"
            elif search_engine == 'youtube':
                search_url = f"https://www.youtube.com/results?search_query={search_query}"
            webbrowser.open_new_tab(search_url)
            return f"Searching for Blender-related '{random_inappropriate_keyword}' (randomly chosen)..."

        # Modify the search query to include "Blender" as a keyword
        search_query = f"Blender {search_text} "
        search_query = search_query.replace(" ", "+")
        if search_engine == 'google':
            search_url = f"https://www.google.com/search?q={search_query}&safe=active"
        elif search_engine == 'youtube':
            search_url = f"https://www.youtube.com/results?search_query={search_query}"
        webbrowser.open_new_tab(search_url)
        return f"Searching for Blender-related '{search_text}'..."

    else:
        return "Please enter text to search."

class OBJECT_OT_TextWebSearchOperator(bpy.types.Operator):
    bl_idname = "object.text_web_search"
    bl_label = "Search Web"
    bl_description = "Perform a Google search based on entered text"
    
    search_engine: bpy.props.EnumProperty(
        items=[('google', 'Google', 'Google Search'), ('youtube', 'YouTube', 'YouTube Search')],
        name="Search Engine"
    )

    def execute(self, context):
        search_text = bpy.context.scene.custom_search_text
        message = perform_web_search(search_text, self.search_engine)
        self.report({'INFO'}, message)
        return {'FINISHED'}

class OBJECT_OT_YouTubeTextWebSearchOperator(bpy.types.Operator):
    bl_idname = "object.youtube_text_web_search"
    bl_label = "YouTube Text Web Search"
    bl_description = "Perform a YouTube search based on entered text"
    
    search_engine: bpy.props.EnumProperty(
        items=[('google', 'Google', 'Google Search'), ('youtube', 'YouTube', 'YouTube Search')],
        name="Search Engine"
    )

    def execute(self, context):
        search_text = bpy.context.scene.custom_search_text
        message = perform_web_search(search_text, 'youtube')  # Perform YouTube search
        self.report({'INFO'}, message)
        return {'FINISHED'}