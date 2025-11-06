#online_resources.py

import bpy
import webbrowser
from . import search_shared_data  # Import the shared data module



class OBJECT_OT_StackExchangeSearchOperator(bpy.types.Operator):
    bl_idname = "object.stack_exchange_search"
    bl_label = "Search on Blender Stack Exchange"
    bl_description = "Perform a search on Blender Stack Exchange"
    
    def execute(self, context):
        search_text = context.scene.online_search_text.strip()
        if search_text:
            search_query = f"https://blender.stackexchange.com/search?q={search_text.replace(' ', '+')}"
            resource_name = "Blender Stack Exchange"
            # Append the searched text to shared search history
            search_shared_data.add_search_history(search_text, search_query, resource_name)
            
            # Update the search history property in the scene
            context.scene.search_history = search_text
        else:
            search_query = "https://blender.stackexchange.com"
        
        try:
            webbrowser.open_new_tab(search_query)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")
            return {'CANCELLED'}

class OBJECT_OT_BlenderStudioOperator(bpy.types.Operator):
    bl_idname = "object.blender_studio_search"
    bl_label = "Search on Blender Studio"
    bl_description = "Perform a search on Blender Studio"

    def execute(self, context):
        search_text = context.scene.online_search_text.strip()
        if search_text:
            search_query = search_text.replace(" ", "+")
            search_query = f"https://studio.blender.org/search/?query={search_query}"
            resource_name = "Blender Studio"
            # Append the searched text to shared search history
            search_shared_data.add_search_history(search_text, search_query, resource_name)
            
            # Update the search history property in the scene
            context.scene.search_history = search_text
        else:
            search_query = "https://studio.blender.org/search/"
        
        try:
            webbrowser.open_new_tab(search_query)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")
            return {'CANCELLED'}


class OBJECT_OT_SketchfabOperator(bpy.types.Operator):
    bl_idname = "object.sketchfab_search"
    bl_label = "Search on Sketchfab"
    bl_description = "Perform a search on Sketchfab"
    
    def execute(self, context):
        search_text = context.scene.online_search_text.strip()
        if search_text:
            search_query = search_text.replace(" ", "+")
            search_query = f"https://sketchfab.com/search?q={search_query}&type=models"
            resource_name = "Sketchfab"
            # Append the searched text to shared search history
            search_shared_data.add_search_history(search_text, search_query, resource_name)
            
            # Update the search history property in the scene
            context.scene.search_history = search_text
        else:
            search_query = "https://sketchfab.com"
        
        try:
            webbrowser.open_new_tab(search_query)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")
            return {'CANCELLED'}


class OBJECT_OT_BlenderMarketOperator(bpy.types.Operator):
    bl_idname = "object.blender_market_search"
    bl_label = "Search on Blender Market"
    bl_description = "Perform a search on Blender Market"
    
    def execute(self, context):
        search_text = context.scene.online_search_text.strip()
        if search_text:
            search_query = f"https://blendermarket.com/search?utf8=✓&search%5Bq%5D={search_text.replace(' ', '+')}&button="
            resource_name = "Blender Market"
            # Append the searched text to shared search history
            search_shared_data.add_search_history(search_text, search_query, resource_name)
            
            # Update the search history property in the scene
            context.scene.search_history = search_text
        else:
            search_query = "https://blendermarket.com"
        
        try:
            webbrowser.open_new_tab(search_query)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")
            return {'CANCELLED'}

class OBJECT_OT_BlenderKitOperator(bpy.types.Operator):
    bl_idname = "object.blenderkit_search"
    bl_label = "Search on BlenderKit"
    bl_description = "Perform a search on BlenderKit"
    
    def execute(self, context):
        search_text = context.scene.online_search_text.strip()
        if search_text:
            search_query = f"https://www.blenderkit.com/asset-gallery?query={search_text.replace(' ', '+')}"
            resource_name = "Blenderkit"
            # Append the searched text to shared search history
            search_shared_data.add_search_history(search_text, search_query, resource_name)
            
            # Update the search history property in the scene
            context.scene.search_history = search_text
        else:
            search_query = "https://www.blenderkit.com"
        
        try:
            webbrowser.open_new_tab(search_query)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")
            return {'CANCELLED'}


class OBJECT_OT_PoliigonOperator(bpy.types.Operator):
    bl_idname = "object.poliigon_search"
    bl_label = "Search on Poliigon"
    bl_description = "Perform a search on Poliigon"
    
    def execute(self, context):
        search_text = context.scene.online_search_text.strip()
        if search_text:
            search_query = f"https://www.poliigon.com/search/{search_text.replace(' ', '-')}"
            resource_name = "Poliigon"
            # Append the searched text to shared search history
            search_shared_data.add_search_history(search_text, search_query, resource_name)
            
            # Update the search history property in the scene
            context.scene.search_history = search_text
        else:
            search_query = "https://www.poliigon.com"
        
        try:
            webbrowser.open_new_tab(search_query)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")
            return {'CANCELLED'}


class OBJECT_OT_QuixelMegascansOperator(bpy.types.Operator):
    bl_idname = "object.quixel_megascans_search"
    bl_label = "Search on Quixel Megascans"
    bl_description = "Perform a search on Quixel Megascans"
    
    def execute(self, context):
        search_text = context.scene.online_search_text.strip()
        if search_text:
            search_query = f"https://quixel.com/megascans/home?search={search_text.replace(' ', '+')}"
            resource_name = "Quixel Megascans"
            # Append the searched text to shared search history
            search_shared_data.add_search_history(search_text, search_query, resource_name)
            
            # Update the search history property in the scene
            context.scene.search_history = search_text
        else:
            search_query = "https://quixel.com"
        
        try:
            webbrowser.open_new_tab(search_query)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")
            return {'CANCELLED'}

class OBJECT_OT_KitBash3DOperator(bpy.types.Operator):
    bl_idname = "object.kitbash3d_search"
    bl_label = "Search on KitBash3D"
    bl_description = "Perform a search on KitBash3D (Use precise words for accurate results)"
    
    def execute(self, context):
        search_text = context.scene.online_search_text.strip()
        if search_text:
            search_query = f"https://kitbash3d.com/products/{search_text.replace(' ', '-')}?_pos=2&_psq={search_text.replace(' ', '+')}&_ss=e&_v=1.0"
            resource_name = "KitBash3D"
            # Append the searched text to shared search history
            search_shared_data.add_search_history(search_text, search_query, resource_name)
            
            # Update the search history property in the scene
            context.scene.search_history = search_text
        else:
            search_query = "https://kitbash3d.com"
        
        try:
            webbrowser.open_new_tab(search_query)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")
            return {'CANCELLED'}
        
class OBJECT_OT_GitHubOperator(bpy.types.Operator):
    bl_idname = "object.github_search"
    bl_label = "Search on GitHub"
    bl_description = "Perform a search on GitHub"
    
    def execute(self, context):
        search_text = context.scene.online_search_text.strip()
        if search_text:
            search_query = f"https://github.com/search?q={search_text.replace(' ', '+')}"
            resource_name = "GitHub"
            # Append the searched text to shared search history
            search_shared_data.add_search_history(search_text, search_query, resource_name)
            
            # Update the search history property in the scene
            context.scene.search_history = search_text
        else:
            search_query = "https://github.com"
        
        try:
            webbrowser.open_new_tab(search_query)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")
            return {'CANCELLED'}

class OBJECT_OT_BlenderCommunityTodayOperator(bpy.types.Operator):
    bl_idname = "object.blender_community_today_search"
    bl_label = "Search on Blender Community Today"
    bl_description = "Perform a search on Blender Community Today"

    def execute(self, context):
        search_text = context.scene.online_search_text.strip()
        if search_text:
            search_query = f"https://blender.community/c/today/?sorting=hot&page=1&text={search_text.replace(' ', '+')}"
            resource_name = "Blender Community Today"
            # Append the searched text to shared search history
            search_shared_data.add_search_history(search_text, search_query, resource_name)
            
            # Update the search history property in the scene
            context.scene.search_history = search_text
        else:
            search_query = "https://blender.community/c/today"
        
        try:
            webbrowser.open_new_tab(search_query)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")
            return {'CANCELLED'}

class OBJECT_OT_BlenderCommunityRightClickOperator(bpy.types.Operator):
    bl_idname = "object.blender_community_right_click_search"
    bl_label = "Search on Blender Community Right Click Select"
    bl_description = "Perform a search on Blender Community Right Click Select"

    def execute(self, context):
        search_text = context.scene.online_search_text.strip()
        if search_text:
            search_query = f"https://blender.community/c/rightclickselect/?sorting=hot&page=1&text={search_text.replace(' ', '+')}"
            resource_name = "Blender Community Right Click"
            # Append the searched text to shared search history
            search_shared_data.add_search_history(search_text, search_query, resource_name)
            
            # Update the search history property in the scene
            context.scene.search_history = search_text
        else:
            search_query = "https://blender.community/c/rightclickselect"
        
        try:
            webbrowser.open_new_tab(search_query)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")
            return {'CANCELLED'}


class OBJECT_OT_PolyHavenOperator(bpy.types.Operator):
    bl_idname = "object.polyhaven_search"
    bl_label = "Search on Poly Haven"
    bl_description = "Perform a search on Poly Haven (Use precise words for accurate results)"

    def execute(self, context):
        search_text = context.scene.online_search_text.strip().lower()
        if search_text:
            search_query = search_text.replace(" ", "_")
            search_query = f"https://polyhaven.com/a/{search_query}"
            resource_name = "Poly Haven"
            # Append the searched text to shared search history
            search_shared_data.add_search_history(search_text, search_query, resource_name)
            
            # Update the search history property in the scene
            context.scene.search_history = search_text
        else:
            search_query = "https://polyhaven.com"
        
        try:
            webbrowser.open_new_tab(search_query)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")
            return {'CANCELLED'}


class OBJECT_OT_BlenderManualOperator(bpy.types.Operator):
    bl_idname = "object.blender_manual_search"
    bl_label = "Search in Blender Manual"
    bl_description = "Perform a search in the Blender Manual"

    def execute(self, context):
        search_text = context.scene.online_search_text.strip()
        if search_text:
            search_query = f"https://docs.blender.org/manual/en/4.1/search.html?q={search_text}&check_keywords=yes&area=default"
            resource_name = "Blender Manual"
            # Append the searched text to shared search history
            search_shared_data.add_search_history(search_text, search_query, resource_name)
            
            # Update the search history property in the scene
            context.scene.search_history = search_text
        else:
            search_query = "https://docs.blender.org/manual/en/4.1/"
        
        try:
            webbrowser.open_new_tab(search_query)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")
            return {'CANCELLED'}