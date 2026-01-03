"""Configuration management for saving and loading setups"""

import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class KeyConfig:
    """Configuration for a single key"""
    hold: float = 0.1
    repeat: int = 1
    wait: float = 0.0


@dataclass 
class Setup:
    """Complete setup configuration"""
    name: str
    window_id: str = ""
    window_title: str = ""
    interval: float = 5.0
    interval_display: str = "5s"  # User-friendly display format
    keybind: str = "F9"
    keys: Dict[str, KeyConfig] = None
    
    def __post_init__(self):
        if self.keys is None:
            self.keys = {}


class ConfigManager:
    """Manages saving and loading of setup configurations"""
    
    def __init__(self, setup_dir: str = "core/setup"):
        self.setup_dir = setup_dir
        os.makedirs(setup_dir, exist_ok=True)
    
    def list_setups(self) -> List[str]:
        """Get list of available setup names"""
        setups = []
        if not os.path.exists(self.setup_dir):
            return setups
            
        for file in os.listdir(self.setup_dir):
            if file.endswith('.json'):
                setups.append(file[:-5])  # Remove .json extension
        
        return sorted(setups)
    
    def save_setup(self, setup: Setup) -> bool:
        """Save a setup to file"""
        try:
            # Convert keybind back to user-friendly format for storage
            display_keybind = self.convert_keybind_to_display(setup.keybind)
            
            config_data = {
                "config": {
                    "window_id": setup.window_id,
                    "window_title": setup.window_title,
                    "interval": setup.interval,
                    "interval_display": setup.interval_display,
                    "keybind": display_keybind
                },
                "process": {}
            }
            
            # Convert keys to the JSON format
            for key, key_config in setup.keys.items():
                config_data["process"][key] = {
                    "hold": key_config.hold,
                    "repeat": key_config.repeat,
                    "wait": key_config.wait
                }
            
            file_path = os.path.join(self.setup_dir, f"{setup.name}.json")
            with open(file_path, 'w') as f:
                json.dump(config_data, f, indent=4)
            
            return True
            
        except Exception as e:
            print(f"Error saving setup {setup.name}: {e}")
            return False
    
    def convert_keybind_to_display(self, tkinter_keybind: str) -> str:
        """Convert Tkinter format back to user-friendly format for display/storage"""
        if "-" not in tkinter_keybind:
            return tkinter_keybind
        
        parts = tkinter_keybind.split("-")
        display_parts = []
        
        for part in parts[:-1]:  # All but the last part are modifiers
            if part == "Control":
                display_parts.append("Ctrl")
            elif part == "Alt":
                display_parts.append("Alt")
            elif part == "Shift":
                display_parts.append("Shift")
            elif part == "Command":
                display_parts.append("Cmd")
            else:
                display_parts.append(part)
        
        # Add the actual key
        key = parts[-1]
        display_parts.append(key)
        
        return "+".join(display_parts)
    
    def load_setup(self, name: str) -> Optional[Setup]:
        """Load a setup from file"""
        try:
            file_path = os.path.join(self.setup_dir, f"{name}.json")
            
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            config = data.get("config", {})
            process = data.get("process", {})
            
            interval = config.get("interval", 5.0)
            # Handle both old (integer only) and new (with display) formats
            interval_display = config.get("interval_display")
            if interval_display is None:
                # Old config - generate display format from seconds
                interval_display = self.seconds_to_display(interval)
            
            # Handle keybind format conversion
            keybind = config.get("keybind", "F9")
            # Convert user format (Ctrl+F) to Tkinter format (Control-F)
            keybind = self.convert_keybind_format(keybind)
            
            setup = Setup(
                name=name,
                window_id=config.get("window_id", ""),
                window_title=config.get("window_title", ""),
                interval=interval,
                interval_display=interval_display,
                keybind=keybind
            )
            
            # Convert process data to KeyConfig objects
            for key, key_data in process.items():
                setup.keys[key] = KeyConfig(
                    hold=key_data.get("hold", 0.1),
                    repeat=key_data.get("repeat", 1),
                    wait=key_data.get("wait", 0.0)
                )
            
            return setup
            
        except Exception as e:
            print(f"Error loading setup {name}: {e}")
            return None
    
    def convert_keybind_format(self, keybind: str) -> str:
        """Convert user-friendly keybind format to Tkinter format"""
        if "+" not in keybind:
            return keybind
        
        parts = keybind.split("+")
        tkinter_parts = []
        
        # Sort modifiers for consistent ordering (Tkinter is sensitive to order)
        modifier_order = {"Control": 0, "Alt": 1, "Shift": 2, "Command": 3}
        modifiers = []
        
        for part in parts[:-1]:  # All but the last part are modifiers
            part = part.strip()
            if part.lower() == "ctrl":
                modifiers.append(("Control", 0))
            elif part.lower() == "alt":
                modifiers.append(("Alt", 1))
            elif part.lower() == "shift":
                modifiers.append(("Shift", 2))
            elif part.lower() == "cmd":
                modifiers.append(("Command", 3))
            else:
                modifiers.append((part.capitalize(), 4))
        
        # Sort modifiers by their order priority
        modifiers.sort(key=lambda x: x[1])
        tkinter_parts = [mod[0] for mod in modifiers]
        
        # Add the actual key
        key = parts[-1].strip()
        tkinter_parts.append(key)
        
        return "-".join(tkinter_parts)
    
    def seconds_to_display(self, seconds: float) -> str:
        """Convert seconds to user-friendly display format - creates compound format for large values"""
        if seconds < 60:
            return f"{int(seconds)}s" if seconds == int(seconds) else f"{seconds}s"
        elif seconds < 3600:
            # Less than 1 hour - show as minutes or minutes+seconds
            minutes = int(seconds // 60)
            remaining_seconds = seconds % 60
            
            if remaining_seconds == 0:
                return f"{minutes}m"
            elif remaining_seconds == int(remaining_seconds):
                return f"{minutes}m,{int(remaining_seconds)}s"
            else:
                return f"{minutes}m,{remaining_seconds}s"
        else:
            # 1+ hours - show as hours or hours+minutes+seconds
            hours = int(seconds // 3600)
            remaining_seconds = seconds % 3600
            minutes = int(remaining_seconds // 60)
            final_seconds = remaining_seconds % 60
            
            parts = [f"{hours}h"]
            
            if minutes > 0:
                parts.append(f"{minutes}m")
            
            if final_seconds > 0:
                if final_seconds == int(final_seconds):
                    parts.append(f"{int(final_seconds)}s")
                else:
                    parts.append(f"{final_seconds}s")
            
            return ",".join(parts)
    
    def display_to_seconds(self, display: str) -> float:
        """Convert display format to seconds - supports compound formats like 2h,30m,15s"""
        display = display.strip().lower()
        
        # Handle compound formats (comma-separated)
        if ',' in display:
            parts = [part.strip() for part in display.split(',')]
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
        if display.endswith('s'):
            return float(display[:-1])
        elif display.endswith('m'):
            return float(display[:-1]) * 60
        elif display.endswith('h'):
            return float(display[:-1]) * 3600
        else:
            # Assume seconds if no unit
            return float(display)
    
    def delete_setup(self, name: str) -> bool:
        """Delete a setup file"""
        try:
            file_path = os.path.join(self.setup_dir, f"{name}.json")
            
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error deleting setup {name}: {e}")
            return False
    
    def setup_exists(self, name: str) -> bool:
        """Check if a setup exists"""
        file_path = os.path.join(self.setup_dir, f"{name}.json")
        return os.path.exists(file_path)