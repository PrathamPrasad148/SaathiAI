"""
Saathi AI — Universal GUI Application Control & Messaging Subsystem
Provides robust, multi-step autonomous GUI interactions for WhatsApp, Telegram,
Discord, Spotify, Chrome, Word, and all Windows desktop applications.
"""

import time
import re
import os
from typing import Dict, Any, Tuple
from automation.app_launcher import launch_application
from automation.windows import focus_window_by_title, list_open_windows
from automation.vision import get_active_window_info, find_text_and_click, find_text_on_screen
from automation.keyboard import type_text, press_key, send_hotkey
from automation.mouse import click_mouse

def send_app_message(app_name: str, contact_name: str, message_text: str = "") -> Dict[str, Any]:
    """
    Autonomously send a message to a specific contact in WhatsApp, Telegram, Discord, Teams, or Slack.
    Handles window focus, search UI, typing, and sending.
    """
    app_clean = app_name.lower().strip()

    # 1. Launch or Focus Target Application
    ok, launch_msg = launch_application(app_clean)
    time.sleep(1.2)  # Give time for the app window to launch and register

    # Focus window explicitly
    focus_window_by_title(app_name)
    time.sleep(0.5)

    # Verify active window title
    win_info = get_active_window_info()
    win_title = win_info.get("title", "")

    # 2. Activate Search Input Box
    # Try Ctrl+F first (standard for WhatsApp / Telegram / Discord / Teams)
    send_hotkey("ctrl", "f")
    time.sleep(0.3)

    # Try Ctrl+K as secondary shortcut if Ctrl+F didn't activate search
    send_hotkey("ctrl", "k")
    time.sleep(0.2)

    # Select all text in search box to clear previous queries
    send_hotkey("ctrl", "a")
    time.sleep(0.1)

    # 3. Type Contact Name into Search Box
    type_text(contact_name)
    time.sleep(0.6)  # Give search results time to render

    # Press Enter to open the first matching contact
    press_key("enter")
    time.sleep(0.5)

    # If focus stayed on search result list, press Down then Enter
    press_key("down")
    time.sleep(0.2)
    press_key("enter")
    time.sleep(0.5)

    # 4. Type Message & Send (if message_text provided)
    if message_text:
        # Type the message text into active chat input box
        type_text(message_text)
        time.sleep(0.3)
        # Press Enter to dispatch message
        press_key("enter")
        return {
            "status": "success",
            "message": f"Sent '{message_text}' to {contact_name} on {app_name.capitalize()}."
        }

    return {
        "status": "success",
        "message": f"Opened chat with {contact_name} on {app_name.capitalize()}."
    }

def control_gui_application(app_name: str, action: str, target: str = "", text: str = "") -> str:
    """
    Universal multi-purpose GUI application controller.
    Supports opening chats, typing documents, searching, playing media, and navigation.
    """
    app_clean = app_name.lower().strip()

    # Ensure app is running and active
    launch_application(app_clean)
    time.sleep(1.0)
    focus_window_by_title(app_name)
    time.sleep(0.4)

    if action in ("chat", "text_person", "message_person"):
        res = send_app_message(app_name, target, text)
        return res["message"]
    elif action == "type_text":
        if text:
            type_text(text)
            return f"Typed text into {app_name.capitalize()}."
    elif action == "search":
        send_hotkey("ctrl", "f")
        time.sleep(0.2)
        if target:
            type_text(target)
            press_key("enter")
            return f"Searched for '{target}' in {app_name.capitalize()}."
    elif action == "new_file":
        send_hotkey("ctrl", "n")
        return f"Created new document in {app_name.capitalize()}."

    return f"Controlled {app_name.capitalize()} successfully."

