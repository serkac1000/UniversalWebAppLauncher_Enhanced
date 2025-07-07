#!/usr/bin/env python3
"""
Build script for Universal Web App Launcher executable.
Creates a standalone executable that can launch any web app with start.bat.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import PyInstaller
        print(f"✓ PyInstaller found: {PyInstaller.__version__}")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")

def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ Cleaned {dir_name} directory")

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building Universal Web App Launcher executables...")
    
    # Build regular launcher
    cmd1 = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                           # Create a single executable file
        "--windowed",                          # Remove console window (for GUI)
        "--name=UniversalWebAppLauncher",      # Name of the executable
        "--distpath=dist",                     # Output directory
        "--workpath=build",                    # Build directory
        "--specpath=.",                        # Spec file location
        "--clean",                             # Clean cache and temporary files
        "--noconfirm",                         # Overwrite output directory without confirmation
        
        # Hidden imports
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=webbrowser",
        "--hidden-import=json",
        "--hidden-import=threading",
        "--hidden-import=subprocess",
        "--hidden-import=pathlib",
        "--hidden-import=time",
        "--hidden-import=os",
        "--hidden-import=sys",
        
        # Main script
        "universal_launcher.py"
    ]
    
    # Build auto-start launcher
    cmd2 = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                           # Create a single executable file
        "--windowed",                          # Remove console window (for GUI)
        "--name=AutoStartLauncher",            # Name of the executable
        "--distpath=dist",                     # Output directory
        "--workpath=build",                    # Build directory
        "--specpath=.",                        # Spec file location
        "--clean",                             # Clean cache and temporary files
        "--noconfirm",                         # Overwrite output directory without confirmation
        
        # Hidden imports
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=webbrowser",
        "--hidden-import=json",
        "--hidden-import=threading",
        "--hidden-import=subprocess",
        "--hidden-import=pathlib",
        "--hidden-import=time",
        "--hidden-import=os",
        "--hidden-import=sys",
        
        # Main script
        "auto_launcher.py"
    ]
    
    try:
        print("Building regular launcher...")
        subprocess.check_call(cmd1)
        print("✓ Regular launcher built successfully!")
        
        print("Building auto-start launcher...")
        subprocess.check_call(cmd2)
        print("✓ Auto-start launcher built successfully!")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def verify_files():
    """Verify that the main files exist"""
    required_files = ["universal_launcher.py", "auto_launcher.py"]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ {file} not found!")
            return False
        print(f"✓ {file} found")
    
    return True

def verify_executables():
    """Verify that executables were created successfully"""
    dist_dir = "dist"
    if not os.path.exists(dist_dir):
        print(f"❌ {dist_dir} directory not found!")
        return False
    
    executables = []
    if sys.platform == "win32":
        executables = ["UniversalWebAppLauncher.exe", "AutoStartLauncher.exe"]
    else:
        executables = ["UniversalWebAppLauncher", "AutoStartLauncher"]
    
    for exe in executables:
        exe_path = os.path.join(dist_dir, exe)
        if not os.path.exists(exe_path):
            print(f"❌ {exe} not created!")
            return False
        
        # Check file size (should be > 0)
        size = os.path.getsize(exe_path)
        if size == 0:
            print(f"❌ {exe} is empty (0 bytes)!")
            return False
        
        print(f"✓ {exe} created successfully ({size:,} bytes)")
    
    return True

def main():
    """Main build process"""
    print("🚀 Universal Web App Launcher Build Script")
    print("=" * 50)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working directory: {script_dir}")
    
    # Verify files
    if not verify_files():
        sys.exit(1)
    
    # Check dependencies
    check_dependencies()
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build executable
    if build_executable():
        # Verify executables were created
        if not verify_executables():
            print("❌ Executable verification failed!")
            sys.exit(1)
        
        regular_exe = os.path.abspath("dist/UniversalWebAppLauncher")
        auto_exe = os.path.abspath("dist/AutoStartLauncher")
        if sys.platform == "win32":
            regular_exe += ".exe"
            auto_exe += ".exe"
            
        print(f"🎉 Build completed successfully!")
        print(f"Regular launcher: {regular_exe}")
        print(f"Auto-start launcher: {auto_exe}")
        
        # Display final instructions
        print("\n" + "=" * 50)
        print("TWO LAUNCHERS CREATED:")
        print("1. UniversalWebAppLauncher.exe - Manual launcher")
        print("   - Browse and select app folder each time")
        print("   - Click 'Start Server & Open Browser'")
        print()
        print("2. AutoStartLauncher.exe - Auto-start launcher")
        print("   - Remembers last used app path")
        print("   - Automatically starts server on launch")
        print("   - Use 'Change App Path' for new apps")
        print()
        print("RECOMMENDED WORKFLOW:")
        print("1. First time: Use UniversalWebAppLauncher.exe")
        print("2. Select your app folder and test")
        print("3. For daily use: Use AutoStartLauncher.exe")
        print("4. It will auto-start your last used app")
        print("5. To switch apps: Click 'Change App Path'")
        print("\n🎯 Your Universal Web App Launchers are ready!")
        
    else:
        print("❌ Build failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()