#blender_manual.py

import bpy
import os
import webbrowser
import platform

from .object_recognize import recognize_selected_object

class OBJECT_OT_ObjectRecognizedOfflineSearchOperator(bpy.types.Operator):
    bl_idname = "object.object_recognized_offline_search"
    bl_label = "Offline Search"
    bl_description = "Perform an offline search for the recognized object in Blender Manual"

    def execute(self, context):
        recognized_object = recognize_selected_object()
        if "No object selected" in recognized_object:
            self.report({'WARNING'}, "No object selected. Please select an object.")
            return {'CANCELLED'}

        recognized_object_name = recognized_object.replace("Recognized object: ", "")
        search_term = recognized_object_name.lower().replace(" ", "_")

        blender_manual_path = os.path.join(os.path.dirname(__file__), "blender_manual")

        search_result_number = context.scene.offline_search_result_number

        matching_files = []
        matching_images = []

        # Get a list of all matching files and images
        for root, dirs, files in os.walk(blender_manual_path):
            for file in files:
                if search_term in file.lower():
                    if file.lower().endswith(('.html', '.htm', '.txt')):
                        matching_files.append(os.path.join(root, file))
                    elif file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                        matching_images.append(os.path.join(root, file))

        total_results = len(matching_files) + len(matching_images)

        if not matching_files and not matching_images:
            self.report({'WARNING'}, f"No offline documentation or images found for '{recognized_object_name}'.")
            return {'CANCELLED'}

        if search_result_number <= 0 or search_result_number > total_results:
            self.report({'WARNING'}, "Invalid search result number.")
            return {'CANCELLED'}

        if search_result_number <= len(matching_files):
            file_to_open = matching_files[search_result_number - 1]
            try:
                with open(file_to_open, "r", encoding="utf-8") as html_file:
                    content = html_file.read()
                    webbrowser.open_new_tab(f"file://{file_to_open}")
            except UnicodeDecodeError:
                self.report({'ERROR'}, "An error occurred while opening the file. Unable to decode file content.")
            except Exception as e:
                self.report({'ERROR'}, f"An error occurred: {e}")
            self.report({'INFO'}, f"Opening result {search_result_number} of {total_results} results.")
        else:
            image_to_open = matching_images[search_result_number - len(matching_files) - 1]
            if platform.system() == "Darwin":  # macOS
                os.system(f"open '{image_to_open}'")
            elif platform.system() == "Linux":
                os.system(f"xdg-open '{image_to_open}'")
            elif platform.system() == "Windows":
                os.system(f'start "" "{image_to_open}"')
            self.report({'INFO'}, f"Opening image result {search_result_number - len(matching_files)} of {len(matching_images)} image results.")

        context.scene.offline_search_total_results = total_results
        return {'FINISHED'}

class OBJECT_OT_TextBlenderManualOperator(bpy.types.Operator):
    bl_idname = "object.text_blender_manual"
    bl_label = "Text Blender Manual Search"
    bl_description = "Perform a text search in Blender Manual based on the entered text"

    def execute(self, context):
        custom_text = context.scene.custom_text_blender_manual.strip()
        if not custom_text:
            self.report({'WARNING'}, "No search text provided.")
            return {'CANCELLED'}

        keywords = custom_text.lower().split()  # Split keywords

        blender_manual_path = os.path.join(os.path.dirname(__file__), "blender_manual")

        matching_files = []

        # Get a list of all matching files
        for root, dirs, files in os.walk(blender_manual_path):
            for file in files:
                file_lower = file.lower()
                if all(keyword in file_lower for keyword in keywords):
                    matching_files.append(os.path.join(root, file))

        total_results = len(matching_files)

        if not matching_files:
            self.report({'WARNING'}, f"No offline documentation found for '{custom_text}'.")
            return {'CANCELLED'}

        context.scene.text_blender_manual_total_results = total_results  # Store the total results

        search_result_number = context.scene.text_blender_manual_search_result_number

        if search_result_number <= 0 or search_result_number > total_results:
            self.report({'WARNING'}, "Invalid search result number.")
            return {'CANCELLED'}

        file_to_open = matching_files[search_result_number - 1]

        try:
            if file_to_open.lower().endswith(('.html', '.htm', '.txt')):
                with open(file_to_open, "r", encoding="utf-8") as html_file:
                    content = html_file.read()
                    webbrowser.open_new_tab(f"file://{file_to_open}")
            else:
                platform_system = platform.system()
                if platform_system == "Darwin":  # macOS
                    os.system(f"open '{file_to_open}'")
                elif platform_system == "Linux":
                    os.system(f"xdg-open '{file_to_open}'")
                elif platform_system == "Windows":
                    os.system(f'start "" "{file_to_open}"')
        except UnicodeDecodeError:
            self.report({'ERROR'}, "An error occurred while opening the file. Unable to decode file content.")
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {e}")

        self.report({'INFO'}, f"Opening result {search_result_number} of {total_results} results.")
        return {'FINISHED'}