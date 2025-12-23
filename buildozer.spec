[app]

# (str) Title of your application
title = Aplikasi Kivy Saya

# (str) Package name
package.name = kivyapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,ttf

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.0

#
# Android specific
#

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 26.1.10909125

# (str) Android NDK path, use this to avoid download
android.ndk_path = /home/firdaus/.buildozer/android/platform/android-ndk-r25c
nano buildozer.spec

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

#
# Python for android (p4a) specific
#

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
