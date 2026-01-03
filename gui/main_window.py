"""Main GUI window"""

import customtkinter as ctk
from tkinter import messagebox, simpledialog
from typing import List, Dict
import threading
from core.window_manager import WindowManager
from core.enhanced_input_sender import EnhancedInputSender
from core.enhanced_scheduler import EnhancedScheduler, SimpleScheduler
from core.config_manager import ConfigManager, Setup, KeyConfig


class MainWindow(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("SpecifInput - Background Input Sender")
        self.geometry("700x800")
        self.resizable(False, False)
        
        # Initialize core components
        self.window_manager = WindowManager()
        self.input_sender = EnhancedInputSender()
        self.config_manager = ConfigManager()
        self.scheduler = None
        
        # State variables
        self.is_active = False
        self.selected_window_id = None
        self.current_setup = Setup(name="")
        self.current_keybind = "F9"
        self.run_count = 0
        
        # Setup UI
        self.setup_ui()
        
        # Refresh setups and windows on start
        self.refresh_setups()
        self.refresh_windows()
        
        # Setup keybind (F9 by default)
        self.update_keybind()
    
    def setup_ui(self):
        """Create and layout all UI elements"""
        
        # Main container with padding
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="SpecifInput",
            font=("Helvetica", 28, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Setup management section
        setup_frame = ctk.CTkFrame(main_frame)
        setup_frame.pack(fill="x", pady=(0, 15))
        
        setup_label = ctk.CTkLabel(
            setup_frame,
            text="Configuration Setup:",
            font=("Helvetica", 14)
        )
        setup_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        setup_controls_frame = ctk.CTkFrame(setup_frame, fg_color="transparent")
        setup_controls_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.setup_dropdown = ctk.CTkComboBox(
            setup_controls_frame,
            values=["No setups found"],
            font=("Helvetica", 12),
            width=200,
            command=self.on_setup_selected
        )
        self.setup_dropdown.pack(side="left", padx=(0, 10))
        
        load_btn = ctk.CTkButton(
            setup_controls_frame,
            text="Load",
            command=self.load_setup,
            width=60,
            font=("Helvetica", 12)
        )
        load_btn.pack(side="left", padx=(0, 5))
        
        save_btn = ctk.CTkButton(
            setup_controls_frame,
            text="Save",
            command=self.save_setup,
            width=60,
            font=("Helvetica", 12)
        )
        save_btn.pack(side="left", padx=(0, 5))
        
        delete_btn = ctk.CTkButton(
            setup_controls_frame,
            text="Delete",
            command=self.delete_setup,
            width=60,
            font=("Helvetica", 12),
            fg_color="#EF4444",
            hover_color="#DC2626"
        )
        delete_btn.pack(side="left")
        
        # Window selection section
        window_frame = ctk.CTkFrame(main_frame)
        window_frame.pack(fill="x", pady=(0, 15))
        
        window_label = ctk.CTkLabel(
            window_frame,
            text="Target Window:",
            font=("Helvetica", 14)
        )
        window_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        window_select_frame = ctk.CTkFrame(window_frame, fg_color="transparent")
        window_select_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.window_dropdown = ctk.CTkComboBox(
            window_select_frame,
            values=["No windows found"],
            font=("Helvetica", 12),
            state="readonly",
            width=400
        )
        self.window_dropdown.pack(side="left", padx=(0, 10))
        
        refresh_btn = ctk.CTkButton(
            window_select_frame,
            text="↻ Refresh",
            command=self.refresh_windows,
            width=100,
            font=("Helvetica", 12)
        )
        refresh_btn.pack(side="left")
        
        # Main interval section
        interval_frame = ctk.CTkFrame(main_frame)
        interval_frame.pack(fill="x", pady=(0, 15))
        
        interval_label = ctk.CTkLabel(
            interval_frame,
            text="Main Interval (time between full sequences):",
            font=("Helvetica", 14)
        )
        interval_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        interval_input_frame = ctk.CTkFrame(interval_frame, fg_color="transparent")
        interval_input_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.interval_entry = ctk.CTkEntry(
            interval_input_frame,
            placeholder_text="5s, 2m,30s, 1h,15m",
            font=("Helvetica", 12),
            height=40,
            width=200
        )
        self.interval_entry.pack(side="left", padx=(0, 10))
        self.interval_entry.insert(0, "5s")
        
        interval_help = ctk.CTkLabel(
            interval_input_frame,
            text="Examples: 5s, 2m,30s, 1h,15m,30s",
            font=("Helvetica", 11),
            text_color="#6B7280"
        )
        interval_help.pack(side="left")
        
        # Key configuration section
        keys_frame = ctk.CTkFrame(main_frame)
        keys_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        keys_header_frame = ctk.CTkFrame(keys_frame, fg_color="transparent")
        keys_header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        keys_label = ctk.CTkLabel(
            keys_header_frame,
            text="Key Configuration:",
            font=("Helvetica", 14)
        )
        keys_label.pack(side="left")
        
        add_key_btn = ctk.CTkButton(
            keys_header_frame,
            text="+ Add Key",
            command=self.add_key,
            width=100,
            font=("Helvetica", 12)
        )
        add_key_btn.pack(side="right")
        
        # Scrollable frame for key configurations with mouse wheel support
        self.keys_scroll_frame = ctk.CTkScrollableFrame(
            keys_frame,
            height=200,
            fg_color=("gray90", "gray10")
        )
        self.keys_scroll_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Enable mouse wheel scrolling with a simpler approach
        self.setup_mouse_wheel_scrolling()
        
        self.key_widgets = {}  # Store references to key configuration widgets
        
        # Status and control section
        control_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        control_frame.pack(fill="x")
        
        # Status indicator
        self.status_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        self.status_frame.pack(pady=(0, 15))
        
        self.status_main_label = ctk.CTkLabel(
            self.status_frame,
            text="● INACTIVE",
            font=("Helvetica", 16, "bold"),
            text_color="#EF4444"
        )
        self.status_main_label.pack(side="left")
        
        self.status_counter_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=("Helvetica", 12),
            text_color="#888888"
        )
        self.status_counter_label.pack(side="left", padx=(5, 0))
        
        # Toggle button
        self.toggle_button = ctk.CTkButton(
            control_frame,
            text=f"ACTIVATE ({self.current_keybind})",
            command=self.toggle_active,
            font=("Helvetica", 14, "bold"),
            height=50,
            fg_color="#2563EB",
            hover_color="#1E40AF"
        )
        self.toggle_button.pack(fill="x")
        
        # Add right-click binding for keybind change
        self.toggle_button.bind("<Button-3>", self.change_keybind)
        
        # Keybind info
        self.keybind_label = ctk.CTkLabel(
            control_frame,
            text=f"Press {self.current_keybind} to toggle from anywhere • Right-click button to change",
            font=("Helvetica", 11),
            text_color="#6B7280"
        )
        self.keybind_label.pack(pady=(10, 0))
    
    def setup_mouse_wheel_scrolling(self):
        """Setup mouse wheel scrolling for the keys scroll frame"""
        def _on_mouse_wheel(event):
            # Calculate scroll amount (negative for natural scrolling)
            delta = -1 * (event.delta / 120) if event.delta else (-1 if event.num == 5 else 1)
            
            # Try different methods to scroll the CustomTkinter ScrollableFrame
            try:
                # Method 1: Try to access the internal canvas
                if hasattr(self.keys_scroll_frame, '_parent_canvas'):
                    self.keys_scroll_frame._parent_canvas.yview_scroll(int(delta), "units")
                elif hasattr(self.keys_scroll_frame, '_scrollable_frame'):
                    # Try to find canvas in scrollable frame
                    canvas = None
                    for child in self.keys_scroll_frame.winfo_children():
                        if 'canvas' in str(type(child)).lower():
                            canvas = child
                            break
                    if canvas:
                        canvas.yview_scroll(int(delta), "units")
                else:
                    # Method 2: Try using the frame's master canvas
                    parent = self.keys_scroll_frame.winfo_parent()
                    if parent:
                        master = self.keys_scroll_frame._nametowidget(parent)
                        if hasattr(master, 'yview_scroll'):
                            master.yview_scroll(int(delta), "units")
            except Exception as e:
                print(f"Mouse wheel scroll error: {e}")
        
        def _bind_mousewheel(event):
            # Bind mouse wheel events
            self.bind_all("<MouseWheel>", _on_mouse_wheel)  # Windows/Mac
            self.bind_all("<Button-4>", _on_mouse_wheel)    # Linux scroll up
            self.bind_all("<Button-5>", _on_mouse_wheel)    # Linux scroll down
        
        def _unbind_mousewheel(event):
            # Unbind mouse wheel events
            self.unbind_all("<MouseWheel>")
            self.unbind_all("<Button-4>")
            self.unbind_all("<Button-5>")
        
        # Bind on hover
        self.keys_scroll_frame.bind("<Enter>", _bind_mousewheel)
        self.keys_scroll_frame.bind("<Leave>", _unbind_mousewheel)
    
    def bind_mouse_wheel(self, widget):
        """Enable mouse wheel scrolling for a scrollable widget"""
        def _on_mouse_wheel(event):
            # For CustomTkinter ScrollableFrame, we need to access the canvas differently
            if hasattr(widget, '_parent_canvas'):
                widget._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif hasattr(widget, 'canvas'):  # Try alternative canvas attribute
                widget.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            else:
                # Fallback for different CustomTkinter versions
                try:
                    # Try to find the canvas widget within the scrollable frame
                    for child in widget.winfo_children():
                        if str(child).endswith('.!canvas'):
                            child.yview_scroll(int(-1 * (event.delta / 120)), "units")
                            break
                except:
                    pass
        
        def _bind_to_mousewheel(event):
            self.bind_all("<MouseWheel>", _on_mouse_wheel)
            # Also bind Button-4 and Button-5 for Linux trackpads/mice
            self.bind_all("<Button-4>", lambda e: _on_mouse_wheel(type('MockEvent', (), {'delta': 120})()))
            self.bind_all("<Button-5>", lambda e: _on_mouse_wheel(type('MockEvent', (), {'delta': -120})()))
        
        def _unbind_from_mousewheel(event):
            self.unbind_all("<MouseWheel>")
            self.unbind_all("<Button-4>")
            self.unbind_all("<Button-5>")
        
        # Bind mouse wheel events when hovering over the scrollable frame
        widget.bind('<Enter>', _bind_to_mousewheel)
        widget.bind('<Leave>', _unbind_from_mousewheel)
        
        # Also bind to all children of the scrollable frame
        def bind_children(parent):
            for child in parent.winfo_children():
                try:
                    child.bind('<Enter>', _bind_to_mousewheel)
                    child.bind('<Leave>', _unbind_from_mousewheel)
                    bind_children(child)  # Recursively bind to grandchildren
                except:
                    pass
        
        # Delay binding to children until after they're created
        widget.after(100, lambda: bind_children(widget))
    
    def update_keybind(self):
        """Update the global keybind"""
        # Clear all existing keybinds first
        try:
            self.unbind_all(f"<{self.current_keybind}>")
        except:
            pass
        
        # Set the new keybind
        self.bind_all(f"<{self.current_keybind}>", lambda e: self.toggle_active())
        
        # Create display format (user-friendly)
        display_format = self.current_keybind.replace("-", "+").lower()
        display_format = display_format.replace("control", "ctrl")
        
        # Update UI elements
        if hasattr(self, 'toggle_button'):
            if self.is_active:
                self.toggle_button.configure(text=f"DEACTIVATE ({display_format})")
            else:
                self.toggle_button.configure(text=f"ACTIVATE ({display_format})")
        
        if hasattr(self, 'keybind_label'):
            self.keybind_label.configure(text=f"Press {display_format} to toggle from anywhere • Right-click button to change")
    
    def change_keybind(self, event=None):
        """Handle right-click on toggle button to change keybind"""
        if self.is_active:
            messagebox.showwarning("Cannot Change", "Stop the input sender first before changing keybind")
            return
        
        # Create key capture dialog
        self.capture_keybind()
    
    def capture_keybind(self):
        """Capture a new keybind by listening for keypresses"""
        # Create capture window
        capture_window = ctk.CTkToplevel(self)
        capture_window.title("Capture Keybind")
        capture_window.geometry("400x250")
        capture_window.resizable(False, False)
        capture_window.transient(self)
        
        # Center the window
        capture_window.geometry("+%d+%d" % (
            self.winfo_rootx() + 150,
            self.winfo_rooty() + 200
        ))
        
        # Variables for key capture
        self.captured_key = None
        self.capture_active = True
        
        # UI elements
        title_label = ctk.CTkLabel(
            capture_window,
            text="Press the key combination you want to use",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(20, 10))
        
        current_label = ctk.CTkLabel(
            capture_window,
            text=f"Current: {self.current_keybind}",
            font=("Helvetica", 12),
            text_color="#6B7280"
        )
        current_label.pack(pady=(0, 20))
        
        # Captured key display
        self.capture_display = ctk.CTkLabel(
            capture_window,
            text="Listening for keypress...",
            font=("Helvetica", 14),
            text_color="#2563EB",
            width=300,
            height=40
        )
        self.capture_display.pack(pady=10)
        
        # Manual typing section
        type_label = ctk.CTkLabel(
            capture_window,
            text="Or type manually (F9, ctrl+f, alt+g, etc.):",
            font=("Helvetica", 11),
            text_color="#6B7280"
        )
        type_label.pack(pady=(10, 5))
        
        self.manual_entry = ctk.CTkEntry(
            capture_window,
            placeholder_text="Type key combination...",
            width=250,
            height=30
        )
        self.manual_entry.pack(pady=(0, 15))
        self.manual_entry.bind("<KeyRelease>", self.on_manual_type)
        
        # Buttons
        button_frame = ctk.CTkFrame(capture_window, fg_color="transparent")
        button_frame.pack(pady=(5, 20))
        
        confirm_btn = ctk.CTkButton(
            button_frame,
            text="Confirm",
            command=lambda: self.confirm_captured_keybind(capture_window),
            width=80,
            fg_color="#10B981",
            hover_color="#059669"
        )
        confirm_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=lambda: self.cancel_capture(capture_window),
            width=80,
            fg_color="#EF4444",
            hover_color="#DC2626"
        )
        cancel_btn.pack(side="left")
        
        # Handle window close event
        capture_window.protocol("WM_DELETE_WINDOW", lambda: self.on_capture_window_close(capture_window))
        
        # Make sure window is visible before setting up focus and grab
        capture_window.update_idletasks()
        
        # Now set focus and grab
        capture_window.lift()
        capture_window.focus_set()
        
        # Bind key events after window is ready
        capture_window.bind("<KeyPress>", self.on_key_capture)
        
        # Use after() to delay grab_set until window is fully rendered
        capture_window.after(100, lambda: capture_window.grab_set())
    
    def on_key_capture(self, event):
        """Handle captured keypress"""
        if not self.capture_active:
            return
        
        # Build the key combination with proper modifier ordering
        modifiers = []
        if event.state & 0x4:  # Control
            modifiers.append(("Control", 0))
        if event.state & 0x8:  # Alt
            modifiers.append(("Alt", 1))
        if event.state & 0x1:  # Shift
            modifiers.append(("Shift", 2))
        
        # Sort modifiers by priority for consistency
        modifiers.sort(key=lambda x: x[1])
        
        key = event.keysym
        
        # Handle special keys
        if key.startswith("F") and key[1:].isdigit():
            # Function keys (F1, F2, etc.)
            captured = key
        elif key in ["Return", "Escape", "Space", "Tab"]:
            # Special keys
            captured = key
        elif len(key) == 1 and key.isalpha():
            # Single letters
            captured = key.lower()
        elif key in ["Left", "Right", "Up", "Down"]:
            # Arrow keys
            captured = key
        else:
            # Other keys
            captured = key
        
        # Combine modifiers and key using Tkinter format
        if modifiers:
            tkinter_modifiers = [mod[0] for mod in modifiers]
            self.captured_key = "-".join(tkinter_modifiers) + "-" + captured
            # Also store user-friendly format for display
            display_modifiers = [mod[0].lower().replace("control", "ctrl") for mod in modifiers]
            self.display_key = "+".join(display_modifiers) + "+" + captured.lower()
        else:
            self.captured_key = captured
            self.display_key = captured
        
        # Update display
        self.capture_display.configure(
            text=f"Captured: {self.display_key}",
            text_color="#10B981"
        )
        
        # Also update manual entry
        self.manual_entry.delete(0, "end")
        self.manual_entry.insert(0, self.display_key)
    
    def on_manual_type(self, event):
        """Handle manual typing in the entry"""
        typed_key = self.manual_entry.get().strip()
        if typed_key:
            # Convert user-friendly format to Tkinter format
            self.display_key = typed_key
            self.captured_key = self.convert_to_tkinter_format(typed_key)
            self.capture_display.configure(
                text=f"Typed: {typed_key}",
                text_color="#10B981"
            )
        else:
            self.captured_key = None
            self.display_key = None
            self.capture_display.configure(
                text="Listening for keypress...",
                text_color="#2563EB"
            )
    
    def convert_to_tkinter_format(self, user_format):
        """Convert user-friendly format (ctrl+shift+f) to Tkinter format (Control-Shift-f)"""
        if "+" not in user_format:
            return user_format
        
        parts = user_format.split("+")
        modifiers = []
        
        # Sort modifiers for consistent ordering
        for part in parts[:-1]:  # All but the last part are modifiers
            part = part.strip().lower()
            if part == "ctrl":
                modifiers.append(("Control", 0))
            elif part == "alt":
                modifiers.append(("Alt", 1))
            elif part == "shift":
                modifiers.append(("Shift", 2))
            elif part == "cmd":
                modifiers.append(("Command", 3))
            else:
                modifiers.append((part.capitalize(), 4))
        
        # Sort modifiers by priority
        modifiers.sort(key=lambda x: x[1])
        tkinter_parts = [mod[0] for mod in modifiers]
        
        # Add the actual key
        key = parts[-1].strip()
        tkinter_parts.append(key)
        
        return "-".join(tkinter_parts)
    
    def confirm_captured_keybind(self, capture_window):
        """Confirm and apply the captured keybind"""
        if not self.captured_key:
            messagebox.showerror("No Key", "Please press a key combination or type one manually")
            return
        
        if self.captured_key == self.current_keybind:
            # No change needed
            self.capture_active = False
            capture_window.destroy()
            return
        
        try:
            # Test the keybind
            test_key = f"<{self.captured_key}>"
            self.bind_all(test_key, lambda e: None)
            self.unbind_all(test_key)
            
            # Apply the new keybind
            self.current_keybind = self.captured_key
            self.update_keybind()
            
            self.capture_active = False
            capture_window.destroy()
            
            # Use display format for success message
            display_format = getattr(self, 'display_key', self.captured_key)
            messagebox.showinfo("Success", f"Keybind changed to: {display_format}")
            
        except Exception as e:
            messagebox.showerror("Invalid Key", f"'{self.captured_key}' is not a valid key combination.\n\nError: {str(e)}")
    
    def on_capture_window_close(self, capture_window):
        """Handle window close - auto-apply if keybind changed"""
        if self.captured_key and self.captured_key != self.current_keybind:
            # Ask user if they want to apply the change
            result = messagebox.askyesno(
                "Apply Changes?", 
                f"You captured '{self.captured_key}' but haven't confirmed it.\n\nApply this keybind change?",
                parent=capture_window
            )
            
            if result:
                try:
                    # Test the keybind
                    test_key = f"<{self.captured_key}>"
                    self.bind_all(test_key, lambda e: None)
                    self.unbind_all(test_key)
                    
                    # Apply the new keybind
                    self.current_keybind = self.captured_key
                    self.update_keybind()
                    
                    self.capture_active = False
                    capture_window.destroy()
                    messagebox.showinfo("Success", f"Keybind changed to: {self.captured_key}")
                    return
                    
                except Exception as e:
                    messagebox.showerror("Invalid Key", f"'{self.captured_key}' is not a valid key combination.\n\nError: {str(e)}")
        
        # Close without applying
        self.cancel_capture(capture_window)
    
    def apply_captured_keybind(self, capture_window):
        """Legacy method - now redirects to confirm"""
        self.confirm_captured_keybind(capture_window)
    
    def cancel_capture(self, capture_window):
        """Cancel keybind capture"""
        self.capture_active = False
        capture_window.destroy()
    
    def refresh_setups(self):
        """Refresh the list of available setups"""
        setups = self.config_manager.list_setups()
        
        if setups:
            self.setup_dropdown.configure(values=setups)
            if setups:
                self.setup_dropdown.set("")  # Clear to allow typing new names
        else:
            self.setup_dropdown.configure(values=["No setups found"])
            self.setup_dropdown.set("")
    
    def refresh_windows(self):
        """Refresh the list of available windows"""
        windows = self.window_manager.get_windows()
        
        if windows:
            window_names = [f"{w['title']} ({w['class']})" for w in windows]
            self.window_dropdown.configure(values=window_names)
            self.window_dropdown.set(window_names[0])
            self.window_list = windows
        else:
            self.window_dropdown.configure(values=["No windows found"])
            self.window_dropdown.set("No windows found")
            self.window_list = []
    
    def add_key(self):
        """Add a new key configuration"""
        key = simpledialog.askstring("Add Key", "Enter key name (e.g., 'w', 'space', 'shift'):")
        
        if key and key.strip():
            key = key.strip().lower()
            if key not in self.current_setup.keys:
                self.current_setup.keys[key] = KeyConfig()
                self.update_key_widgets()
            else:
                messagebox.showwarning("Duplicate Key", f"Key '{key}' already exists")
    
    def remove_key(self, key: str):
        """Remove a key configuration"""
        if key in self.current_setup.keys:
            del self.current_setup.keys[key]
            self.update_key_widgets()
    
    def update_key_widgets(self):
        """Update the key configuration widgets"""
        # Clear existing widgets
        for widget in self.keys_scroll_frame.winfo_children():
            widget.destroy()
        self.key_widgets.clear()
        
        if not self.current_setup.keys:
            # Show placeholder when no keys
            placeholder = ctk.CTkLabel(
                self.keys_scroll_frame,
                text="No keys configured. Click '+ Add Key' to get started.",
                font=("Helvetica", 12),
                text_color="#6B7280"
            )
            placeholder.pack(pady=20)
            return
        
        # Create widgets for each key
        for key_name, key_config in self.current_setup.keys.items():
            self.create_key_widget(key_name, key_config)
    
    def create_key_widget(self, key_name: str, key_config: KeyConfig):
        """Create a widget for configuring a single key"""
        # Main frame for this key
        key_frame = ctk.CTkFrame(self.keys_scroll_frame)
        key_frame.pack(fill="x", padx=10, pady=5)
        
        # Header with key name and remove button
        header_frame = ctk.CTkFrame(key_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        key_label = ctk.CTkLabel(
            header_frame,
            text=f"Key: {key_name.upper()}",
            font=("Helvetica", 14, "bold")
        )
        key_label.pack(side="left")
        
        remove_btn = ctk.CTkButton(
            header_frame,
            text="✖ Remove",
            command=lambda k=key_name: self.remove_key(k),
            width=80,
            height=25,
            font=("Helvetica", 10),
            fg_color="#EF4444",
            hover_color="#DC2626"
        )
        remove_btn.pack(side="right")
        
        # Configuration options
        config_frame = ctk.CTkFrame(key_frame, fg_color="transparent")
        config_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Hold time
        hold_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        hold_frame.pack(side="left", padx=(0, 20))
        
        ctk.CTkLabel(hold_frame, text="Hold Time:", font=("Helvetica", 11)).pack()
        hold_entry = ctk.CTkEntry(hold_frame, width=80, height=25)
        hold_entry.pack(pady=(2, 0))
        hold_entry.insert(0, str(key_config.hold))
        
        # Repeat count
        repeat_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        repeat_frame.pack(side="left", padx=(0, 20))
        
        ctk.CTkLabel(repeat_frame, text="Repeat:", font=("Helvetica", 11)).pack()
        repeat_entry = ctk.CTkEntry(repeat_frame, width=80, height=25)
        repeat_entry.pack(pady=(2, 0))
        repeat_entry.insert(0, str(key_config.repeat))
        
        # Wait time
        wait_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        wait_frame.pack(side="left")
        
        ctk.CTkLabel(wait_frame, text="Wait After:", font=("Helvetica", 11)).pack()
        wait_entry = ctk.CTkEntry(wait_frame, width=80, height=25)
        wait_entry.pack(pady=(2, 0))
        wait_entry.insert(0, str(key_config.wait))
        
        # Store widget references for value retrieval
        self.key_widgets[key_name] = {
            'hold': hold_entry,
            'repeat': repeat_entry,
            'wait': wait_entry
        }
    
    def get_current_setup_from_ui(self) -> Setup:
        """Extract current setup configuration from UI"""
        setup = Setup(name=self.current_setup.name)
        
        # Get interval with parsing
        interval_text = self.interval_entry.get().strip() or "5s"
        try:
            setup.interval = self.parse_interval(interval_text)
            setup.interval_display = interval_text
        except ValueError:
            setup.interval = 5.0
            setup.interval_display = "5s"
        
        # Get current keybind
        setup.keybind = self.current_keybind
        
        # Get window info
        selected_value = self.window_dropdown.get()
        if selected_value != "No windows found" and hasattr(self, 'window_list'):
            for i, window_name in enumerate([f"{w['title']} ({w['class']})" for w in self.window_list]):
                if window_name == selected_value:
                    setup.window_id = self.window_list[i]['id']
                    setup.window_title = self.window_list[i]['title']
                    break
        
        # Get key configurations from widgets
        for key_name, widgets in self.key_widgets.items():
            try:
                hold_time = float(widgets['hold'].get() or "0.1")
                repeat_count = int(widgets['repeat'].get() or "1")
                wait_time = float(widgets['wait'].get() or "0")
                
                setup.keys[key_name] = KeyConfig(
                    hold=hold_time,
                    repeat=repeat_count,
                    wait=wait_time
                )
            except ValueError:
                # Use defaults for invalid values
                setup.keys[key_name] = KeyConfig()
        
        return setup
    
    def parse_interval(self, interval_text: str) -> float:
        """Parse interval text to seconds - supports compound formats like 2h,30m,15s"""
        interval_text = interval_text.strip().lower()
        
        # Handle compound formats (comma-separated)
        if ',' in interval_text:
            parts = [part.strip() for part in interval_text.split(',')]
            total_seconds = 0.0
            
            for part in parts:
                if not part:
                    continue
                    
                if part.endswith('s'):
                    total_seconds += float(part[:-1])
                elif part.endswith('m'):
                    total_seconds += float(part[:-1]) * 60
                elif part.endswith('h'):
                    total_seconds += float(part[:-1]) * 3600
                else:
                    # Assume seconds if no unit
                    total_seconds += float(part)
            
            return total_seconds
        
        # Handle single format
        if interval_text.endswith('s'):
            return float(interval_text[:-1])
        elif interval_text.endswith('m'):
            return float(interval_text[:-1]) * 60
        elif interval_text.endswith('h'):
            return float(interval_text[:-1]) * 3600
        else:
            # Assume seconds if no unit
            return float(interval_text)
    
    def load_setup_to_ui(self, setup: Setup):
        """Load a setup configuration into the UI"""
        self.current_setup = setup
        
        # Update interval with display format
        self.interval_entry.delete(0, "end")
        self.interval_entry.insert(0, setup.interval_display)
        
        # Update keybind if different from current
        if setup.keybind != self.current_keybind:
            self.current_keybind = setup.keybind
            self.update_keybind()
        
        # Select matching window if available
        if setup.window_title and hasattr(self, 'window_list'):
            for window in self.window_list:
                if window['title'] == setup.window_title:
                    window_name = f"{window['title']} ({window['class']})"
                    self.window_dropdown.set(window_name)
                    break
        
        # Update key widgets
        self.update_key_widgets()
    
    def on_setup_selected(self, choice):
        """Handle setup selection from dropdown"""
        # This is called when dropdown selection changes
        pass
    
    def load_setup(self):
        """Load the selected setup"""
        selected = self.setup_dropdown.get()
        
        if selected == "No setups found" or not selected:
            return
        
        setup = self.config_manager.load_setup(selected)
        if setup:
            self.load_setup_to_ui(setup)
            messagebox.showinfo("Success", f"Loaded setup '{selected}'")
        else:
            messagebox.showerror("Error", f"Failed to load setup '{selected}'")
    
    def save_setup(self):
        """Save the current configuration as a setup"""
        name = self.setup_dropdown.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter a setup name in the dropdown")
            return
        
        # Check if setup exists
        if self.config_manager.setup_exists(name):
            if not messagebox.askyesno("Overwrite", f"Setup '{name}' already exists. Overwrite?"):
                return
        
        # Get current configuration
        setup = self.get_current_setup_from_ui()
        setup.name = name
        
        # Save setup
        if self.config_manager.save_setup(setup):
            messagebox.showinfo("Success", f"Saved setup '{name}'")
            self.refresh_setups()
            self.setup_dropdown.set(name)
        else:
            messagebox.showerror("Error", f"Failed to save setup '{name}'")
    
    def delete_setup(self):
        """Delete the selected setup"""
        selected = self.setup_dropdown.get()
        
        if selected == "No setups found" or not selected:
            return
        
        if messagebox.askyesno("Delete Setup", f"Delete setup '{selected}'? This cannot be undone."):
            if self.config_manager.delete_setup(selected):
                messagebox.showinfo("Success", f"Deleted setup '{selected}'")
                self.refresh_setups()
                # Reset to empty setup
                self.current_setup = Setup(name="")
                self.update_key_widgets()
            else:
                messagebox.showerror("Error", f"Failed to delete setup '{selected}'")
    
    def toggle_active(self):
        """Toggle the input sender on/off"""
        if not self.is_active:
            # Activate
            if not self.validate_inputs():
                return
            
            # Get current setup from UI
            current_setup = self.get_current_setup_from_ui()
            
            if not current_setup.window_id:
                messagebox.showerror("Error", "Please select a valid window")
                return
            
            if not current_setup.keys:
                messagebox.showerror("Error", "Please add at least one key configuration")
                return
            
            # Start enhanced scheduler
            self.run_count = 0  # Reset counter
            self.scheduler = EnhancedScheduler(self.input_sender, current_setup, self.on_run_cycle)
            self.scheduler.start()
            
            self.is_active = True
            self.update_ui_state()
            
        else:
            # Deactivate
            if self.scheduler:
                self.scheduler.stop()
                self.scheduler = None
            
            self.is_active = False
            self.update_ui_state()
    
    def on_run_cycle(self):
        """Callback when a run cycle completes"""
        self.run_count += 1
        if self.is_active:
            # Update the status labels with new count
            self.status_main_label.configure(text="● ACTIVE")
            self.status_counter_label.configure(text=f"({self.run_count})")
    
    def validate_inputs(self) -> bool:
        """Validate user inputs"""
        # Check interval
        interval_text = self.interval_entry.get().strip()
        if not interval_text:
            messagebox.showerror("Error", "Please enter an interval")
            return False
        
        try:
            interval = self.parse_interval(interval_text)
            if interval <= 0:
                raise ValueError("Interval must be positive")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid interval format. Use examples: 5s, 2m,30s, 1h,15m,30s\n\nError: {str(e)}")
            return False
        
        return True
    
    def update_ui_state(self):
        """Update UI elements based on active state"""
        if self.is_active:
            self.status_main_label.configure(
                text="● ACTIVE",
                text_color="#10B981"
            )
            if self.run_count > 0:
                self.status_counter_label.configure(text=f"({self.run_count})")
            else:
                self.status_counter_label.configure(text="")
            self.toggle_button.configure(
                text=f"DEACTIVATE ({self.current_keybind})",
                fg_color="#EF4444",
                hover_color="#DC2626"
            )
            # Disable inputs while active
            self.window_dropdown.configure(state="disabled")
            self.interval_entry.configure(state="disabled")
            # Disable key widgets
            for widgets in self.key_widgets.values():
                for widget in widgets.values():
                    widget.configure(state="disabled")
        else:
            self.status_main_label.configure(
                text="● INACTIVE",
                text_color="#EF4444"
            )
            self.status_counter_label.configure(text="")
            self.toggle_button.configure(
                text=f"ACTIVATE ({self.current_keybind})",
                fg_color="#2563EB",
                hover_color="#1E40AF"
            )
            # Enable inputs
            self.window_dropdown.configure(state="readonly")
            self.interval_entry.configure(state="normal")
            # Enable key widgets
            for widgets in self.key_widgets.values():
                for widget in widgets.values():
                    widget.configure(state="normal")
    
    def destroy(self):
        """Clean up before closing"""
        if self.scheduler:
            self.scheduler.stop()
        super().destroy()
