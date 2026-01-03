"""Input sending functionality for sending keys to specific windows"""

import subprocess
from typing import List


class InputSender:
    """Sends keyboard inputs to specific windows"""
    
    def __init__(self):
        self.backend = self._detect_backend()
    
    def _detect_backend(self) -> str:
        """Detect which input tool is available"""
        # Try xdotool first (most common)
        try:
            subprocess.run(
                ["xdotool", "version"],
                capture_output=True,
                check=True,
                timeout=2
            )
            return "xdotool"
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        return "none"
    
    def send_keys(self, window_id: str, keys: List[str]) -> bool:
        """
        Send keys to a specific window
        
        Args:
            window_id: The window ID to send keys to
            keys: List of keys to send
            
        Returns:
            True if successful, False otherwise
        """
        if self.backend == "xdotool":
            return self._send_keys_xdotool(window_id, keys)
        return False
    
    def _send_keys_xdotool(self, window_id: str, keys: List[str]) -> bool:
        """Send keys using xdotool without focusing the window"""
        try:
            # Only use background methods that don't steal focus
            for key in keys:
                # Method 1: Direct key send to window (background only)
                result1 = subprocess.run(
                    ["xdotool", "key", "--window", window_id, key],
                    capture_output=True,
                    timeout=2
                )
                
                if result1.returncode == 0:
                    continue
                
                # Method 2: For single characters, try type (background only)
                if len(key) == 1 and key.isalnum():
                    result2 = subprocess.run(
                        ["xdotool", "type", "--window", window_id, key],
                        capture_output=True,
                        timeout=2
                    )
                    
                    if result2.returncode == 0:
                        continue
                
                # If both background methods failed, log but don't use focus methods
                if result1.stderr:
                    stderr_msg = result1.stderr.decode().strip()
                    if stderr_msg and "BadWindow" not in stderr_msg:  # Suppress common window errors
                        print(f"Debug: Background input failed for key '{key}': {stderr_msg}")
                
                return False
            
            return True
            
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
            return False
