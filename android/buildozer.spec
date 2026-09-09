# ===================================================================
# Saathi AI — Buildozer Android Compilation Specification
# Engineered by Pratham Prasad
# ===================================================================

[app]

# (str) Title of your application
title = Saathi AI OS

# (str) Package name
package.name = saathiai

# (str) Package domain (needed for android/ios packaging)
package.domain = com.prathamprasad

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,json,txt,vbs,bat,html,css,js,md

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests,bin,.git,.gradle,.idea,__pycache__

# (str) Application versioning (method 1)
version = 2.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3==3.12.0,hostpython3,requests,urllib3,numpy,setuptools,pip

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = all

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
permissions = INTERNET,RECORD_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,SYSTEM_ALERT_WINDOW,RECEIVE_BOOT_COMPLETED,FOREGROUND_SERVICE,VIBRATE,ACCESS_NETWORK_STATE,MODIFY_AUDIO_SETTINGS,ACCESS_WIFI_STATE,BLUETOOTH

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API required
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25.2.9519653

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (list) List of Java .jar files to add to the libs so that Pygame can perform
# with them.
android.add_jars = 

# (list) List of Java files to add to the android project (paths relative to
# .buildozer/android/platform/python-for-android/dists/app)
#android.add_src =

# (str) Android entrypoint, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (list) Pattern to whitelist for the compilation
#android.whitelist =

# (bool) If True, then skip trying to update the Android sdk
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a symlink
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1

# (str) Path to build artifact storage
build_dir = ./.buildozer

# (str) Path to final APK output directory
bin_dir = ./dist

