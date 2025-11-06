# addons_panel.py

import bpy
import re
from . import bl_info  # Import bl_info from the add-on module

def prettify_addon_name(addon_name):
    # Define regular expression patterns for common naming conventions
    patterns = [
        (r'(?<!^)(?=[A-Z])', ' '),  # Split camel case
        (r'_+', ' '),              # Replace underscores with space
    ]
    
    # Apply each pattern to the addon name
    for pattern, replacement in patterns:
        addon_name = re.sub(pattern, replacement, addon_name)
    
    # Capitalize each word
    return addon_name.title()

class AddonShowOperator(bpy.types.Operator):
    """Show addon preferences"""
    bl_idname = "wm.addon_show"
    bl_label = "Show Addon Preferences"
    module: bpy.props.StringProperty()

    def execute(self, context):
        bpy.ops.preferences.addon_show(module=self.module)
        return {'FINISHED'}

bpy.utils.register_class(AddonShowOperator)

class HelperAddonsPanel(bpy.types.Panel):
    bl_label = "Addons"
    bl_idname = "HELPER_PT_helper_addons"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Helper'
    bl_description = "A collection of blender tools and addons"
    bl_version = (1, 4)
    bl_author = "lokisinary"
    bl_order = 3

    def draw(self, context):
        layout = self.layout

        # Get the list of all add-ons
        addons = bpy.utils._addon_utils.modules()

        # Count the total number of add-ons
        num_addons = len(addons)

        # Show the total number of add-ons
        layout.label(text=f"Total Add-ons: {num_addons}")

        # Get the list of enabled add-ons
        enabled_addons = bpy.context.preferences.addons

        # Sort the enabled add-ons alphabetically
        sorted_addons = sorted(enabled_addons.items(), key=lambda x: x[0].lower())

        # Count the number of enabled add-ons
        num_enabled_addons = len(sorted_addons)

        # Show the number of enabled add-ons as a toggleable button with down and right arrows
        row = layout.row()
        row.prop(context.scene, "show_enabled_addons", toggle=True, text=f"Enabled Add-ons: {num_enabled_addons}", icon='TRIA_DOWN' if context.scene.show_enabled_addons else 'TRIA_RIGHT')

        # Show the names of enabled add-ons if the toggle is enabled
        if context.scene.show_enabled_addons:
            # Create a sub-layout for the enabled add-ons
            sub_layout = layout.box().column()

            # Show the names of enabled add-ons with numbering and gear icon
            for index, (addon_name, addon_info) in enumerate(sorted_addons, start=1):
                # Retrieve the addon's bl_info dictionary
                addon_preferences = addon_info.preferences

                # Get the addon name from bl_info or prettify the addon_name
                if addon_preferences and hasattr(addon_preferences, "name"):
                    pretty_name = addon_preferences.name
                else:
                    pretty_name = prettify_addon_name(addon_name)

                # Add row for addon name and gear icon
                sub_row = sub_layout.row(align=True)
                sub_row.label(text=f"{index}. {pretty_name}")

                # Assign operator to gear icon
                sub_row.operator("wm.addon_show", text="", icon='PREFERENCES', emboss=False).module = addon_name

        # Add a row for the "Info" section with a toggleable button
        info_row = layout.row()
        info_row.prop(context.scene, "show_info", toggle=True, text="Info", icon='INFO' if context.scene.show_info else 'FILE_TICK')

        # Show additional information if the toggle is enabled
        if context.scene.show_info:
            info_layout = layout.box().column()
            info_layout.label(icon='USER', text=f"Author: {self.bl_author}")
            version = ".".join(str(num) for num in self.bl_version)  # Convert tuple to string with dot as separator
            info_layout.label(icon='TEXT', text=f"Version: {version}")
            
            # Add buttons to display the README and License in the same row
            row = info_layout.row(align=True)
            row.alignment = 'LEFT'  # Align the buttons to the left
            row.operator("object.display_readme", text="Readme", icon='HELP', emboss=False)
            row.operator("object.display_license", text="License", icon='COPY_ID', emboss=False)

            # Add a button to display the Privacy and Terms in the same row
            row = info_layout.row(align=True)
            row.alignment = 'LEFT'  # Align the button to the left
            row.operator("object.display_privacy_policy", text="Privacy Policy", icon='LOCKED', emboss=False)
            row.operator("object.display_terms_and_conditions", text="Terms And Conditions", icon='BOOKMARKS', emboss=False)