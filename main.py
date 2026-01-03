#!/usr/bin/env python3
"""
SpecifInput - Send inputs to specific windows in the background
Main application entry point
"""

import customtkinter as ctk
from gui.main_window import MainWindow


def main():
    """Initialize and run the application"""
    # Set appearance mode and color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Create and run the main window
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
