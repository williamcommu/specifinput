"""Enhanced scheduling with configuration support"""

import threading
import time
from typing import List, Dict, Optional
from core.enhanced_input_sender import EnhancedInputSender
from core.config_manager import KeyConfig, Setup


class EnhancedScheduler:
    """Enhanced scheduler that supports both simple and advanced configurations"""
    
    def __init__(self, input_sender: EnhancedInputSender, setup: Setup, cycle_callback=None):
        """
        Initialize the enhanced scheduler
        
        Args:
            input_sender: EnhancedInputSender instance
            setup: Complete setup configuration
            cycle_callback: Optional callback function called after each cycle
        """
        self.input_sender = input_sender
        self.setup = setup
        self.cycle_callback = cycle_callback
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
        """Main scheduler loop with advanced configuration"""
        while self.running:
            # Send keys using configuration
            if self.setup.keys:
                success = self.input_sender.send_keys_with_config(
                    self.setup.window_id, 
                    self.setup.keys
                )
            else:
                # Fallback for empty configuration
                success = True
            
            if not success:
                # Only print warning every 10 failures to avoid spam
                if not hasattr(self, '_failure_count'):
                    self._failure_count = 0
                self._failure_count += 1
                
                if self._failure_count % 10 == 1:
                    print(f"Warning: Failed to send keys to window {self.setup.window_id} ({self._failure_count} failures)")
            else:
                # Reset failure count on success and call callback
                if hasattr(self, '_failure_count'):
                    self._failure_count = 0
                
                # Call the callback function if provided (for UI updates)
                if self.cycle_callback and self.running:
                    try:
                        self.cycle_callback()
                    except Exception as e:
                        print(f"Callback error: {e}")
            
            # Wait for interval
            elapsed = 0
            while elapsed < self.setup.interval and self.running:
                time.sleep(0.1)
                elapsed += 0.1


class SimpleScheduler:
    """Simple scheduler for basic key sequences (backward compatibility)"""
    
    def __init__(self, input_sender: EnhancedInputSender, window_id: str, keys: List[str], interval: float):
        """Initialize simple scheduler"""
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
            success = self.input_sender.send_keys_simple(self.window_id, self.keys)
            
            if not success:
                if not hasattr(self, '_failure_count'):
                    self._failure_count = 0
                self._failure_count += 1
                
                if self._failure_count % 10 == 1:
                    print(f"Warning: Failed to send keys to window {self.window_id} ({self._failure_count} failures)")
            else:
                if hasattr(self, '_failure_count'):
                    self._failure_count = 0
            
            elapsed = 0
            while elapsed < self.interval and self.running:
                time.sleep(0.1)
                elapsed += 0.1