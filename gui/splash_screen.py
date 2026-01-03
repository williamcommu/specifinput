"""Splash screen with banner fade-out animation"""

import customtkinter as ctk
from PIL import Image
import tkinter as tk
import os
import threading
import time


class SplashScreen(ctk.CTkToplevel):
    """Splash screen that displays banner and fades out"""
    
    def __init__(self, parent=None, callback=None):
        super().__init__(parent)
        
        self.callback = callback
        self.alpha = 1.0
        self.fade_step = 0.05
        self.fade_delay = 50  # milliseconds
        self.is_closing = False
        self.pending_callbacks = []  # Track scheduled callbacks
        
        # Configure splash window
        self.setup_window()
        
        # Load and display banner
        self.setup_banner()
        
        # Start fade-out timer
        callback_id = self.after(2000, self.start_fade_out)
        self.pending_callbacks.append(callback_id)
    
    def setup_window(self):
        """Configure the splash screen window"""
        # Remove window decorations
        self.overrideredirect(True)
        
        # Set window size and center it
        window_width = 400
        window_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Set background color
        self.configure(fg_color="#1a1a1a")
        
        # Make window stay on top
        self.attributes("-topmost", True)
        
        # Set initial alpha
        self.attributes("-alpha", self.alpha)
    
    def setup_banner(self):
        """Load and display the banner image"""
        try:
            # Get the path to the banner image
            assets_path = os.path.join(os.path.dirname(__file__), "assets", "banner.png")
            
            # Load the image
            banner_image = Image.open(assets_path)
            
            # Resize image to fit window while maintaining aspect ratio
            window_width = 380
            window_height = 280
            
            # Calculate scaling to fit within window
            img_ratio = banner_image.width / banner_image.height
            window_ratio = window_width / window_height
            
            if img_ratio > window_ratio:
                # Image is wider than window ratio
                new_width = window_width
                new_height = int(window_width / img_ratio)
            else:
                # Image is taller than window ratio
                new_height = window_height
                new_width = int(window_height * img_ratio)
            
            banner_image = banner_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to CTkImage for better compatibility
            self.banner_photo = ctk.CTkImage(
                light_image=banner_image,
                dark_image=banner_image,
                size=(new_width, new_height)
            )
            
            # Create label to display image
            self.banner_label = ctk.CTkLabel(
                self,
                image=self.banner_photo,
                text=""
            )
            self.banner_label.place(
                relx=0.5, 
                rely=0.5, 
                anchor="center"
            )
            
        except FileNotFoundError:
            # Fallback: show text if banner image not found
            self.banner_label = ctk.CTkLabel(
                self,
                text="SpecifInput",
                font=ctk.CTkFont(size=32, weight="bold"),
                text_color="white"
            )
            self.banner_label.place(
                relx=0.5, 
                rely=0.4, 
                anchor="center"
            )
            
            # Add subtitle
            subtitle_label = ctk.CTkLabel(
                self,
                text="Background Input Sender",
                font=ctk.CTkFont(size=16),
                text_color="#888888"
            )
            subtitle_label.place(
                relx=0.5, 
                rely=0.6, 
                anchor="center"
            )
        
        except Exception as e:
            print(f"Error loading banner: {e}")
            # Fallback: show text
            self.banner_label = ctk.CTkLabel(
                self,
                text="SpecifInput",
                font=ctk.CTkFont(size=32, weight="bold"),
                text_color="white"
            )
            self.banner_label.place(
                relx=0.5, 
                rely=0.5, 
                anchor="center"
            )
    
    def start_fade_out(self):
        """Begin the fade-out animation"""
        if not self.is_closing:
            self.fade_out()
    
    def fade_out(self):
        """Gradually fade out the splash screen"""
        if self.is_closing:
            return
            
        if self.alpha > 0:
            self.alpha -= self.fade_step
            if self.alpha < 0:
                self.alpha = 0
            
            try:
                self.attributes("-alpha", self.alpha)
                if not self.is_closing:
                    callback_id = self.after(self.fade_delay, self.fade_out)
                    self.pending_callbacks.append(callback_id)
            except tk.TclError:
                # Window might have been destroyed
                self.close_splash()
                return
        else:
            # Fade complete, close splash and show main window
            self.close_splash()
    
    def cancel_pending_callbacks(self):
        """Cancel all pending after() callbacks"""
        for callback_id in self.pending_callbacks:
            try:
                self.after_cancel(callback_id)
            except (tk.TclError, ValueError):
                # Callback already executed or window destroyed
                pass
        self.pending_callbacks.clear()
    
    def close_splash(self):
        """Close the splash screen and trigger callback"""
        if self.is_closing:
            return
            
        self.is_closing = True
        
        # Cancel all pending callbacks
        self.cancel_pending_callbacks()
        
        # Execute callback to show main window
        if self.callback:
            self.callback()