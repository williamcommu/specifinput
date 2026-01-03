<img width="613" height="146" alt="image" src="https://github.com/user-attachments/assets/f570dcdc-e2ae-493f-bca3-1d7cd51b0f07" />


Send keyboard inputs to specific windows in the background - perfect for AFK prevention without losing focus on your current work.

## Features

- Send inputs to any window without focusing it
- Configure custom key sequences (WASD, space, etc.)
- Adjustable time intervals
- Global keybind (F9) to toggle from anywhere (Right click start button to change)
- Easy window selection from dropdown

## Requirements

- Python 3.8+
- Linux with X11 (most Linux desktops)
- `xdotool` or `wmctrl` (for window management)

## Installation

1. **Install system dependencies:**

   ```bash
   # On Ubuntu/Debian
   sudo apt install xdotool wmctrl
   
   # On Fedora
   sudo dnf install xdotool wmctrl
   
   # On Arch
   sudo pacman -S xdotool wmctrl
   ```

2. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**

   ```bash
   python main.py
   ```

2. **Configure your automation:**
   - Select the target window from the dropdown
   - Enter the keys to send (space-separated, e.g., `w a s d` or `space`)
   - Set the time interval in seconds
   - Click "ACTIVATE" or press F9

3. **Toggle on/off:**
   - Use the button or press F9 from anywhere

## How It Works

SpecifInput uses `xdotool` to send keyboard inputs directly to specific window IDs, allowing you to:
- Play games in the background while working
- Prevent AFK kicks without keeping the window focused
- Automate repetitive key presses in specific applications

## Key Format

Common keys you can use:
- Letters: `a`, `b`, `c`, ... `z`
- WASD: `w`, `a`, `s`, `d`
- Space: `space`
- Numbers: `1`, `2`, `3`, etc.
- Special: `shift`, `ctrl`, `alt`, `Return`, `Escape`

Multiple keys separated by spaces will be sent in sequence.

## Troubleshooting

**"No windows found":**
- Make sure `xdotool` or `wmctrl` is installed
- Try clicking the Refresh button
- Some minimal windows may not be detected

**Keys not being sent:**
- Ensure the target application accepts background input
- Some games with anti-cheat may block this functionality
- Try running with sudo (not recommended for security reasons)

**Wayland users:**
- This tool works best with X11
- On Wayland, you may need to use `ydotool` (not yet implemented)

## License

MIT License - Free to use and modify

## Disclaimer

Use responsibly. Some games and applications may consider automated input as violation of their terms of service.
I am not reponsible for any bans or penalties incurred from using this tool. This is purely recreation.
This was programmed on Linux Mint, and may not work the same on windows.
