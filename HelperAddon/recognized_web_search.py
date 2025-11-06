import bpy
import webbrowser
from .object_recognize import recognize_selected_object

def search_web_for_recognized_object():
    recognized_object = recognize_selected_object()
    if "No object selected" in recognized_object:
        return None
    else:
        recognized_object_name = recognized_object.replace("Recognized object: ", "")
        search_query = f"Blender {recognized_object_name} "
        return search_query

def open_web_browser_with_search(query, search_engine):
    search_url = f"https://www.google.com/search?q={query}" if search_engine == 'google' else f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open_new_tab(search_url)
    return f"Searching for '{query}'..."

class OBJECT_OT_WebSearchOperator(bpy.types.Operator):
    bl_idname = "object.web_search"
    bl_label = "Google Search"
    bl_description = "Perform a Google search for the recognized object"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        search_query = search_web_for_recognized_object()
        if search_query:
            message = open_web_browser_with_search(search_query, 'google')
            self.report({'INFO'}, message)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "No object selected. Please select an object.")
            return {'CANCELLED'}

class OBJECT_OT_YouTubeSearchOperator(bpy.types.Operator):
    bl_idname = "object.youtube_search"
    bl_label = "YouTube Search"
    bl_description = "Perform a YouTube search for the recognized object"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        search_query = search_web_for_recognized_object()
        if search_query:
            message = open_web_browser_with_search(search_query, 'youtube')
            self.report({'INFO'}, message)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "No object selected. Please select an object.")
            return {'CANCELLED'}
