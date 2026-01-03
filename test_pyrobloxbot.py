#!/usr/bin/env python3
"""
Test script for py-roblox-bot integration with SpecifInput
This script demonstrates how to use pyrobloxbot library for Roblox automation
WINDOWS USERS: Ensure you have pywin32 installed and run with admin rights
WINDOWS ONLY: pip install pywin32
"""

import time
import sys
import traceback
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('roblox_bot_test.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

try:
    import pyrobloxbot as bot
    PYROBLOXBOT_AVAILABLE = True
    logger.info("pyrobloxbot library imported successfully")
except ImportError as e:
    PYROBLOXBOT_AVAILABLE = False
    logger.warning(f"pyrobloxbot not available: {e}")
    logger.info("Install with: pip install pyrobloxbot")


class RobloxBotTester:
    """Test class for py-roblox-bot functionality"""
    
    def __init__(self):
        self.test_results = {}
        
    def run_all_tests(self):
        """Run all available tests"""
        logger.info("Starting Roblox Bot Tests")
        logger.info("=" * 50)
        
        if not PYROBLOXBOT_AVAILABLE:
            logger.error("Cannot run tests - pyrobloxbot not installed")
            return
            
        # Basic functionality tests
        self.test_chat()
        self.test_movement()
        self.test_player_actions()
        self.test_failsafe_configuration()
        
        # Print test summary
        self.print_test_summary()
    
    def test_chat(self):
        """Test chat functionality"""
        test_name = "Chat Test"
        logger.info(f"\nRunning {test_name}...")
        
        try:
            # Test sending a chat message
            logger.info("Sending 'Hello from SpecifInput!' to Roblox chat")
            bot.chat("Hello from SpecifInput!")
            
            # Wait a moment for the command to execute
            time.sleep(1)
            
            # Test sending multiple messages
            messages = [
                "Testing automated chat",
                "Bot integration successful",
                "SpecifInput + pyrobloxbot working!"
            ]
            
            for i, message in enumerate(messages, 1):
                logger.info(f"Sending message {i}/{len(messages)}: {message}")
                bot.chat(message)
                time.sleep(0.5)  # Small delay between messages
            
            self.test_results[test_name] = "PASSED"
            logger.info(f"✅ {test_name} completed successfully")
            
        except Exception as e:
            self.test_results[test_name] = f"FAILED: {str(e)}"
            logger.error(f"❌ {test_name} failed: {e}")
            logger.debug(traceback.format_exc())
    
    def test_movement(self):
        """Test movement controls"""
        test_name = "Movement Test"
        logger.info(f"\nRunning {test_name}...")
        
        try:
            # Test walking forward
            logger.info("Testing walk forward for 2 seconds")
            bot.walk_forward(2)
            
            # Test walking backward
            logger.info("Testing walk backward for 1 second")
            bot.walk_backward(1)
            
            # Test walking left and right
            logger.info("Testing walk left for 1 second")
            bot.walk_left(1)
            
            logger.info("Testing walk right for 1 second")
            bot.walk_right(1)
            
            # Test jumping
            logger.info("Testing jump action")
            bot.jump()
            
            self.test_results[test_name] = "PASSED"
            logger.info(f"✅ {test_name} completed successfully")
            
        except Exception as e:
            self.test_results[test_name] = f"FAILED: {str(e)}"
            logger.error(f"❌ {test_name} failed: {e}")
            logger.debug(traceback.format_exc())
    
    def test_player_actions(self):
        """Test player-related actions"""
        test_name = "Player Actions Test"
        logger.info(f"\nRunning {test_name}...")
        
        try:
            # Wait before reset to ensure character is stable
            logger.info("Waiting 3 seconds before reset...")
            time.sleep(3)
            
            # Test player reset
            logger.info("Testing player reset")
            bot.reset_player()
            
            # Wait for reset to complete
            logger.info("Waiting 5 seconds for reset to complete...")
            time.sleep(5)
            
            self.test_results[test_name] = "PASSED"
            logger.info(f"✅ {test_name} completed successfully")
            
        except Exception as e:
            self.test_results[test_name] = f"FAILED: {str(e)}"
            logger.error(f"❌ {test_name} failed: {e}")
            logger.debug(traceback.format_exc())
    
    def test_failsafe_configuration(self):
        """Test failsafe hotkey configuration"""
        test_name = "Failsafe Configuration Test"
        logger.info(f"\nRunning {test_name}...")
        
        try:
            # Test setting custom failsafe hotkey
            logger.info("Setting failsafe hotkey to Ctrl+Shift+Q")
            bot.set_failsafe_hotkey("ctrl", "shift", "q")
            
            logger.info("Failsafe hotkey configured successfully")
            logger.info("Use Ctrl+Shift+Q to emergency stop the bot")
            
            # Reset to default failsafe
            logger.info("Resetting to default failsafe (Ctrl+M)")
            bot.set_failsafe_hotkey("ctrl", "m")
            
            self.test_results[test_name] = "PASSED"
            logger.info(f"✅ {test_name} completed successfully")
            
        except Exception as e:
            self.test_results[test_name] = f"FAILED: {str(e)}"
            logger.error(f"❌ {test_name} failed: {e}")
            logger.debug(traceback.format_exc())
    
    def test_advanced_sequence(self):
        """Test a complex sequence of actions"""
        test_name = "Advanced Sequence Test"
        logger.info(f"\nRunning {test_name}...")
        
        try:
            logger.info("Starting advanced bot sequence...")
            
            # Complex movement pattern
            logger.info("Executing movement pattern...")
            bot.walk_forward(2)
            bot.walk_right(1)
            bot.jump()
            time.sleep(0.5)
            bot.walk_backward(1)
            bot.walk_left(1)
            
            # Chat sequence
            logger.info("Executing chat sequence...")
            bot.chat("Starting automated sequence")
            time.sleep(1)
            bot.chat("Movement pattern complete")
            time.sleep(1)
            bot.chat("Advanced test successful!")
            
            self.test_results[test_name] = "PASSED"
            logger.info(f"✅ {test_name} completed successfully")
            
        except Exception as e:
            self.test_results[test_name] = f"FAILED: {str(e)}"
            logger.error(f"❌ {test_name} failed: {e}")
            logger.debug(traceback.format_exc())
    
    def print_test_summary(self):
        """Print a summary of all test results"""
        logger.info("\n" + "=" * 50)
        logger.info("TEST SUMMARY")
        logger.info("=" * 50)
        
        passed_tests = 0
        failed_tests = 0
        
        for test_name, result in self.test_results.items():
            if result == "PASSED":
                logger.info(f"✅ {test_name}: {result}")
                passed_tests += 1
            else:
                logger.error(f"❌ {test_name}: {result}")
                failed_tests += 1
        
        logger.info("-" * 50)
        logger.info(f"Total Tests: {len(self.test_results)}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {failed_tests}")
        
        if failed_tests == 0:
            logger.info("🎉 All tests passed!")
        else:
            logger.warning(f"⚠️ {failed_tests} test(s) failed")


def interactive_test():
    """Run interactive test mode"""
    print("\n🤖 Roblox Bot Interactive Test Mode")
    print("=" * 40)
    
    if not PYROBLOXBOT_AVAILABLE:
        print("❌ pyrobloxbot not available!")
        print("Install with: pip install pyrobloxbot")
        return
    
    print("Make sure Roblox is open and you're in a game!")
    print("Emergency stop: Ctrl+M (default failsafe)")
    print("-" * 40)
    
    while True:
        print("\nAvailable commands:")
        print("1. Send chat message")
        print("2. Walk forward (5 sec)")
        print("3. Jump")
        print("4. Reset player")
        print("5. Movement test")
        print("6. Advanced sequence")
        print("7. Exit")
        
        try:
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                message = input("Enter message to send: ")
                bot.chat(message)
                print(f"✅ Sent: {message}")
                
            elif choice == "2":
                print("Walking forward for 5 seconds...")
                bot.walk_forward(5)
                print("✅ Walk completed")
                
            elif choice == "3":
                bot.jump()
                print("✅ Jump executed")
                
            elif choice == "4":
                print("Resetting player...")
                bot.reset_player()
                print("✅ Player reset")
                
            elif choice == "5":
                print("Running movement test...")
                tester = RobloxBotTester()
                tester.test_movement()
                
            elif choice == "6":
                print("Running advanced sequence...")
                tester = RobloxBotTester()
                tester.test_advanced_sequence()
                
            elif choice == "7":
                print("Goodbye! 👋")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-7.")
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Test interrupted by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main function"""
    print("🚀 SpecifInput + py-roblox-bot Test Script")
    print("=" * 45)
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "interactive" or mode == "-i":
            interactive_test()
        elif mode == "automated" or mode == "-a":
            tester = RobloxBotTester()
            tester.run_all_tests()
        elif mode == "help" or mode == "-h":
            print("Usage:")
            print("  python test_pyrobloxbot.py                 # Run automated tests")
            print("  python test_pyrobloxbot.py interactive     # Interactive mode")
            print("  python test_pyrobloxbot.py automated       # Automated mode")
            print("  python test_pyrobloxbot.py help            # Show this help")
        else:
            print(f"❌ Unknown mode: {mode}")
            print("Use 'help' to see available options")
    else:
        # Default to automated tests
        tester = RobloxBotTester()
        tester.run_all_tests()


if __name__ == "__main__":
    main()