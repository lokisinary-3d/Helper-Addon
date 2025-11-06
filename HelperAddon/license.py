# license.py

import bpy
import os
import tempfile
import webbrowser

class OBJECT_OT_DisplayLicenseOperator(bpy.types.Operator):
    bl_idname = "object.display_license"
    bl_label = "Display Addon Information"
    bl_description = "Open the License file"

    def execute(self, context):
        addon_directory = os.path.dirname(__file__)
        license_path = os.path.join(addon_directory, "LICENSE")

        try:
            # Create a temporary HTML file
            temp_html_path = os.path.join(tempfile.gettempdir(), "addon_license.html")
            with open(temp_html_path, "w") as html_file:
                html_file.write(f'<html><body><pre>{open(license_path).read()}</pre></body></html>')

            # Open the temporary HTML file in the user's default web browser
            webbrowser.open(f"file://{temp_html_path}")
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {e}")

        return {'FINISHED'}