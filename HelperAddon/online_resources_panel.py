#online_resources_panel.py

import bpy
from bpy.types import Operator, Panel
from . import search_shared_data  # Import the shared data module
from datetime import datetime
from datetime import datetime
from typing import List



class OnlineResourcesPanel(Panel):
    bl_label = "Helper Resources Panel"
    bl_idname = "HELPER_PT_OnlineResourcesPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Helper'
    bl_description = "A collection of tools to assist with object recognition and web searches in Blender"
    bl_version = (1, 4)
    bl_author = "lokisinary"
    bl_order = 1

    def draw(self, context):
        layout = self.layout

        online_resources_box = layout.box()
        online_resources_box.label(text="Resources:")

        # Add an option field to choose between online resources
        search_type_row = online_resources_box.row(align=True)
        search_type_row.prop(context.scene, "online_search_type", text="Search Type")

        online_search_row = online_resources_box.row(align=True)
        online_search_row.prop(context.scene, "online_search_text", text="", emboss=True, icon='VIEWZOOM')

        # Add the search button for online resources
        search_operator_name = f"object.{context.scene.online_search_type}_search"
        button_label = f"Search on {context.scene.online_search_type.replace('_', ' ').title()}"
        online_resources_box.operator(search_operator_name, text=button_label)

        # Display search history dropdown
        history_box = layout.box()

        # Row for Search History and Information Icon
        row = history_box.row(align=True)

        # Toggle button for search history display
        toggle_icon = 'TRIA_DOWN' if context.scene.show_search_history else 'TRIA_RIGHT'
        row.operator("object.toggle_search_history", icon=toggle_icon, text="", emboss=False)
        row.label(text="Search History")

        # Add 'i' icon to show search history info
        row.operator("object.show_search_history_info", icon='INFO')

        # Display search history
        if context.scene.show_search_history:
            max_display_history = 4  # Maximum items to display in search history box
            if not search_shared_data.search_history:
                history_box.label(text="No history found")
            else:
                # Display search history
                for index, item in enumerate(reversed(search_shared_data.search_history[-max_display_history:])):
                    # Calculate the top-down numbering
                    top_down_number = len(search_shared_data.search_history) - index

                    split_item = item.rsplit(' ', 3)  # Split the entry into parts: query, timestamp, resource name, URL
                    if len(split_item) == 4:
                        query_text, timestamp_text, resource_text, url_text = split_item
                        label_text = f"{top_down_number}. {query_text.strip()} {timestamp_text.strip()} {resource_text.strip()} {url_text.strip()}"

                        # Splitting the resource_text and URL with a dash (-)
                        display_text = f"{query_text.strip()} {timestamp_text.strip()} {resource_text.strip()} - {url_text.strip()}"

                        copy_operator = row.operator("object.copy_website_url", text="", icon='COPY_ID')
                        copy_operator.url_text = url_text.strip()  # Assign the URL to the operator property

                    else:
                        label_text = f"{top_down_number}. {item}"  # Display search text only

                    history_box.label(text=label_text)



class ToggleSearchHistoryDisplayOperator(bpy.types.Operator):
    bl_idname = "object.toggle_search_history"
    bl_label = "Toggle Search History Display"
    bl_description = "Toggle the display of search history"

    def execute(self, context):
        # Toggle the visibility of the search history box
        context.scene.show_search_history = not context.scene.show_search_history

        max_search_history_box = 4  # Set maximum limit for the search history box
        if len(search_shared_data.search_history) > max_search_history_box:
            search_shared_data.search_history = search_shared_data.search_history[:max_search_history_box]

        return {'FINISHED'}


class CopyWebsiteNameOperator(bpy.types.Operator):
    bl_idname = "object.copy_website_url"
    bl_label = "Copy Website URL"
    bl_description = "Copy the website URL to the clipboard"

    url_text: bpy.props.StringProperty()  # Property for URL

    def execute(self, context):
        # Copy only the URL to the clipboard
        bpy.context.window_manager.clipboard = self.url_text
        return {'FINISHED'}





class ShowSearchHistoryInfoOperator(Operator):
    bl_idname = "object.show_search_history_info"
    bl_label = ""
    bl_description = "Display search history information"

    def format_timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    def generate_formatted_history(self, header: List[tuple]) -> str:
        formatted_history = (
            "----------------------------------------------------------------------------------------------------\n"
            "                                        Helper Addon by Lokisinary\n"
            "-----------------------------------------------------------------------------------------------------\n"
            "Helper Addon Online Resources Search History\n\n"
        )

        for column, width in header:
            formatted_history += f"{column:<{width}}  "
        formatted_history += "\n" + "-" * sum(width for _, width in header) + "\n"
        return formatted_history

    def execute(self, context) -> dict:
        header = [
            ("No.", 5),
            ("Search Query", 23),
            ("Timestamp", 29),
            ("Resource Name", 30),
            ("URL", 0)
        ]

        formatted_history = self.generate_formatted_history(header)

        for index, item in enumerate(search_shared_data.search_history, start=1):
            split_item = item.split(' ')
            if len(split_item) > 3:
                query_text = f"{split_item[0]} "
                timestamp_text = f"{split_item[1]} {split_item[2]} {split_item[3]}"

                resource_text = ' '.join(split_item[4:-1])
                url_text = split_item[-1]

                formatted_history += f"{index:<5} {query_text:<25} {timestamp_text:<30} {resource_text:<30}{url_text}\n"

        formatted_history += "-" * sum(width for _, width in header) + "\n"
        self.report({'INFO'}, formatted_history)
        return {'FINISHED'}