# terms_and_conditions.py

import bpy
import os
import tempfile
import webbrowser

class OBJECT_OT_DisplayTermsAndConditionsOperator(bpy.types.Operator):
    bl_idname = "object.display_terms_and_conditions"
    bl_label = "Display Addon Information"
    bl_description = "Open the Terms And Conditions file"

    def execute(self, context):
        addon_directory = os.path.dirname(__file__)
        terms_and_conditions_path = os.path.join(addon_directory, "TERMS_AND_CONDITIONS.md")

        try:
            # Create a temporary HTML file
            temp_html_path = os.path.join(tempfile.gettempdir(), "addon_terms_and_conditions.html")
            with open(temp_html_path, "w") as html_file:
                html_file.write(f'<html><body><pre>{open(terms_and_conditions_path).read()}</pre></body></html>')

            # Open the temporary HTML file in the user's default web browser
            webbrowser.open(f"file://{temp_html_path}")
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {e}")

        return {'FINISHED'}