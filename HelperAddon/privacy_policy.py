# privacy_policy.py

import bpy
import os
import tempfile
import webbrowser

class OBJECT_OT_DisplayPrivacyPolicyOperator(bpy.types.Operator):
    bl_idname = "object.display_privacy_policy"
    bl_label = "Display Addon Information"
    bl_description = "Open the Privacy Policy file"

    def execute(self, context):
        addon_directory = os.path.dirname(__file__)
        privacy_policy_path = os.path.join(addon_directory, "PrivacyPolicy.md")

        try:
            # Create a temporary HTML file
            temp_html_path = os.path.join(tempfile.gettempdir(), "addon_privacy_policy.html")
            with open(temp_html_path, "w") as html_file:
                html_file.write(f'<html><body><pre>{open(privacy_policy_path).read()}</pre></body></html>')

            # Open the temporary HTML file in the user's default web browser
            webbrowser.open(f"file://{temp_html_path}")
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {e}")

        return {'FINISHED'}