#!/usr/bin/env python3
"""
Auto-start version of Universal Web App Launcher
This version automatically starts the server on startup if a path is saved
"""

from universal_launcher import UniversalWebAppLauncher

if __name__ == "__main__":
    # Create launcher with auto-start enabled
    app = UniversalWebAppLauncher(auto_start=True)
    app.run()