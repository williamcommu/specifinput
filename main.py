#!/usr/bin/env python3
"""
SpecifInput - Send inputs to specific windows in the background
Main application entry point
"""

import customtkinter as ctk
from gui.main_window import MainWindow
from gui.splash_screen import SplashScreen
import threading
import time


class App:
    """Main application controller"""
    
    def __init__(self):
        self.main_window = None
        self.splash = None
    
    def run(self):
        """Run the application with splash screen"""
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window hidden initially
        self.main_window = MainWindow(start_hidden=True)
        
        # Create and show splash screen
        self.splash = SplashScreen(self.main_window, callback=self.show_main_window)
        
        # Start the main loop
        self.main_window.mainloop()
    
    def show_main_window(self):
        """Show the main application window after splash"""
        # Hide splash screen
        if self.splash:
            self.splash.withdraw()
        
        # Show main window
        if self.main_window:
            self.main_window.deiconify()
            self.main_window.lift()
            self.main_window.focus_force()
        
        # Clean up splash after a delay to avoid callback issues
        if self.splash:
            self.main_window.after(1000, self.cleanup_splash)
    
    def cleanup_splash(self):
        """Clean up splash screen safely"""
        if self.splash:
            try:
                self.splash.destroy()
                self.splash = None
            except:
                pass


def main():
    """Initialize and run the application"""
    app = App()
    app.run()


if __name__ == "__main__":
    main()
