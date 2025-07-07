import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys
import threading
import time
import webbrowser
import json
from pathlib import Path

class UniversalWebAppLauncher:
    def __init__(self, auto_start=False):
        self.root = tk.Tk()
        self.root.title("Universal Web App Launcher")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Center the window
        self.center_window()
        
        # Initialize variables
        self.app_path = tk.StringVar()
        self.server_process = None
        self.config_file = "launcher_config.json"
        self.auto_start = auto_start
        
        # Load saved configuration
        self.load_config()
        
        # Setup UI
        self.setup_ui()
        
        # Auto-start if enabled and path is available
        if self.auto_start and self.app_path.get():
            self.root.after(1000, self.auto_start_server)  # Start after 1 second
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Universal Web App Launcher", 
            font=("Arial", 18, "bold"),
            fg="#2E8B57"
        )
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_label = tk.Label(
            main_frame,
            text="Launch any web application by selecting its folder and running start.bat",
            font=("Arial", 11),
            fg="#666666",
            wraplength=500
        )
        desc_label.pack(pady=(0, 30))
        
        # App path selection frame
        path_frame = tk.LabelFrame(main_frame, text="Application Path", font=("Arial", 12, "bold"))
        path_frame.pack(fill="x", pady=(0, 20))
        
        path_inner_frame = tk.Frame(path_frame)
        path_inner_frame.pack(fill="x", padx=10, pady=10)
        
        # Path entry
        self.path_entry = tk.Entry(
            path_inner_frame,
            textvariable=self.app_path,
            font=("Arial", 10),
            width=50
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Browse button
        browse_btn = tk.Button(
            path_inner_frame,
            text="Browse...",
            command=self.browse_folder,
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            padx=15
        )
        browse_btn.pack(side="right")
        
        # Server controls frame
        controls_frame = tk.LabelFrame(main_frame, text="Server Controls", font=("Arial", 12, "bold"))
        controls_frame.pack(fill="x", pady=(0, 20))
        
        buttons_frame = tk.Frame(controls_frame)
        buttons_frame.pack(pady=15)
        
        # Start server button
        self.start_btn = tk.Button(
            buttons_frame,
            text="🚀 Start Server & Open Browser",
            command=self.start_server_and_browser,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=30,
            pady=10,
            width=25
        )
        self.start_btn.pack(pady=5)
        
        # Stop server button
        self.stop_btn = tk.Button(
            buttons_frame,
            text="⏹️ Stop Server",
            command=self.stop_server,
            font=("Arial", 12, "bold"),
            bg="#f44336",
            fg="white",
            padx=30,
            pady=10,
            width=25,
            state="disabled"
        )
        self.stop_btn.pack(pady=5)
        
        # Open browser button
        self.browser_btn = tk.Button(
            buttons_frame,
            text="🌐 Open Browser Only",
            command=self.open_browser,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            padx=30,
            pady=8,
            width=25
        )
        self.browser_btn.pack(pady=5)
        
        # Change Path button
        self.change_path_btn = tk.Button(
            buttons_frame,
            text="📁 Change App Path",
            command=self.change_app_path,
            font=("Arial", 12),
            bg="#9C27B0",
            fg="white",
            padx=30,
            pady=8,
            width=25
        )
        self.change_path_btn.pack(pady=5)
        
        # Status frame
        status_frame = tk.LabelFrame(main_frame, text="Status", font=("Arial", 12, "bold"))
        status_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Status text widget
        self.status_text = tk.Text(
            status_frame,
            height=8,
            font=("Consolas", 9),
            bg="#f5f5f5",
            fg="#333333",
            wrap="word"
        )
        self.status_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar for status
        scrollbar = tk.Scrollbar(self.status_text)
        scrollbar.pack(side="right", fill="y")
        self.status_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.status_text.yview)
        
        # Initial status
        if self.app_path.get():
            self.log_status(f"Loaded saved app path: {self.app_path.get()}")
            if self.auto_start:
                self.log_status("Auto-start mode enabled - will start server automatically")
            else:
                self.log_status("Click 'Start Server & Open Browser' or use 'Change App Path' for new app")
        else:
            self.log_status("Ready to launch web applications")
            self.log_status("Select an application folder and click 'Start Server & Open Browser'")
        
    def browse_folder(self):
        """Open folder browser dialog"""
        folder_path = filedialog.askdirectory(
            title="Select Web Application Folder",
            initialdir=self.app_path.get() if self.app_path.get() else os.getcwd()
        )
        
        if folder_path:
            self.app_path.set(folder_path)
            self.save_config()
            self.log_status(f"Selected folder: {folder_path}")
            
            # Check if start.bat exists
            start_bat_path = os.path.join(folder_path, "start.bat")
            if os.path.exists(start_bat_path):
                self.log_status("✓ start.bat found in selected folder")
            else:
                self.log_status("⚠️ start.bat not found in selected folder")
    
    def start_server_and_browser(self):
        """Start the server using start.bat and open browser"""
        app_folder = self.app_path.get().strip()
        
        if not app_folder:
            messagebox.showerror("Error", "Please select an application folder first")
            return
        
        if not os.path.exists(app_folder):
            messagebox.showerror("Error", "Selected folder does not exist")
            return
        
        start_bat_path = os.path.join(app_folder, "start.bat")
        if not os.path.exists(start_bat_path):
            messagebox.showerror("Error", "start.bat not found in the selected folder")
            return
        
        try:
            self.log_status("Starting server...")
            self.log_status(f"Running: {start_bat_path}")
            
            # Start the server process
            self.server_process = subprocess.Popen(
                [start_bat_path],
                shell=True,
                cwd=app_folder,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Update UI
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            
            self.log_status("✓ Server started successfully")
            
            # Wait a moment then open browser
            def delayed_browser_open():
                time.sleep(3)  # Wait for server to start
                self.open_browser()
            
            threading.Thread(target=delayed_browser_open, daemon=True).start()
            
            # Monitor server output
            self.monitor_server_output()
            
        except Exception as e:
            self.log_status(f"❌ Failed to start server: {str(e)}")
            messagebox.showerror("Error", f"Failed to start server: {str(e)}")
    
    def stop_server(self):
        """Stop the running server"""
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process = None
                
                # Update UI
                self.start_btn.config(state="normal")
                self.stop_btn.config(state="disabled")
                
                self.log_status("✓ Server stopped")
                
            except Exception as e:
                self.log_status(f"❌ Error stopping server: {str(e)}")
        else:
            self.log_status("No server process to stop")
    
    def open_browser(self):
        """Open browser to localhost:5000"""
        try:
            url = "http://127.0.0.1:5000"
            webbrowser.open(url)
            self.log_status(f"✓ Opening browser: {url}")
            
        except Exception as e:
            self.log_status(f"❌ Failed to open browser: {str(e)}")
    
    def change_app_path(self):
        """Allow user to change the app path"""
        self.browse_folder()
    
    def auto_start_server(self):
        """Automatically start server if path is saved"""
        app_folder = self.app_path.get().strip()
        
        if not app_folder:
            self.log_status("No saved app path found. Please select an app folder.")
            return
        
        if not os.path.exists(app_folder):
            self.log_status(f"❌ Saved path no longer exists: {app_folder}")
            self.log_status("Please select a new app folder.")
            return
        
        start_bat_path = os.path.join(app_folder, "start.bat")
        if not os.path.exists(start_bat_path):
            self.log_status(f"❌ start.bat not found in: {app_folder}")
            self.log_status("Please select a valid app folder.")
            return
        
        self.log_status(f"🚀 Auto-starting server from saved path: {app_folder}")
        self.start_server_and_browser()
    
    def monitor_server_output(self):
        """Monitor server output in a separate thread"""
        def monitor():
            if self.server_process:
                try:
                    # Read server output
                    while self.server_process.poll() is None:
                        output = self.server_process.stdout.readline()
                        if output:
                            self.log_status(f"Server: {output.strip()}")
                        time.sleep(0.1)
                    
                    # Server process ended
                    self.log_status("Server process ended")
                    self.root.after(0, lambda: self.stop_btn.config(state="disabled"))
                    self.root.after(0, lambda: self.start_btn.config(state="normal"))
                    
                except Exception as e:
                    self.log_status(f"Error monitoring server: {str(e)}")
        
        threading.Thread(target=monitor, daemon=True).start()
    
    def log_status(self, message):
        """Add a message to the status log"""
        timestamp = time.strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}\n"
        
        # Append to text widget
        self.status_text.insert("end", full_message)
        self.status_text.see("end")  # Scroll to bottom
        
        # Update the GUI
        self.root.update_idletasks()
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config = {
                "app_path": self.app_path.get()
            }
            with open(self.config_file, "w") as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    self.app_path.set(config.get("app_path", ""))
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def on_closing(self):
        """Handle application closing"""
        if self.server_process:
            try:
                self.server_process.terminate()
            except:
                pass
        
        self.save_config()
        self.root.destroy()
        
    def run(self):
        """Start the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    import sys
    
    # Check for auto-start command line argument
    auto_start = len(sys.argv) > 1 and sys.argv[1] == "--auto-start"
    
    app = UniversalWebAppLauncher(auto_start=auto_start)
    app.run()