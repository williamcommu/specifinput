"""Enhanced input sender with hold time and repeat functionality"""

import subprocess
import time
from typing import List, Dict
from core.config_manager import KeyConfig


class EnhancedInputSender:
    """Sends keyboard inputs with advanced timing and repeat controls"""
    
    def __init__(self):
        self.backend = self._detect_backend()
    
    def _detect_backend(self) -> str:
        """Detect which input tool is available"""
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
    
    def send_keys_with_config(self, window_id: str, key_configs: Dict[str, KeyConfig]) -> bool:
        """
        Send keys to a specific window with individual configuration
        
        Args:
            window_id: The window ID to send keys to
            key_configs: Dictionary of key names to KeyConfig objects
            
        Returns:
            True if all keys sent successfully, False otherwise
        """
        if self.backend != "xdotool":
            return False
        
        try:
            for key_name, config in key_configs.items():
                success = self._send_single_key_with_config(window_id, key_name, config)
                if not success:
                    return False
            
            return True
            
        except Exception as e:
            print(f"Error in send_keys_with_config: {e}")
            return False
    
    def _send_single_key_with_config(self, window_id: str, key: str, config: KeyConfig) -> bool:
        """Send a single key with its specific configuration"""
        try:
            for repeat in range(config.repeat):
                # Send key down
                result_down = subprocess.run(
                    ["xdotool", "keydown", "--window", window_id, key],
                    capture_output=True,
                    timeout=2
                )
                
                if result_down.returncode != 0:
                    # Fallback to simple key press
                    result_simple = subprocess.run(
                        ["xdotool", "key", "--window", window_id, key],
                        capture_output=True,
                        timeout=2
                    )
                    
                    if result_simple.returncode != 0:
                        return False
                    
                    # Wait after key press
                    if config.wait > 0:
                        time.sleep(config.wait)
                    continue
                
                # Hold the key
                if config.hold > 0:
                    time.sleep(config.hold)
                
                # Send key up
                subprocess.run(
                    ["xdotool", "keyup", "--window", window_id, key],
                    capture_output=True,
                    timeout=2
                )
                
                # Wait before next repeat
                if config.wait > 0 and repeat < config.repeat - 1:
                    time.sleep(config.wait)
            
            return True
            
        except Exception as e:
            print(f"Error sending key {key}: {e}")
            return False
    
    def send_keys_simple(self, window_id: str, keys: List[str]) -> bool:
        """
        Simple key sending (for backward compatibility)
        
        Args:
            window_id: The window ID to send keys to
            keys: List of keys to send
            
        Returns:
            True if successful, False otherwise
        """
        if self.backend != "xdotool":
            return False
        
        try:
            for key in keys:
                result = subprocess.run(
                    ["xdotool", "key", "--window", window_id, key],
                    capture_output=True,
                    timeout=2
                )
                
                if result.returncode != 0:
                    return False
            
            return True
            
        except Exception as e:
            return False