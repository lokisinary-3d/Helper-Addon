# __init__.py

bl_info = {
    "name": "Helper Addon",
    "author": "lokisinary",
    "version": (1, 4),
    "blender": (2, 89, 0),
    "location": "View3D > Sidebar > Helper Panel",
    "description": "A helpful add-on for object recognition, web searches and community engagement in Blender.",
    "category": "Object",
    "doc_url": "https://github.com/lokisinary3d/Helper-Addon/blob/main/README.md",  # Documentation URL
    "website_url": "https://sinary.org/",  # Official Website
}
version = bl_info["version"]

import bpy
from bpy.props import BoolProperty, IntProperty, StringProperty, CollectionProperty
from bpy.types import AddonPreferences
from .ui import HelperPanel
from .recognized_web_search import OBJECT_OT_WebSearchOperator, OBJECT_OT_YouTubeSearchOperator
from .text_web_search import OBJECT_OT_TextWebSearchOperator, OBJECT_OT_YouTubeTextWebSearchOperator
from .blender_manual import OBJECT_OT_ObjectRecognizedOfflineSearchOperator, OBJECT_OT_TextBlenderManualOperator
from .online_resources import (
    OBJECT_OT_BlenderKitOperator,
    OBJECT_OT_BlenderMarketOperator,
    OBJECT_OT_SketchfabOperator,
    OBJECT_OT_StackExchangeSearchOperator,
    OBJECT_OT_BlenderStudioOperator,
    OBJECT_OT_PoliigonOperator,
    OBJECT_OT_QuixelMegascansOperator,
    OBJECT_OT_KitBash3DOperator,
    OBJECT_OT_GitHubOperator,
    OBJECT_OT_BlenderCommunityTodayOperator,
    OBJECT_OT_BlenderCommunityRightClickOperator,
    OBJECT_OT_BlenderManualOperator,
    OBJECT_OT_PolyHavenOperator,
)
from .online_resources_panel import OnlineResourcesPanel, CopyWebsiteNameOperator, ShowSearchHistoryInfoOperator
from .addons_panel import HelperAddonsPanel
from .readme import OBJECT_OT_DisplayReadmeOperator  # Import the operator from readme.py
from .license import OBJECT_OT_DisplayLicenseOperator
from .privacy_policy import OBJECT_OT_DisplayPrivacyPolicyOperator
from .terms_and_conditions import OBJECT_OT_DisplayTermsAndConditionsOperator

# Import community engagement functionality
from .helper_community import operators, panels

# Add-on Preferences for Community Engagement
class HelperAddonPreferences(AddonPreferences):
    bl_idname = "HelperAddon"

    # Property for collapsible preferences
    show_preferences: BoolProperty(
        name="Show Preferences",
        description="Expand or collapse the preferences section",
        default=True
    )

    token: StringProperty(
        name="Token",
        description="JWT token for API authentication",
        default="",
        options={'HIDDEN'},
    )

    username: StringProperty(
        name="Username",
        description="Username of the logged-in user",
        default="",
    )

    status_message: StringProperty(
        name="Status Message",
        description="Latest status message to display",
        default="",
    )

    questions: CollectionProperty(
        name="Questions",
        type=operators.QuestionItem
    )

    active_question_index: IntProperty(
        name="Active Question Index",
        description="Index of the currently selected question",
        default=0
    )

    answers: CollectionProperty(
        name="Answers",
        type=operators.AnswerItem
    )

    active_answer_index: IntProperty(
        name="Active Answer Index",
        description="Index of the currently selected answer",
        default=0
    )

    is_fetching_questions: BoolProperty(
        name="Is Fetching Questions",
        description="Indicates whether questions are currently being fetched",
        default=False
    )

    is_fetching_answers: BoolProperty(
        name="Is Fetching Answers",
        description="Indicates whether answers are currently being fetched",
        default=False
    )

    def draw(self, context):
        layout = self.layout

        # Collapsible preferences section
        row = layout.row()
        row.prop(self, "show_preferences", icon="TRIA_DOWN" if self.show_preferences else "TRIA_RIGHT", emboss=False)

        if self.show_preferences:
            # Add-on Information
            layout.label(text="Helper Addon Preferences", icon='PREFERENCES')

            # Documentation URL
            doc_url = bl_info.get("doc_url")
            if doc_url:
                layout.operator("wm.url_open", text="GitHub", icon="HELP").url = doc_url

            # Website URL
            website_url = bl_info.get("website_url")
            if website_url:
                layout.operator("wm.url_open", text="Visit Website", icon="URL").url = website_url

            # Username Field
            layout.prop(self, "username", text="Username")

# Register all classes
general_classes = (
    HelperPanel,
    OnlineResourcesPanel,
    HelperAddonsPanel,
    OBJECT_OT_TextWebSearchOperator,
    OBJECT_OT_YouTubeTextWebSearchOperator,
    OBJECT_OT_WebSearchOperator,
    OBJECT_OT_YouTubeSearchOperator,
    OBJECT_OT_ObjectRecognizedOfflineSearchOperator,
    OBJECT_OT_TextBlenderManualOperator,
    OBJECT_OT_StackExchangeSearchOperator,
    OBJECT_OT_BlenderStudioOperator,
    OBJECT_OT_SketchfabOperator,
    OBJECT_OT_BlenderMarketOperator,
    OBJECT_OT_BlenderKitOperator,
    OBJECT_OT_PoliigonOperator,
    OBJECT_OT_QuixelMegascansOperator,
    OBJECT_OT_KitBash3DOperator,
    OBJECT_OT_GitHubOperator,
    OBJECT_OT_BlenderCommunityTodayOperator,
    OBJECT_OT_BlenderCommunityRightClickOperator,
    OBJECT_OT_BlenderManualOperator,
    OBJECT_OT_PolyHavenOperator,
    OBJECT_OT_DisplayReadmeOperator,  # Add the imported operator to the classes tuple
    OBJECT_OT_DisplayLicenseOperator,
    OBJECT_OT_DisplayPrivacyPolicyOperator,
    OBJECT_OT_DisplayTermsAndConditionsOperator,
)

community_classes = (
    operators.QuestionItem,
    operators.AnswerItem,
    operators.FetchQuestionsOperator,
    operators.FetchAnswersOperator,
    operators.PostAnswerOperator,
    operators.RegisterOperator,
    operators.LoginOperator,
    operators.LogoutOperator,
    operators.PostQuestionOperator,
    operators.QuestionsUIList,
    panels.HELPER_PT_CommunityPanel,
    HelperAddonPreferences,
)

def register():
    # Register General Functionality
    for cls in general_classes:
        bpy.utils.register_class(cls)

    # Register Community Engagement
    for cls in community_classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.google_access_token = bpy.props.StringProperty()
    bpy.types.Scene.google_access_token = bpy.props.StringProperty()  # Register google_access_token here
    bpy.types.Scene.google_email = bpy.props.StringProperty(name="Google Email")
    bpy.types.Scene.google_password = bpy.props.StringProperty(name="Google Password")
    bpy.types.Scene.custom_search_text = bpy.props.StringProperty(name="Custom Search Text")
    bpy.types.Scene.offline_search_result_number = bpy.props.IntProperty(name="SN", default=1, min=1, description="Enter the result number to open")
    bpy.types.Scene.offline_search_total_results = bpy.props.IntProperty(name="Offline Search Total Results", default=0, min=0, description="Total number of results found")
    bpy.types.Scene.show_blender_manual = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.show_text_blender_manual = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.custom_text_blender_manual = bpy.props.StringProperty(name="Custom Text Blender Manual", default="")
    bpy.types.Scene.text_blender_manual_search_result_number = bpy.props.IntProperty(name="Search Result Number", default=1, min=1, description="Enter the search result number")
    bpy.types.Scene.text_blender_manual_total_results = bpy.props.IntProperty(name="Text Blender Manual Total Results", default=0, min=0, description="Total number of results found")
    bpy.types.Scene.online_search_type = bpy.props.EnumProperty(
        items=[
            ('blender_market', 'Blender Market', 'Search on Blender Market'),
            ('polyhaven', 'Poly Haven', 'Search on Poly Haven'),
            ('sketchfab', 'Sketchfab', 'Search on Sketchfab'),
            ('quixel_megascans', 'Quixel Megascans', 'Search on Quixel Megascans'),
            ('blender_studio', 'Blender Studio', 'Search on Blender Studio'),
            ('blenderkit', 'BlenderKit', 'Search on BlenderKit'),
            ('poliigon', 'Poliigon', 'Search on Poliigon'),
            ('kitbash3d', 'KitBash3D', 'Search on KitBash3D'),
            ('blender_community_today', 'Blender Community Today', 'Search on Blender Community Today'),
            ('stack_exchange', 'Blender Stack Exchange', 'Search on Blender Stack Exchange'),
            ('blender_community_right_click', 'Blender Community Right Click Select', 'Search on Blender Community Right Click Select'),
            ('github', 'GitHub', 'Search on GitHub'),
            ('blender_manual', 'Blender Manual', 'Search on Blender Manual'),
        ],
        name="Search Type",
        default='blender_market'
    )
    bpy.types.Scene.online_search_text = bpy.props.StringProperty(name="Online Search Text", default="")
    bpy.types.Scene.search_history = bpy.props.StringProperty()  # Register the search_history property in the scene
    bpy.utils.register_class(CopyWebsiteNameOperator)
    # Add the show_search_history property to the scene
    bpy.types.Scene.show_search_history = bpy.props.BoolProperty(
        name="Show Search History",
        default=True,  # Set the default value to True to initially show the search history
    )
    bpy.utils.register_class(ShowSearchHistoryInfoOperator)
    bpy.types.Scene.show_enabled_addons = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.show_info = bpy.props.BoolProperty(default=True)


def unregister():
    # Unregister General Functionality
    for cls in reversed(general_classes):
        bpy.utils.unregister_class(cls)

    # Unregister Community Engagement
    for cls in reversed(community_classes):
        bpy.utils.unregister_class(cls)

    # Remove Custom Properties
    del bpy.types.Scene.google_access_token  # Delete the google_access_token property
    del bpy.types.Scene.custom_search_text
    del bpy.types.Scene.offline_search_result_number
    del bpy.types.Scene.offline_search_total_results
    del bpy.types.Scene.show_blender_manual
    del bpy.types.Scene.show_text_blender_manual
    del bpy.types.Scene.custom_text_blender_manual
    del bpy.types.Scene.text_blender_manual_search_result_number
    del bpy.types.Scene.text_blender_manual_total_results
    del bpy.types.Scene.online_search_type
    del bpy.types.Scene.online_search_text
    del bpy.types.Scene.search_history  # Remove the search_history property from the scene
    bpy.utils.unregister_class(ShowSearchHistoryInfoOperator)


if __name__ == "__main__":
    register()