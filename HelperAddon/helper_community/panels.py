# Path: helper_addon/panels.py

import bpy

class HELPER_PT_CommunityPanel(bpy.types.Panel):
    bl_label = "Helper Community"
    bl_idname = "HELPER_PT_community_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Helper'
    bl_order = 2 

    def draw(self, context):
        layout = self.layout
        addon_prefs = context.preferences.addons["HelperAddon"].preferences

        # Display Status Message if available
        if addon_prefs.status_message:
            # Use a box with a different background for visibility
            box = layout.box()
            if addon_prefs.status_message.startswith("Error:"):
                box.label(text=addon_prefs.status_message, icon='ERROR')
            else:
                box.label(text=addon_prefs.status_message, icon='INFO')

        # Authentication Section
        if addon_prefs.token:
            layout.label(text=f"Logged in as: {addon_prefs.username}")
            row = layout.row()
            row.operator("helper.logout_operator", text="Logout")
            layout.separator()
            row = layout.row()
            row.operator("helper.post_question_operator", text="Post Question")
        else:
            layout.operator("helper.register_operator", text="Register")
            layout.operator("helper.login_operator", text="Login")
        
        layout.separator()

        # "Show All Questions" button is always visible
        row = layout.row()
        row.enabled = not addon_prefs.is_fetching_questions  # Disable if fetching
        row.operator("helper.fetch_questions_operator", text="Show All Questions")
        if addon_prefs.is_fetching_questions:
            row = layout.row()
            row.label(text="Fetching...", icon='FILE_TICK')
        layout.separator()

        # Display the fetched questions using UIList
        if len(addon_prefs.questions) > 0:
            # Layout split for UIList and details
            split = layout.split(factor=0.3)
            col = split.column()
            col.template_list("UI_UL_QUESTIONS_LIST", "", addon_prefs, "questions", addon_prefs, "active_question_index", rows=4)

            # Retrieve the active question
            try:
                active_index = addon_prefs.active_question_index
                if active_index >= len(addon_prefs.questions):
                    active_index = 0
                    addon_prefs.active_question_index = active_index
                active_question = addon_prefs.questions[active_index]
            except IndexError:
                active_question = None

            # Display details of the active question and fetch answers functionality
            col = split.column()
            if active_question:
                box = col.box()
                box.label(text="Question Details:", icon='QUESTION')
                box.separator()
                box.label(text=f"Title: {active_question.title}", icon='VIEWZOOM')
                box.label(text=f"Description: {active_question.description}", icon='TEXT')
                box.label(text=f"Posted By: {active_question.posted_by_username}", icon='USER')
                box.label(text=f"Posted At: {active_question.posted_at}", icon='TIME')
                box.separator()
                
                # Post Answer Section - Only Visible if Logged In
                if addon_prefs.token:
                    box.separator()
                    box.label(text="Post an Answer:", icon='FILE_TICK')
                    row = box.row()
                    row.prop(context.window_manager, "helper_answer_text", text="Answer", icon='TEXT')
                    row = box.row()
                    row.operator("helper.post_answer_operator", text="Submit Answer")

                # Fetch Answers Section - Always Visible
                box.label(text="Fetch Answers:", icon='FILE_TICK')
                row = box.row()
                row.enabled = not addon_prefs.is_fetching_answers  # Disable if fetching
                row.operator("helper.fetch_answers_operator", text="Fetch Answers")
                if addon_prefs.is_fetching_answers:
                    row = box.row()
                    row.label(text="Fetching...", icon='FILE_TICK')
                
                # Display fetched answers
                if len(addon_prefs.answers) > 0:
                    box.separator()
                    box.label(text="Existing Answers:", icon='FILE_TICK')
                    for answer in addon_prefs.answers:
                        answer_box = box.box()
                        answer_box.label(text=f"Answer: {answer.answer_text}", icon='TEXT')
                        answer_box.label(text=f"Posted By: {answer.posted_by_username}", icon='USER')
                        answer_box.label(text=f"Posted At: {answer.posted_at}", icon='TIME')
                        answer_box.separator()
                else:
                    box.label(text="No answers fetched yet.", icon='INFO')

            else:
                col.label(text="Select a question to see details.", icon='INFO')
        else:
            layout.label(text="No questions fetched. Click 'Show All Questions' to retrieve them.")
