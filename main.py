"""Saathi: local-first Hinglish desktop assistant — JARVIS Edition."""
from __future__ import annotations

import json
import os
import queue
import random
import re
import shutil
import subprocess
import sys
import threading
import asyncio
import difflib
import html
import tempfile
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk

try:
    from PIL import ImageGrab  # for screenshots; Image/ImageDraw already imported below for the tray icon
except ImportError:
    ImageGrab = None

try:
    from send2trash import send2trash  # deletes go to Recycle Bin instead of being permanent
except ImportError:
    send2trash = None

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    pystray = None


# ─── JARVIS Color Palette ──────────────────────────────────────────────
# Deep midnight base with JARVIS Green accent
COLOR_BG = "#0a0a0f"
COLOR_PANEL = "#12121f"
COLOR_ACCENT = "#00ff88"
COLOR_ACCENT_DIM = "#00cc6a"
COLOR_TEXT = "#e8e8f0"
COLOR_TEXT_MUTED = "#6a6a80"
COLOR_ORB = "#00ff88"
COLOR_ORB_GLOW = "#00ff8840"
COLOR_HEADER = "#0f0f14"
COLOR_BORDER = "#2a2a3a"
COLOR_SUCCESS = "#00ff88"
COLOR_WARNING = "#ffaa00"
COLOR_ERROR = "#ff5555"


APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
HISTORY_FILE = DATA_DIR / "history.json"
FAST_MODEL = "qwen3:4b-instruct"
DEEP_MODEL = "qwen3:14b"
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"


# ── System prompts ─────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are Saathi, a warm, sharp, capable personal assistant who talks like a real Indian friend, not a robot. Reply only in natural Hinglish, Roman/English letters only (e.g. 'Haan bilkul, abhi karta hoon'). Never use Devanagari, Urdu/Arabic script, or any other writing system. Vary your phrasing, keep it conversational and confident, avoid stiff or repetitive sentence patterns and avoid excessive apologising. Give direct, useful answers. For coding, first state a short plan, then provide complete runnable code and clear run instructions. Be honest about limits. Saathi CAN open apps/websites/media, list/read/create/edit files and folders, run terminal commands, and fetch live data (weather, currency, definitions, Wikipedia, etc.) on the user's desktop once permission is granted or confirmed in the app — say so plainly when something actually happened. Never claim you opened something, changed a file, ran a command, fetched data, sent a message, or controlled a device unless the desktop app actually confirms it happened. Deleting/moving files and running terminal commands always show the user an explicit confirmation with the exact path/command first, regardless of any standing permission — that's a hard rule Saathi cannot waive."""

QUICK_PROMPT = """You are Saathi, chatting casually. Reply only in natural, warm Hinglish using Roman/English letters, never Devanagari or Urdu/Arabic script. Be brief, direct, a little playful, and vary your wording like a real person would — don't sound scripted. You cannot actually play music, open apps, run commands, or touch files yourself from chat — the desktop app handles those separately and will tell the user when it happens. NEVER say or imply a song is "now playing," a file was created, a command ran, or any action is done — if the user wants something done, tell them to phrase it as a direct instruction so the desktop app can act, or acknowledge the app is already handling it. Never reveal hidden reasoning or use
"""