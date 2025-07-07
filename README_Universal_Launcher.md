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

### Running from Source
```bash
python universal_launcher.py
```

### Building Executable
```bash
python build_universal_launcher.py
```
This creates `dist/UniversalWebAppLauncher.exe` (Windows) or `dist/UniversalWebAppLauncher` (Linux/Mac).

### Using the Launcher
1. Run the executable or Python script
2. Click "Browse..." to select your web app folder
3. Click "🚀 Start Server & Open Browser"
4. The app will:
   - Run `start.bat` from your selected folder
   - Wait 3 seconds for server startup
   - Open your browser to http://127.0.0.1:5000
   - Show real-time status in the log

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