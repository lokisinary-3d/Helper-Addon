#ui.py

import bpy
from .object_recognize import recognize_selected_object

class HelperPanel(bpy.types.Panel):
    bl_label = "Helper Panel"
    bl_idname = "HELPER_PT_helper_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Helper'
    bl_description = "A collection of tools to assist with object recognition and web searches in Blender"
    bl_order = 0

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        recognized_object = recognize_selected_object()
        if recognized_object:
            box.label(text=recognized_object)
            row = box.row(align=True)
            row.operator("object.web_search", text="Google")
            row.operator("object.youtube_search", text="YouTube")

            blender_manual_box = box.box()
            row = blender_manual_box.row(align=True)
            row.prop(context.scene, "show_blender_manual", icon="TRIA_DOWN" if context.scene.show_blender_manual else "TRIA_RIGHT", icon_only=True, emboss=False)
            row.label(text="Blender Manual RO")
            if context.scene.show_blender_manual:
                offline_search_row = blender_manual_box.row(align=True)
                offline_search_row.operator("object.object_recognized_offline_search", text="Offline Search")
                
                offline_search_results_row = blender_manual_box.row(align=True)
                offline_search_results_row.prop(context.scene, "offline_search_result_number", text="SN")
                offline_search_results_row.label(text=f"of {context.scene.offline_search_total_results} results")

        else:
            box.label(text="No object selected")
            box.operator("object.web_search", text="Google Search")

        text_box = layout.box()
        text_box.label(text="Text Web Search:")
        custom_search_row = text_box.row(align=True)
        custom_search_row.prop(context.scene, "custom_search_text", text="", emboss=True, icon='VIEWZOOM')
        text_search_row = text_box.row(align=True)
        text_search_row.operator("object.text_web_search", text="Google").search_engine = 'google'
        text_search_row.operator("object.youtube_text_web_search", text="YouTube").search_engine = 'youtube'

        text_blender_manual_box = text_box.box()
        row = text_blender_manual_box.row(align=True)
        row.prop(context.scene, "show_text_blender_manual", icon="TRIA_DOWN" if context.scene.show_text_blender_manual else "TRIA_RIGHT", icon_only=True, emboss=False)
        row.label(text="Blender Manual Text")
        if context.scene.show_text_blender_manual:
            text_search_row = text_blender_manual_box.row(align=True)
            text_search_row.prop(context.scene, "custom_text_blender_manual", text="", emboss=True, icon='VIEWZOOM')

            search_button_row = text_blender_manual_box.row(align=True)
            search_button_row.operator("object.text_blender_manual", text="Offline Search")
            
            result_number_row = text_blender_manual_box.row(align=True)
            result_number_row.prop(context.scene, "text_blender_manual_search_result_number", text="SN")
            result_number_row.label(text=f"of {context.scene.text_blender_manual_total_results} results")
