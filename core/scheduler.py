"""Scheduling functionality for periodic input sending"""

import threading
import time
from typing import List
from core.input_sender import InputSender


class InputScheduler:
    """Schedules periodic input sending to a window"""
    
    def __init__(self, input_sender: InputSender, window_id: str, keys: List[str], interval: float):
        """
        Initialize the scheduler
        
        Args:
            input_sender: InputSender instance
            window_id: Target window ID
            keys: List of keys to send
            interval: Time interval in seconds between sends
        """
        self.input_sender = input_sender
        self.window_id = window_id
        self.keys = keys
        self.interval = interval
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the scheduler"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
    
    def _run(self):
        """Main scheduler loop"""
        while self.running:
            # Send keys
            success = self.input_sender.send_keys(self.window_id, self.keys)
            
            if not success:
                # Only print warning every 10 failures to avoid spam
                if not hasattr(self, '_failure_count'):
                    self._failure_count = 0
                self._failure_count += 1
                
                if self._failure_count % 10 == 1:  # Print on 1st, 11th, 21st failure, etc.
                    print(f"Warning: Failed to send keys to window {self.window_id} ({self._failure_count} failures)")
            else:
                # Reset failure count on success
                if hasattr(self, '_failure_count'):
                    self._failure_count = 0
            
            # Wait for interval (check running status frequently for quick stop)
            elapsed = 0
            while elapsed < self.interval and self.running:
                time.sleep(0.1)
                elapsed += 0.1
