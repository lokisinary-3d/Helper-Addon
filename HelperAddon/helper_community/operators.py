# Path: helper_addon/operators.py

import bpy
from bpy.props import StringProperty, IntProperty
import requests
import json
from . import utils
from bpy.types import Operator, PropertyGroup
import traceback
from datetime import datetime
import threading  # For background threads

# Define the Report Functions
def report_error(message):
    def _set_error():
        addon_prefs = bpy.context.preferences.addons["HelperAddon"].preferences
        addon_prefs.status_message = f"Error: {message}"
        # Schedule the message to be cleared after 5 seconds
        bpy.app.timers.register(lambda: clear_status_message(addon_prefs), first_interval=5)
        return None
    bpy.app.timers.register(_set_error, first_interval=0)

def report_info(message):
    def _set_info():
        addon_prefs = bpy.context.preferences.addons["HelperAddon"].preferences
        addon_prefs.status_message = f"Info: {message}"
        # Schedule the message to be cleared after 5 seconds
        bpy.app.timers.register(lambda: clear_status_message(addon_prefs), first_interval=5)
        return None
    bpy.app.timers.register(_set_info, first_interval=0)

def clear_status_message(addon_prefs):
    addon_prefs.status_message = ""
    return None

def update_questions(context, questions_data):
    addon_prefs = context.preferences.addons["HelperAddon"].preferences
    addon_prefs.questions.clear()
    for q in questions_data:
        question = addon_prefs.questions.add()
        question.title = q.get('title', '')
        question.description = q.get('description', '')
        question.posted_by_username = q.get('postedByUserName', '')
        question.question_id = q.get('id', 0)
        # Parse the datetime to extract only the date
        posted_at_str = q.get('postedAt', '')
        try:
            dt = datetime.strptime(posted_at_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            formatted_date = dt.strftime("%Y-%m-%d")
        except ValueError:
            # If parsing fails, fallback to the original string
            formatted_date = posted_at_str.split('T')[0] if 'T' in posted_at_str else posted_at_str
        question.posted_at = formatted_date
    addon_prefs.is_fetching_questions = False
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)  # Force UI refresh
    bpy.ops.wm.save_userpref()  # Optional: Save preferences
    report_info(f"Fetched {len(questions_data)} questions.")

def update_answers(context, answers_data):
    addon_prefs = context.preferences.addons["HelperAddon"].preferences
    addon_prefs.answers.clear()
    for a in answers_data:
        answer = addon_prefs.answers.add()
        answer.answer_text = a.get('answerText', '')
        answer.posted_by_username = a.get('postedByUserName', '')
        answer.answer_id = a.get('id', 0)
        # Parse the datetime to extract only the date
        posted_at_str = a.get('postedAt', '')
        try:
            dt = datetime.strptime(posted_at_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            formatted_date = dt.strftime("%Y-%m-%d")
        except ValueError:
            # If parsing fails, fallback to the original string
            formatted_date = posted_at_str.split('T')[0] if 'T' in posted_at_str else posted_at_str
        answer.posted_at = formatted_date
    addon_prefs.is_fetching_answers = False
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)  # Force UI refresh
    bpy.ops.wm.save_userpref()  # Optional: Save preferences
    report_info(f"Fetched {len(answers_data)} answers.")

class QuestionItem(PropertyGroup):
    title: StringProperty(name="Title")
    description: StringProperty(name="Description")
    posted_by_username: StringProperty(name="Posted By")
    posted_at: StringProperty(name="Posted At")
    question_id: IntProperty(name="Question ID")  # To uniquely identify questions

class AnswerItem(PropertyGroup):
    answer_text: StringProperty(name="Answer Text")
    posted_by_username: StringProperty(name="Posted By")
    posted_at: StringProperty(name="Posted At")
    answer_id: IntProperty(name="Answer ID")  # To uniquely identify answers

class QuestionsUIList(bpy.types.UIList):
    """Custom UIList for displaying questions"""
    bl_idname = "UI_UL_QUESTIONS_LIST"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # 'data' is the RNA struct of the collection
        # 'item' is the current item
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.title, icon='QUESTION')
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon='QUESTION')

class RegisterOperator(Operator):
    bl_idname = "helper.register_operator"
    bl_label = "Register"

    email: StringProperty(name="Email")
    password: StringProperty(name="Password", subtype='PASSWORD')
    confirm_password: StringProperty(name="Confirm Password", subtype='PASSWORD')

    def execute(self, context):
        url = utils.get_api_base_url() + "/api/Account/register"
        data = {
            "email": self.email,
            "password": self.password,
            "confirmPassword": self.confirm_password
        }
        try:
            response = requests.post(url, json=data, verify=True)
            if response.status_code == 200 or response.status_code == 201:
                report_info("Registration successful!")
            else:
                try:
                    error_message = response.json().get('message', 'Registration failed.')
                except json.JSONDecodeError:
                    error_message = response.text
                report_error(f"Error {response.status_code}: {error_message}")
        except requests.exceptions.SSLError:
            report_error("SSL error occurred. Please check your SSL settings.")
        except Exception as e:
            report_error(f"Error: {e}")
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class LoginOperator(Operator):
    bl_idname = "helper.login_operator"
    bl_label = "Login"

    email: StringProperty(name="Email")
    password: StringProperty(name="Password", subtype='PASSWORD')

    def execute(self, context):
        url = utils.get_api_base_url() + "/api/Account/login"
        data = {
            "email": self.email,
            "password": self.password
        }
        try:
            response = requests.post(url, json=data, verify=True)
            response.raise_for_status()
            response_data = response.json()
            if response.status_code == 200:
                token = response_data.get('token') or response_data.get('Token')  # Handle both cases
                if token:
                    addon_prefs = context.preferences.addons["HelperAddon"].preferences
                    addon_prefs.token = token
                    addon_prefs.username = self.email
                    report_info("Login successful!")
                else:
                    report_error("Token not received.")
            else:
                error_message = response_data.get('message', 'Login failed.')
                report_error(error_message)
        except requests.exceptions.HTTPError as http_err:
            try:
                error_message = response.json().get('message', str(http_err))
            except:
                error_message = str(http_err)
            report_error(f"HTTP error occurred: {error_message}")
        except requests.exceptions.SSLError:
            report_error("SSL error occurred. Please check your SSL settings.")
        except Exception as e:
            report_error(f"Error: {e}")
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class LogoutOperator(Operator):
    bl_idname = "helper.logout_operator"
    bl_label = "Logout"

    def execute(self, context):
        addon_prefs = context.preferences.addons["HelperAddon"].preferences
        addon_prefs.token = ""
        addon_prefs.username = ""
        addon_prefs.active_question_index = 0
        addon_prefs.questions.clear()
        addon_prefs.answers.clear()
        bpy.ops.wm.save_userpref()  # Ensure preferences are saved
        report_info("Logged out successfully.")
        return {'FINISHED'}

class PostQuestionOperator(Operator):
    bl_idname = "helper.post_question_operator"
    bl_label = "Post Question"

    title: StringProperty(name="Title")
    description: StringProperty(name="Description", subtype='NONE', description="Description of the question")

    def execute(self, context):
        addon_prefs = context.preferences.addons["HelperAddon"].preferences
        token = addon_prefs.token

        if not token:
            report_error("You must be logged in to post a question.")
            return {'CANCELLED'}

        url = utils.get_api_base_url() + "/api/HelperAddonBlender/PostQuestion"
        data = {
            "title": self.title,
            "description": self.description
        }
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(url, json=data, headers=headers, verify=True)
            if response.status_code == 200:
                report_info("Question posted successfully!")
            else:
                try:
                    error_message = response.json().get('Message', 'Failed to post question.')
                except json.JSONDecodeError:
                    error_message = response.text
                report_error(f"Error {response.status_code}: {error_message}")
        except requests.exceptions.SSLError:
            report_error("SSL error occurred. Please check your SSL settings.")
        except Exception as e:
            report_error(f"Exception occurred: {e}")
            traceback.print_exc()
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class PostAnswerOperator(Operator):
    bl_idname = "helper.post_answer_operator"
    bl_label = "Post Answer"

    answer_text: StringProperty(name="Answer Text", description="Your answer to the question", subtype='NONE')

    def execute(self, context):
        addon_prefs = context.preferences.addons["HelperAddon"].preferences
        token = addon_prefs.token
        active_question_index = addon_prefs.active_question_index

        if not token:
            report_error("You must be logged in to post an answer.")
            return {'CANCELLED'}

        if active_question_index >= len(addon_prefs.questions):
            report_error("Selected question is invalid.")
            return {'CANCELLED'}

        selected_question = addon_prefs.questions[active_question_index]
        question_id = selected_question.question_id

        url = utils.get_api_base_url() + "/api/HelperAddonBlender/PostAnswer"
        data = {
            "questionId": question_id,
            "answerText": self.answer_text
        }
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(url, json=data, headers=headers, verify=True)
            if response.status_code == 200:
                # Optionally, you can fetch the answers again to update the UI
                addon_prefs.answers.clear()
                answer_data = response.json().get('Answer')
                if answer_data:
                    answer = addon_prefs.answers.add()
                    answer.answer_text = answer_data.get('answerText', '')
                    answer.posted_by_username = answer_data.get('postedByUserName', '')
                    # Format the date
                    posted_at_str = answer_data.get('postedAt', '')
                    try:
                        dt = datetime.strptime(posted_at_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                        formatted_date = dt.strftime("%Y-%m-%d")
                    except ValueError:
                        formatted_date = posted_at_str.split('T')[0] if 'T' in posted_at_str else posted_at_str
                    answer.posted_at = formatted_date
                    answer.answer_id = answer_data.get('id', 0)
                report_info("Answer posted successfully!")
            else:
                try:
                    error_message = response.json().get('Message', 'Failed to post answer.')
                except json.JSONDecodeError:
                    error_message = response.text
                report_error(f"Error {response.status_code}: {error_message}")
        except requests.exceptions.SSLError:
            report_error("SSL error occurred. Please check your SSL settings.")
        except Exception as e:
            report_error(f"Exception occurred: {e}")
            traceback.print_exc()
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class FetchQuestionsOperator(Operator):
    bl_idname = "helper.fetch_questions_operator"
    bl_label = "Show All Questions"

    def execute(self, context):
        addon_prefs = context.preferences.addons["HelperAddon"].preferences

        if addon_prefs.is_fetching_questions:
            report_info("Already fetching questions.")
            return {'CANCELLED'}

        addon_prefs.is_fetching_questions = True
        threading.Thread(target=self.fetch_questions, args=(context,), daemon=True).start()
        report_info("Fetching questions in the background...")
        return {'FINISHED'}

    def fetch_questions(self, context):
        addon_prefs = context.preferences.addons["HelperAddon"].preferences
        token = addon_prefs.token

        url = utils.get_api_base_url() + "/api/HelperAddonBlender/GetQuestions"
        headers = {
            "Accept": "application/json",
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            response = requests.get(url, headers=headers, verify=True)
            if response.status_code == 200:
                questions_data = response.json()
                # Schedule the update on the main thread
                bpy.app.timers.register(lambda: update_questions(context, questions_data), first_interval=0)
            else:
                try:
                    error_message = response.json().get('message', 'Failed to fetch questions.')
                except json.JSONDecodeError:
                    error_message = response.text
                # Schedule the error report on the main thread
                bpy.app.timers.register(lambda: report_error(f"Error {response.status_code}: {error_message}"), first_interval=0)
        except requests.exceptions.RequestException as e:
            # Handle generic request exceptions
            bpy.app.timers.register(lambda: report_error(f"Request error: {e}"), first_interval=0)
        finally:
            # Reset the flag regardless of success or failure
            bpy.app.timers.register(lambda: self.reset_fetch_flag(addon_prefs), first_interval=0)

    def reset_fetch_flag(self, addon_prefs):
        addon_prefs.is_fetching_questions = False
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)  # Force UI refresh

class FetchAnswersOperator(Operator):
    bl_idname = "helper.fetch_answers_operator"
    bl_label = "Fetch Answers"

    def execute(self, context):
        addon_prefs = context.preferences.addons["HelperAddon"].preferences

        if addon_prefs.is_fetching_answers:
            report_info("Already fetching answers.")
            return {'CANCELLED'}

        addon_prefs.is_fetching_answers = True
        threading.Thread(target=self.fetch_answers, args=(context,), daemon=True).start()
        report_info("Fetching answers in the background...")
        return {'FINISHED'}

    def fetch_answers(self, context):
        addon_prefs = context.preferences.addons["HelperAddon"].preferences
        token = addon_prefs.token
        active_question_index = addon_prefs.active_question_index

        if active_question_index >= len(addon_prefs.questions):
            bpy.app.timers.register(lambda: report_error("Selected question is invalid."), first_interval=0)
            return

        selected_question = addon_prefs.questions[active_question_index]
        question_id = selected_question.question_id

        url = utils.get_api_base_url() + f"/api/HelperAddonBlender/GetAnswersByQuestionId/{question_id}"
        headers = {
            "Accept": "application/json",
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            response = requests.get(url, headers=headers, verify=True)
            if response.status_code == 200:
                answers_data = response.json()
                # Schedule the update on the main thread
                bpy.app.timers.register(lambda: update_answers(context, answers_data), first_interval=0)
            else:
                try:
                    error_message = response.json().get('message', 'Failed to fetch answers.')
                except json.JSONDecodeError:
                    error_message = response.text
                # Schedule the error report on the main thread
                bpy.app.timers.register(lambda: report_error(f"Error {response.status_code}: {error_message}"), first_interval=0)
        except requests.exceptions.SSLError:
            bpy.app.timers.register(lambda: report_error("SSL error occurred. Please check your SSL settings."), first_interval=0)
        except Exception as e:
            bpy.app.timers.register(lambda: report_error(f"Error: {e}"), first_interval=0)
