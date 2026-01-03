"""Window management functionality for detecting and listing windows"""

import subprocess
from typing import List, Dict, Optional


class WindowManager:
    """Manages window detection and listing"""
    
    def __init__(self):
        self.backend = self._detect_backend()
    
    def _detect_backend(self) -> str:
        """Detect which window management tool is available"""
        # Try wmctrl first
        try:
            subprocess.run(
                ["wmctrl", "-l"],
                capture_output=True,
                check=True,
                timeout=2
            )
            return "wmctrl"
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Try xdotool
        try:
            subprocess.run(
                ["xdotool", "search", "--name", ".*"],
                capture_output=True,
                check=True,
                timeout=2
            )
            return "xdotool"
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        return "none"
    
    def get_windows(self) -> List[Dict[str, str]]:
        """Get list of all windows with their IDs and titles"""
        if self.backend == "wmctrl":
            return self._get_windows_wmctrl()
        elif self.backend == "xdotool":
            return self._get_windows_xdotool()
        else:
            return []
    
    def _get_windows_wmctrl(self) -> List[Dict[str, str]]:
        """Get windows using wmctrl"""
        windows = []
        try:
            result = subprocess.run(
                ["wmctrl", "-lx"],
                capture_output=True,
                text=True,
                check=True,
                timeout=2
            )
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                parts = line.split(None, 4)
                if len(parts) >= 5:
                    window_id = parts[0]
                    window_class = parts[2]
                    window_title = parts[4]
                    
                    # Filter out some common windows we don't want
                    if window_title and not window_title.startswith('Desktop'):
                        windows.append({
                            'id': window_id,
                            'title': window_title,
                            'class': window_class
                        })
        
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return windows
    
    def _get_windows_xdotool(self) -> List[Dict[str, str]]:
        """Get windows using xdotool"""
        windows = []
        try:
            # Get all window IDs
            result = subprocess.run(
                ["xdotool", "search", "--name", ".*"],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            window_ids = result.stdout.strip().split('\n')
            
            for window_id in window_ids:
                if not window_id:
                    continue
                
                try:
                    # Get window title
                    title_result = subprocess.run(
                        ["xdotool", "getwindowname", window_id],
                        capture_output=True,
                        text=True,
                        timeout=1
                    )
                    title = title_result.stdout.strip()
                    
                    # Get window class
                    class_result = subprocess.run(
                        ["xdotool", "getwindowclassname", window_id],
                        capture_output=True,
                        text=True,
                        timeout=1
                    )
                    window_class = class_result.stdout.strip()
                    
                    if title and not title.startswith('Desktop'):
                        windows.append({
                            'id': window_id,
                            'title': title,
                            'class': window_class
                        })
                
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    continue
        
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return windows
