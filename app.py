import threading
import os
import dearpygui.dearpygui as dpg
from client import multithreaded_download, list_files, download_file

selected_files = set()

# log error messages to the GUI
def log(msg):
    dpg.add_text(msg, parent="download_window")

# Toggle checkbox state and update selected files
def toggle_file_checkbox(sender, app_data, user_data):
    if app_data:
        selected_files.add(user_data)
    else:
        selected_files.discard(user_data)

# Render the directory tree recursively
def render_directory_tree(tree, parent):
    for item in tree:
        name = item["name"]
        if item["type"] == "folder":
            with dpg.tree_node(label=f"{name}", parent=parent, default_open=False) as folder_node:
                dpg.bind_item_font(folder_node, filename)
                dpg.bind_item_theme(folder_node, tree_node_theme)
                render_directory_tree(item["children"], folder_node)
        elif item["type"] == "file":
            checkbox_id = dpg.add_checkbox(
                label=f"{name}",
                parent=parent,
                callback=toggle_file_checkbox,
                user_data=item["path"]
            )
            dpg.bind_item_font(checkbox_id, filename)
            dpg.bind_item_theme(checkbox_id, text_black_theme)

# Fetch the directory tree from the server and render it in the GUI
def fetch_directory_tree():
    try:
        # call backend to get the directory structure from the server
        data = list_files()

        # display the directory structure in the GUI
        dpg.delete_item("file_tree_panel", children_only=True)
        render_directory_tree(data, "file_tree_panel")
    except Exception as e:
        log(f"❌ Failed to load tree: {e}")

# Download a file from the server and update the GUI with progress
def download_file_ui(filename):
    try:
        progress_id = dpg.generate_uuid()
        text_id = dpg.generate_uuid()

        # add text, bind font and theme
        dpg.add_text(f"Downloading: {os.path.basename(filename)}", 
                     parent="download_window", tag=text_id)
        dpg.bind_item_font(text_id, filename)
        dpg.bind_item_theme(text_id, text_black_theme)

        # add progress bar
        dpg.add_progress_bar(tag=progress_id, parent="download_window", width=700, overlay="0%")

        # update progress function
        # called by the backend function to update the progress bar
        def update_progress(p):
            dpg.set_value(progress_id, p)
            dpg.configure_item(progress_id, overlay=f"{int(p * 100)}%")

        # call backend to download
        success, result = download_file(filename, progress_callback=update_progress)

        if success:
            dpg.set_value(text_id, f"Downloaded: {os.path.basename(filename)}")
        else:
            log(f"❌ {filename}: {result}")

    except Exception as e:
        log(f"❌ {filename}: {e}")

# Start the download process for selected files
def start_download():
    if not selected_files:
        log("⚠ No file selected.")
        return
    for file_path in selected_files:
        threading.Thread(target=download_file_ui, args=(file_path,), daemon=True).start()

# GUI setup
dpg.create_context()

with dpg.theme() as tree_node_theme:
    with dpg.theme_component(dpg.mvTreeNode):
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255)) 

with dpg.theme() as text_black_theme:
    with dpg.theme_component(dpg.mvCheckbox): 
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255)) 
    with dpg.theme_component(dpg.mvText): 
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255)) 

with dpg.texture_registry():
    width, height, channels, data = dpg.load_image("Element/bg.png")
    texture_id = dpg.add_static_texture(width, height, data)
    width1, height1, channels1, data1 = dpg.load_image("Element/downbtn.png")
    downbtn = dpg.add_static_texture(width1, height1, data1)
    width2, height2, channels2, data2 = dpg.load_image("Element/refreshbtn.png")
    refreshbtn = dpg.add_static_texture(width2, height2, data2)


main_window_width = 1778
main_window_height = 1000

with dpg.theme() as child_window_theme:
    with dpg.theme_component(dpg.mvChildWindow):
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (100,102,155,0))  
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (100, 100, 150, 0))  
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (150, 150, 200, 255))  

with dpg.font_registry():
    filename = dpg.add_font("Font/LithosPro-Black.otf",20)


with dpg.theme() as theme_button_back:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 0, 0))       
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0)   

with dpg.window(label="📦 File Downloader", width=main_window_width, height=main_window_height, tag="main_window"):
    dpg.add_image(texture_id)
    
    down_button = dpg.add_image_button(texture_tag=downbtn, pos=(840,330), width=60, height=60, 
                        frame_padding=0,
                        background_color=(0, 0, 0, 0),
                        callback=start_download)
    dpg.bind_item_theme(down_button, theme_button_back)

    refresh_btn = dpg.add_image_button(texture_tag=refreshbtn, pos=(910,330), width=60, height=60, 
                            frame_padding=0,
                            background_color=(0, 0, 0, 0),
                            callback=fetch_directory_tree)

    dpg.bind_item_theme(refresh_btn, theme_button_back)
    dpg.add_spacer(height=5)
    dpg.add_child_window(tag="file_tree_panel", width=800, height=175, pos=(105,160), border=False)
    dpg.bind_item_theme("file_tree_panel", child_window_theme)

    dpg.add_child_window(tag="download_window", width=800, height=125, pos=(105,410), border=False)
    dpg.bind_item_theme("download_window", child_window_theme)

dpg.create_viewport(title="Socket File Downloader", width=1030, height=640)
dpg.setup_dearpygui()
dpg.show_viewport()

# Fetch the initial directory tree
fetch_directory_tree()

dpg.start_dearpygui()
dpg.destroy_context()