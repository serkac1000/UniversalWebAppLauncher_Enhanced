# Universal Web App Launcher

A flexible GUI application that can launch any web application with a `start.bat` file.

## Features

- **Browse for any app folder** - Select any web application directory
- **Automatic server startup** - Runs `start.bat` from the selected folder
- **Browser auto-launch** - Opens http://127.0.0.1:5000 automatically
- **Real-time monitoring** - Status log shows server output and actions
- **Path memory** - Remembers your last used application path
- **Process management** - Start/stop server controls

## Requirements

- Any web application with a `start.bat` file
- Server must run on port 5000
- Python 3.11+ (for building executable)

## Usage

### Step 1: Build the Executable Files
```bash
python build_universal_launcher.py
```
This creates TWO executable files in the `dist/` folder:
- `UniversalWebAppLauncher.exe` - Main launcher for selecting apps
- `AutoStartLauncher.exe` - Auto-start launcher for daily use

### Step 2: Using the Main Launcher (First Time Setup)
1. Run `dist/UniversalWebAppLauncher.exe`
2. Click "Browse..." to select your web app folder
3. **Important**: The selected folder MUST contain a `start.bat` file
4. Click "🚀 Start Server & Open Browser"
5. The launcher will:
   - Validate that `start.bat` exists in your folder
   - Run `start.bat` from your selected folder
   - Wait 3 seconds for server startup
   - Open your browser to http://127.0.0.1:5000
   - Save your app path for future use

### Step 3: Using the Auto-Start Launcher (Daily Use)
1. After setting up your app path once, use `dist/AutoStartLauncher.exe`
2. This will automatically:
   - Load your saved app path
   - Start the server using the `start.bat` file
   - Open the browser immediately
   - No need to browse for the folder again

### How It Works
The executable files are created from the Python scripts and can launch any web application that has:
- A `start.bat` file in its root directory
- A server that runs on port 5000
- The exe files remember your app path and automate the startup process

## GUI Layout

```
┌─────────────────────────────────────────┐
│        Universal Web App Launcher       │
│                                         │
│ Application Path                        │
│ ┌─────────────────────┐ ┌─────────────┐ │
│ │ /path/to/webapp/    │ │ Browse...   │ │
│ └─────────────────────┘ └─────────────┘ │
│                                         │
│ Server Controls                         │
│ ┌─────────────────────────────────────┐ │
│ │   🚀 Start Server & Open Browser   │ │
│ │          ⏹️ Stop Server            │ │
│ │        🌐 Open Browser Only        │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Status                                  │
│ ┌─────────────────────────────────────┐ │
│ │ [13:45:22] Ready to launch...       │ │
│ │ [13:45:25] Selected folder: ...     │ │
│ │ [13:45:27] ✓ start.bat found       │ │
│ │ [13:45:30] Starting server...       │ │
│ │ [13:45:32] ✓ Server started        │ │
│ │ [13:45:35] ✓ Opening browser       │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Complete Workflow

### Initial Setup (One Time)
1. Build the executables: `python build_universal_launcher.py`
2. Run `dist/UniversalWebAppLauncher.exe`
3. Browse to your app folder (must contain `start.bat`)
4. Test that it starts your server and opens browser
5. Your app path is now saved in `launcher_config.json`

### Daily Usage
1. Double-click `dist/AutoStartLauncher.exe`
2. Your app starts automatically - no browsing needed!
3. To change apps: Use the "Change App Path" button

### Requirements for Your App
Your web application folder must have:
- A `start.bat` file that starts your server
- Server must run on port 5000 (or update the launcher code)
- Server should be accessible at http://127.0.0.1:5000

## Example Use Cases

- **Yoga Pose Recognition App** - Launch with your existing `start.bat`
- **Any Python web app** - Flask, Django, FastAPI apps
- **Node.js applications** - Express, Next.js, etc.
- **Static site servers** - Any folder with HTML files
- **Development servers** - Any project with a `start.bat` script

## Files

- `universal_launcher.py` - Main GUI application (11.5KB)
- `build_universal_launcher.py` - Executable build script (4KB)
- `UniversalWebAppLauncher.spec` - PyInstaller configuration
- `launcher_config.json` - Saves your last used path (auto-created)

## Technical Details

- **Framework**: Python + Tkinter GUI
- **Process Management**: subprocess for server control
- **Browser Integration**: webbrowser module for auto-opening
- **Configuration**: JSON file for persistent settings
- **Build Tool**: PyInstaller for standalone executables
- **Cross-platform**: Works on Windows, Linux, Mac

## Build Process

The build creates a single executable file that includes:
- Python runtime
- All required libraries (tkinter, subprocess, webbrowser, json)
- The launcher application code
- No external dependencies needed on target machine

## Testing

The launcher has been tested with:
- ✓ Yoga Pose Recognition App (current project)
- ✓ Python HTTP server applications
- ✓ Path browsing and selection
- ✓ Server startup and shutdown
- ✓ Browser auto-launch functionality
- ✓ Status logging and monitoring
- ✓ Configuration save/load

Ready for production use!