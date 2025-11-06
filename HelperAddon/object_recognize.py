#object_recognize.py

import bpy

def recognize_selected_object():
    active_object = bpy.context.active_object

    if active_object:
        return f"Recognized object: {active_object.name}"
    else:
        return "No object selected"
